#!/bin/bash
# Backs up the whole project folder LOCALLY (always) and pushes committed work to GitHub (when reachable).
# Local copy: $TMAGE_BACKUP_DIR (default /data/tmage_backups, a different physical disk than /).
#   snapshots/<ts>/   full folder incl. git-ignored results and local config; unchanged files are hard links
#   bundles/<ts>.bundle   complete git history (restorable with `git clone <bundle>`)
# Usage: scripts/backup.sh [reason]    reason: commit | timer | manual (only goes into the log)
set -u
ROOT=$(cd "$(dirname "$0")/.." && pwd)
DEST=${TMAGE_BACKUP_DIR:-/data/tmage_backups}
KEEP=${TMAGE_BACKUP_KEEP:-48}
REASON=${1:-manual}
mkdir -p "$DEST/snapshots" "$DEST/bundles" || exit 1
LOG=$DEST/backup.log
log() { echo "$(date '+%F %T') [$REASON] $*" >> "$LOG"; }
exec 9>"$DEST/.lock"
flock -n 9 || { log "skipped: another backup is running"; exit 0; }

ts=$(date +%Y%m%d_%H%M%S)
prev=$(ls -1d "$DEST"/snapshots/*/ 2>/dev/null | grep -v '\.tmp/$' | tail -1)
args=(-a --delete --exclude=__pycache__ --exclude='*.pyc')
[ -n "$prev" ] && args+=("--link-dest=$prev")
if nice -n 19 ionice -c3 rsync "${args[@]}" "$ROOT"/ "$DEST/snapshots/$ts.tmp/" 2>>"$LOG"; then
  mv "$DEST/snapshots/$ts.tmp" "$DEST/snapshots/$ts"
  log "local snapshot ok: snapshots/$ts ($(du -sh --apparent-size "$DEST/snapshots/$ts" | cut -f1))"
else
  log "LOCAL SNAPSHOT FAILED"; rm -rf "$DEST/snapshots/$ts.tmp"; exit 1
fi

# git history bundle, only when refs changed
refs=$(git -C "$ROOT" for-each-ref | sha1sum | cut -d' ' -f1)
if [ "$refs" != "$(cat "$DEST/bundles/.last" 2>/dev/null)" ]; then
  git -C "$ROOT" bundle create "$DEST/bundles/$ts.bundle" --all >/dev/null 2>&1 && echo "$refs" > "$DEST/bundles/.last" && log "git bundle ok: bundles/$ts.bundle"
fi

# prune old copies
ls -1d "$DEST"/snapshots/*/ 2>/dev/null | head -n -"$KEEP" | xargs -r rm -rf
ls -1 "$DEST"/bundles/*.bundle 2>/dev/null | head -n -"$KEEP" | xargs -r rm -f

# GitHub (committed work only; uncommitted files never leave the machine)
if git -C "$ROOT" remote get-url origin >/dev/null 2>&1; then
  if out=$(cd "$ROOT" && GIT_SSH_COMMAND="ssh -o BatchMode=yes -o ConnectTimeout=10" timeout 90 git push origin main --tags 2>&1); then
    log "github push ok: $(echo "$out" | tail -1)"
  else
    log "GITHUB PUSH FAILED (local backup is fine): $(echo "$out" | tail -1)"
  fi
fi
