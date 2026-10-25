---
tags: [tmage, synopsys, hspice, kurulum]
---
# Synopsys kurulumu

Kaynak: GTÜ kurulum kiti (USB, `SYNOPSYS_KURULUM/`), sürüm X-2025.06-SP2: CustomCompiler, FineSim, HSPICE, IC Validator, StarRC + SAED90nm PDK. Toplam ~72 GB, hedef `/opt/synopsys/tools`.

## Yöntem
Kitin `kur.sh` dosyasının bu makineye uyarlanmış kopyası `/data/installers/kur_tmage.sh` (yollar `/opt/synopsys` ve `/data`'ya çevrildi). 6 adım: md5 kontrolü → sistem kontrolü → Installer → `.spf` kopyalama → ürün kurulumu → PDK.

## Karşılaşılan iki sorun ve çözümü
1. **`SynopsysInstaller_v5.11.run` bash ile çalışmıyordu** (`syntax error near unexpected token '('`). Dosya bir **Perl betiği** (`#!/usr/bin/perl`). Çözüm: betikte `bash "$KIT/installer/...run"` yerine `perl "$KIT/installer/...run"`.
2. **`Invalid Site ID, Synopsys Tools NOT installed`.** `yes yes` ile gelen cevap Site ID'yi geçersiz kıldı. Site ID kitin kılavuzunda (`docs/Synopsys_Kullanim_Rehberi.txt`) yazıyor; **depoya yazılmaz**. Çözüm: `-site_info` dosyası:
```
SiteId      :<kılavuzdaki numara>
LicenseAdmin:GTU
PhoneOrEmail:<eposta>
```
```bash
yes yes | /opt/synopsys/installer/installer \
  -source /data/installers/kaynak_tmp -target /opt/synopsys/tools \
  -site_info /data/installers/site_info
```
- GUI installer (`setup.sh`) kullanılmaz: NVIDIA sürücüsü yok, çökebilir. Yalnızca metin modu.

## PDK ve ortam
```bash
tar -xf pdk/SAED90nm_PDK_10222017.tar -C /opt/synopsys/edk && chmod -R a-w /opt/synopsys/edk/SAED90nm_PDK_10222017
cp /opt/synopsys/edk/SAED90nm_PDK_10222017/install/lib.defs ~/lib.defs
```
`config/env.sh` (örnek dosya `env.sh.example`):
```bash
export HSPICE_HOME=/opt/synopsys/tools/hspice/X-2025.06-SP2/hspice
export PATH=$HSPICE_HOME/bin:$PATH
export SNPSLMD_LICENSE_FILE=27200@<lisans sunucusu>
export SAED90_PDK=/opt/synopsys/edk/SAED90nm_PDK_10222017
```
Lisans erişimi için [[05_VPN_Split_Tunnel]].
