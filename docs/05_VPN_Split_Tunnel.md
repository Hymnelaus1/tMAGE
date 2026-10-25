---
tags: [tmage, vpn, lisans]
---
# VPN ve split tunnel

**Amaç:** Yalnızca HSPICE lisans sunucusu VPN'den geçsin; internet normal bağlantıdan çıksın.

## Yapılandırma
GTÜ'nün kişiye özel `.ovpn` dosyası (**asla depoya girmez**, içinde özel anahtar var) `~/vpn/gtu.ovpn` olarak kopyalanır (`chmod 600`) ve sonuna eklenir:
```
route-nopull
pull-filter ignore "redirect-gateway"
pull-filter ignore "dhcp-option"
pull-filter ignore "block-outside-dns"
route <lisans sunucusu IP> 255.255.255.255 vpn_gateway
```
- `route-nopull`: sunucunun gönderdiği tüm yönlendirmeleri yok sayar.
- `pull-filter`: tüm trafiği VPN'e yönlendirmeyi ve DNS değişikliğini engeller.
- Son satır: yalnızca lisans sunucusunun adresi `tun0` üzerinden gider.

## Bağlanma
```bash
sudo openvpn --config ~/vpn/gtu.ovpn   # kullanıcı adı/parola sorar; terminal açık kalmalı
```
`Initialization Sequence Completed` görülünce bağlandı.

## Doğrulama
```bash
ip -br a | grep tun0                 # tun0 var mı
ip route | grep tun0                 # yalnızca lisans /32 rotası ve VPN alt ağı
curl -s ifconfig.me                  # genel IP DEĞİŞMEMELİ
timeout 5 bash -c 'echo > /dev/tcp/<lisans>/27200' && echo ok
```
Tailscale (100.64.0.0/10) ile çakışmaz.

## Bilinen risk
Terminal kapanırsa ya da VPN kopar ise HSPICE `Unable to checkout (hspice)` verir ve 120 sn bekler. Boru hattı bunu önceden kontrol eder ([[09_Loglama]], [[13_Sorun_Giderme]]).

İsteğe bağlı: sağ üst aç/kapa düğmesi için `NetworkManager-openvpn` + `NetworkManager-openvpn-gnome` kurulur ve profil `nmcli connection import type openvpn` ile içe aktarılır (kurulmadı).
