---
tags: [tmage, dogrulama, karar]
---
# Doğrulama: LLM-as-judge yerine oylama

**Karar (2026-10-25):** Sunumdaki LLM-as-judge, ana doğrulama olarak **çoğunluk oylaması + kural kontrolü** ile değiştirildi. LLM yalnızca isteğe bağlı açıklama için kalır.

## Gerekçe
- Elimizde objektif sinyal var: simülasyon sayıları.
- Hakem modelin yanlılığına bağımlılık yok; küçük yerel modellerle uyumlu.
- Yanlış bias gibi hatalar sayıları ayrıştırır.

## Yöntem
1. N bağımsız testbench adayı üretilir (farklı sıcaklık/örnekleme).
2. Her aday HSPICE'ta koşulur; ölçümler toplanır.
3. **Kural kontrolü (script):** kazanç ≥0 dB, faz payı 0–180°, güç >0, `.meas` hatası yok, ölçümler üretildi. Geçemeyen aday oylamaya girmez.
4. Ölçümler toleransla (varsayılan %5) kümelenir; en kalabalık küme kazanır.
5. Rapor yalnızca kazanan adayın HSPICE sayılarını kullanır.

## Sınırlar
- Tüm modeller aynı hatayı yaparsa çoğunluk yanlış olabilir (model çeşitliliği azaltır).
- N kat koşu maliyeti; Jetson yavaş olduğundan N=1 başlangıç varsayılanı, N=1'de rapor "oylama yapılmadı" bayrağı taşır.
- Yapılandırma `context.json → verification` içinde (`method`, `n`, `tolerance_pct`); arayüz seçici henüz yok.
