---
tags: [tmage, indeks]
---
# tMAGE: Proje Notları

**tMAGE** (testbench Multi-Agent Generation Engine), analog devreler için testbench üretimini çok ajanlı LLM yapısıyla otomatikleştiren GTÜ ELM491 bitirme projesidir. Bu klasör hem Obsidian kasası hem de depo belgeleridir; yapılan her değişiklik **nasıl yapıldığıyla** birlikte kayıtlıdır.

## Okuma sırası
1. [[01_Proje_Ozeti]]: ne yapıyoruz, neden
2. [[02_Mimari]]: parçalar ve akış
3. [[03_Ortam_Kurulumu]]: MSI, Tailscale, uzak masaüstü
4. [[04_Synopsys_Kurulumu]]: HSPICE ve PDK
5. [[05_VPN_Split_Tunnel]]: lisans sunucusuna erişim
6. [[06_Teknoloji_Uyarlama_90nm]]: 130 nm → SAED90 uyarlaması
7. [[07_Arayuz_ve_API]]: web arayüzü
8. [[08_Ajanlar_Arasi_Veri_Aktarimi]]: aşama şemaları
9. [[09_Loglama]]
10. [[10_Dogrulama_Oylama]]: neden hakem yerine oylama
11. [[11_Jetson_LLM_Benchmark]]: her ajan için model seçimi
12. [[12_Duman_Testi_Sonuclari]]: ilk HSPICE sonuçları
13. [[16_Rapor_Jetson_LLM]]: model karşılaştırma raporu ve iyileştirmeler

## Operasyon
- [[13_Sorun_Giderme]]: karşılaşılan hatalar ve çözümleri
- [[14_Yapilacaklar]]
- [[15_Degisiklik_Gunlugu]]

## Hızlı başlangıç
```bash
source ~/tmage/config/env.sh        # HSPICE yolu ve lisans
~/tmage/run.sh                      # arayüz: http://127.0.0.1:8765
sudo openvpn --config ~/vpn/gtu.ovpn  # lisans için (ayrı terminalde açık kalmalı)
```
