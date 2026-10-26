---
tags: [tmage, vpn, license]
---
# VPN and split tunnel

**Goal:** Only the HSPICE license server goes through the VPN; the internet uses the normal connection.

## Configuration
The personal GTU `.ovpn` file (**never committed**, it contains a private key) is copied to `~/vpn/gtu.ovpn` (`chmod 600`) and these lines are appended:
```
route-nopull
pull-filter ignore "redirect-gateway"
pull-filter ignore "dhcp-option"
pull-filter ignore "block-outside-dns"
route <license server IP> 255.255.255.255 vpn_gateway
```
- `route-nopull`: ignores all routes the server pushes.
- `pull-filter`: blocks sending all traffic into the VPN and the DNS change.
- Last line: only the license server's address goes through `tun0`.

## Connecting
```bash
sudo openvpn --config ~/vpn/gtu.ovpn   # asks for user name/password; keep the terminal open
```
`Initialization Sequence Completed` means it is connected.

## Verification
```bash
ip -br a | grep tun0                 # does tun0 exist
ip route | grep tun0                 # only the license /32 route and the VPN subnet
curl -s ifconfig.me                  # the public IP must NOT change
timeout 5 bash -c 'echo > /dev/tcp/<license>/27200' && echo ok
```
It does not clash with Tailscale (100.64.0.0/10).

## Known risk
If the terminal closes or the VPN drops, HSPICE reports `Unable to checkout (hspice)` and waits 120 s. The pipeline checks this beforehand ([[09_Logging]], [[13_Troubleshooting]]).

Optional: for an on/off button at the top right, install `NetworkManager-openvpn` + `NetworkManager-openvpn-gnome` and import the profile with `nmcli connection import type openvpn` (not installed).
