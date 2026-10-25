---
tags: [tmage, sorun-giderme]
---
# Sorun giderme

| Belirti | Neden | Çözüm |
|---|---|---|
| RDP: `User does not exist` | Kullanıcı adı büyük harfle (`Hym`) | Küçük harf `hym`; kayıtlı Windows kimlik bilgisini sil |
| RDP: `X server could not be started` | `xorgxrdp` yok / `/dev/tty0` izni | `sudo dnf install xorgxrdp`; xrdp'yi yeniden başlat |
| RDP siyah ekran / hemen kapanma | Aynı kullanıcıyla fiziksel GNOME oturumu açık | MSI'de *Log Out* |
| Yapıştırılan komutlar birleşiyor | Terminal çoklu satır yapıştırma | Komutları tek tek çalıştır |
| `sudo` yok / terminal gerekli | `!` komutu TTY'siz | Normal terminalde çalıştır |
| `SynopsysInstaller_v5.11.run` sözdizimi hatası | Perl betiği, bash ile çalıştı | `perl ...run` ([[04_Synopsys_Kurulumu]]) |
| `Invalid Site ID` | Installer interaktif Site ID bekliyor | `-site_info` dosyası |
| `Cannot connect to license server` / `Unable to checkout` | VPN kopuk | [[05_VPN_Split_Tunnel]]; `ip -br a \| grep tun0` |
| HSPICE 120 sn takılıyor | Lisans yeniden deneme bekleme süresi | Önce lisans portunu denemek (boru hattı yapar) |
| Testbench'te `{context...}` | Küçük model yer tutucu bırakıyor | Ön doğrulama + geri bildirim döngüsü |
| `tailscale` deposu imza hatası | Depo anahtarı | `dnf --disablerepo=tailscale-stable` |
| Pil %93'te `Not charging` | Pil koruma limiti | Arıza değil; pil düşünce şarj başlar |
| `pkill -f server.py` kabuğu öldürüyor | Desen kendi komut satırına uyuyor | `kill $(pgrep -f '^python3 app/server.py')` |
| Yarım kalan koşu yenisini engelliyor | `status.json` bayat | pid kontrolü (düzeltildi) |
