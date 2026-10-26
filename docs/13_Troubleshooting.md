---
tags: [tmage, troubleshooting]
---
# Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| RDP: `User does not exist` | User name in capitals (`Hym`) | Lower case `hym`; delete the saved Windows credential |
| RDP: `X server could not be started` | `xorgxrdp` missing / `/dev/tty0` permission | `sudo dnf install xorgxrdp`; restart xrdp |
| RDP black screen / closes at once | A physical GNOME session of the same user is open | *Log Out* on the MSI |
| Pasted commands get merged | Terminal multi-line paste | Run the commands one by one |
| No `sudo` / a terminal is needed | The `!` command runs without a TTY | Run it in a normal terminal |
| `SynopsysInstaller_v5.11.run` syntax error | It is a Perl script, it was run with bash | `perl ...run` ([[04_Synopsys_Install]]) |
| `Invalid Site ID` | The installer expects an interactive Site ID | A `-site_info` file |
| `Cannot connect to license server` / `Unable to checkout` | VPN is down | [[05_VPN_Split_Tunnel]]; `ip -br a \| grep tun0` |
| HSPICE hangs for 120 s | License retry wait time | Try the license port first (the pipeline does this) |
| `{context...}` in a testbench | A small model leaves a placeholder | Pre-validation + feedback loop |
| `tailscale` repository signature error | Repository key | `dnf --disablerepo=tailscale-stable` |
| Battery `Not charging` at 93 % | Battery-care limit | Not a fault; charging resumes when it drops |
| `pkill -f server.py` kills the shell | The pattern matches its own command line | `kill $(pgrep -f '^python3 app/server.py')` |
| A half-finished run blocks a new one | Stale `status.json` | pid check (fixed) |
| `stale info` on `git push --force-with-lease` after a history rewrite | The rewrite also rewrote the local `origin/main` | `--force-with-lease=main:<expected hash>` |
| An HSPICE `.meas` printed as 25.0 or 1.0 | The measure failed and the parser read the temperature / alter# column | See [[20_Observed_Errors]] (open bug) |
