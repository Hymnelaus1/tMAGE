---
tags: [tmage, saed90, uyarlama]
---
# 130 nm / SKY130 → SAED 90 nm uyarlaması

Kitteki analizler 130 nm'ye yazılmıştı. **Analiz ve ölçüm komutları (`.ac .tran .noise .dc .meas`) teknolojiden bağımsızdır**; değişen: model adları, kütüphane satırı, besleme düzeni, köşeler, boyutlar.

## SAED90nm (PDK'dan okunanlar)
- Model dosyası: `hspice/SAED90nm.lib`; köşe bölümleri `TT_12 FF_12 SS_12 FS_12 SF_12` (LVT/HVT: `*_12_LVT/HVT`).
- Cihazlar: `n12`, `p12` (+ `_lvt`, `_hvt`); BJT `VPNP`, `LPNP`.
- Çekirdek besleme **1.2 V, tek besleme** (130 nm kiti ±1.2 V çift besleme kullanıyordu).
- `BJT_12` kütüphanesi **yalnızca `TT_12` içinde** hazır gelir; diğer köşelerde ayrıca eklenir (bandgap için önemli).
- Kullanım: `.lib '<pdk>/hspice/SAED90nm.lib' TT_12`, transistör `M1 d g s b n12 w=... l=...`.

## Otomatik uyarlama (`server.py: adapt_netlist`)
1. Kaynak teknolojiyi tespit eder (`NFET/PFET` → gtu130, `sky130_fd_pr__*` → sky130).
2. Model adlarını eşler (`NFET→n12`, `PFET→p12`, `pnp_05v5_...→VPNP`).
3. Eski `.inc` model satırlarını siler, tek `.lib` satırı ekler.
4. SKY130 alt devre çağrılarını (`XM1`) SAED90'daki doğrudan MOSFET'e (`M1`) çevirir.
5. TT dışı köşede BJT varsa `BJT_12` ekler.
6. Rapor üretir: yapılanlar ve **uyarılar** (besleme düzeni farkı, Lmin farkı, boyutların eski teknolojiye göre olması).

Arayüzde 1. bölümde uyarı bandı çıkar; orijinal korunur, *Orijinale dön* vardır.

## Sınırlar
- W/L ve `param_*.cir` değerleri uyarlanmaz (boyutlandırma kapsam dışı). Yine de eski değerlerle DA çalıştı ([[12_Duman_Testi_Sonuclari]]).
- Besleme kaynak satırları elle gözden geçirilmeli.
- Boru hattı v0 yalnızca SAED90 koşturur.
