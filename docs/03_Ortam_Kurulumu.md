---
tags: [tmage, ortam, kurulum]
---
# Ortam kurulumu (MSI, Rocky Linux 9.8)

## Makineler
| Ad | Rol | Tailscale |
|---|---|---|
| `msi` | Ana makine: Rocky 9.8, GNOME, HSPICE | 100.73.38.99 |
| `hym` | Windows PC: uzak masaüstü istemcisi | 100.105.14.59 |
| `jetson-orin` | Jetson Orin Nano: Ollama LLM sunucusu | 100.113.87.120 |

Diskler: `/` 108 GB (sda2); `/opt/synopsys` 250 GB (sdb2, araçlar); `/data` 650 GB (sdb3, geçici kurulum dosyaları).

## Tailscale
```bash
curl -fsSL https://tailscale.com/install.sh | sh
sudo systemctl enable --now tailscaled
sudo tailscale up --hostname=msi
tailscale status
```
- Ağdan bağımsız erişim sağlar (aynı LAN gerekmez). Admin panelinde MSI için *Disable key expiry* seçilmeli.
- Tailscale dnf deposu imza hatası verirse: `dnf --disablerepo=tailscale-stable ...`

## Uzak masaüstü (Windows → MSI)
```bash
sudo dnf install -y epel-release
sudo dnf install -y xrdp xorgxrdp
sudo systemctl enable --now xrdp
sudo firewall-cmd --permanent --add-port=3389/tcp && sudo firewall-cmd --reload
```
- Windows'ta `mstsc` ile `100.73.38.99`; kullanıcı adı **küçük harfle** `hym` (Linux büyük/küçük harfe duyarlı, `Hym` hata verir).
- `xorgxrdp` olmadan oturum açılmaz: *X server could not be started* (`/dev/tty0` izin hatası).
- GNOME oturumu için `~/.xsession`:
```bash
#!/bin/bash
export XDG_SESSION_TYPE=x11
export XDG_CURRENT_DESKTOP=GNOME
export XDG_SESSION_DESKTOP=gnome
exec gnome-session
```
- Aynı kullanıcıyla fiziksel oturum açıkken ikinci GNOME oturumu çakışabilir; gerekirse MSI'de *Log Out*.
- Portu internete açmayın; yalnızca Tailscale üzerinden.

## Uzaktan çalışırken
```bash
gsettings set org.gnome.settings-daemon.plugins.power sleep-inactive-ac-type 'nothing'
gsettings set org.gnome.settings-daemon.plugins.power sleep-inactive-battery-type 'nothing'
```
Pilde uykuyu kapatmak pili hızlı boşaltır; geri almak için `'suspend'`. Pil `pending-charge` durumunda %93'te şarjı durdurabilir (pil koruma limiti); arıza değildir.

## GNOME masaüstü düzeni
- Eklentiler (hazır paketler): `desktop-icons`, `window-list`. Etkinleştirme: `gsettings set org.gnome.shell enabled-extensions "[...]"`
- Hızlı başlatma listesi: `gsettings set org.gnome.shell favorite-apps "[...]"` (Dosyalar, Terminal, Firefox, gedit, Sistem İzleyici).
- Masaüstü kısayolları: `~/Desktop/tmage → ~/tmage`, `~/Desktop/synopsys → /opt/synopsys`.
- Sürekli görünen dock için: `sudo dnf install -y --disablerepo=tailscale-stable gnome-shell-extension-dash-to-dock`.
