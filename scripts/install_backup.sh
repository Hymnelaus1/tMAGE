#!/bin/bash
# One-time setup: git post-commit hook + 2-hourly user timer. Safe to re-run.
ROOT=$(cd "$(dirname "$0")/.." && pwd)
cat > "$ROOT/.git/hooks/post-commit" <<H
#!/bin/bash
nohup "$ROOT/scripts/backup.sh" commit >/dev/null 2>&1 &
H
chmod +x "$ROOT/.git/hooks/post-commit"
mkdir -p ~/.config/systemd/user
cat > ~/.config/systemd/user/tmage-backup.service <<U
[Unit]
Description=tMAGE backup (local snapshot + GitHub push)
[Service]
Type=oneshot
ExecStart=$ROOT/scripts/backup.sh timer
U
cat > ~/.config/systemd/user/tmage-backup.timer <<U
[Unit]
Description=tMAGE backup every 2 hours
[Timer]
OnBootSec=10min
OnUnitActiveSec=2h
Persistent=true
[Install]
WantedBy=timers.target
U
systemctl --user daemon-reload && systemctl --user enable --now tmage-backup.timer
echo "hook: $ROOT/.git/hooks/post-commit"; systemctl --user list-timers tmage-backup.timer --no-pager | head -3
