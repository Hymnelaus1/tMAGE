---
tags: [tmage, environment, setup]
---
# Environment setup (MSI, Rocky Linux 9.8)

## Machines
| Name | Role | Tailscale |
|---|---|---|
| `msi` | Main machine: Rocky 9.8, GNOME, HSPICE | 100.73.38.99 |
| `hym` | Windows PC: remote desktop client | 100.105.14.59 |
| `jetson-orin` | Jetson Orin Nano: Ollama LLM server | 100.113.87.120 |

Disks: `/` 108 GB (sda2); `/opt/synopsys` 250 GB (sdb2, tools); `/data` 650 GB (sdb3, temporary installer files).

## Tailscale
```bash
curl -fsSL https://tailscale.com/install.sh | sh
sudo systemctl enable --now tailscaled
sudo tailscale up --hostname=msi
tailscale status
```
- Gives access independent of the network (no shared LAN needed). In the admin panel choose *Disable key expiry* for MSI.
- If the Tailscale dnf repository gives a signature error: `dnf --disablerepo=tailscale-stable ...`

## Remote desktop (Windows to MSI)
```bash
sudo dnf install -y epel-release
sudo dnf install -y xrdp xorgxrdp
sudo systemctl enable --now xrdp
sudo firewall-cmd --permanent --add-port=3389/tcp && sudo firewall-cmd --reload
```
- On Windows use `mstsc` to `100.73.38.99`; the user name must be **lower case** `hym` (Linux is case sensitive, `Hym` fails).
- Without `xorgxrdp` the session does not start: *X server could not be started* (`/dev/tty0` permission error).
- `~/.xsession` for a GNOME session:
```bash
#!/bin/bash
export XDG_SESSION_TYPE=x11
export XDG_CURRENT_DESKTOP=GNOME
export XDG_SESSION_DESKTOP=gnome
exec gnome-session
```
- A second GNOME session can clash while a physical session of the same user is open; if needed use *Log Out* on the MSI.
- Do not expose the port to the internet; use it only over Tailscale.

## Working remotely
```bash
gsettings set org.gnome.settings-daemon.plugins.power sleep-inactive-ac-type 'nothing'
gsettings set org.gnome.settings-daemon.plugins.power sleep-inactive-battery-type 'nothing'
```
Turning off sleep on battery drains it quickly; use `'suspend'` to revert. The battery can stop charging at 93 % in the `pending-charge` state (battery-care limit); this is not a fault.

## GNOME desktop layout
- Extensions (ready packages): `desktop-icons`, `window-list`. Enable with: `gsettings set org.gnome.shell enabled-extensions "[...]"`
- Quick-launch list: `gsettings set org.gnome.shell favorite-apps "[...]"` (Files, Terminal, Firefox, gedit, System Monitor).
- Desktop shortcuts: `~/Desktop/tmage -> ~/tmage`, `~/Desktop/synopsys -> /opt/synopsys`.
- For an always-visible dock: `sudo dnf install -y --disablerepo=tailscale-stable gnome-shell-extension-dash-to-dock`.
