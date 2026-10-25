---
tags: [tmage, hspice, sonuc]
---
# Duman testi: SAED90 üzerinde DA

**Amaç:** Araç zincirinin (HSPICE + lisans + SAED90 + uyarlama) çalıştığını doğrulamak.
**Devre:** kitin `amp_llm.sp` (130 nm) → tMAGE uyarlaması → `.lib ... TT_12`. Boyutlar 130 nm'den olduğu gibi.
**Lisans:** `1(in_use)/50(total) FLOATING license(s)`.

| Ölçüm | SAED90 (TT) | Eski 130 nm koşusu (`amp.ma0`) |
|---|---|---|
| Kazanç | 40.38 dB | 33.83 dB |
| BW (0 dB) | 115 MHz | 30.35 kHz |
| Faz payı | 61.56° | — |
| CMRR | 103.3 dB | — |
| PSRR | 58.86 dB | — |
| Güç | 0.853 mW | — |

## HSPICE uyarıları
- ±1.2 V çift besleme 1.2 V cihazlar için fazla (2.4 V). Gerçek koşularda tek besleme, VDD 1.2 V, VSS 0.
- PSRR testbench'inde `vin3` kaynağına değer verilmemiş (HSPICE sıfır varsaydı).
- Bir transistörde `Acde` geometri uyarısı (W=24.7 µm, L=1.0 µm); boyutlar 90 nm için uygun değil.

**Sonuç:** araç zinciri çalışıyor; sayılar boyutlandırılmamış devreye ait, yalnızca doğrulama içindir.
