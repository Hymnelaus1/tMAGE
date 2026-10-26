# HSPICE kılavuzundan çıkarılanlar

Kaynak: `~/Downloads/hspice_sa.pdf`, *HSPICE User Guide: Simulation and Analysis*, 1024 sayfa. Metin: `knowledge/manual/hspice_sa.txt` (pdftotext). Modellere **verilmez**; yalnız doğrulanmış kurallar promptlara aktarılır.

**Dikkat:** kılavuz sürümü **B-2008.09**, kurulu HSPICE **X-2025.06-SP2**. Kurallar eski sürümden; yeni sürümde değişmiş olabilir, bu yüzden her kural küçük bir HSPICE koşusuyla doğrulanmalı.

## .MEASURE (kılavuz s.317-322), `measure` ajanına eklendi
- `.meas` kendisinden önceki **son analiz kartına** bağlanır.
- Ölçüm adı `.param` adıyla çakışırsa HSPICE hata verip durur.
- Eşitlik biçimi yalnız önceki ölçümlerin sonuçlarını kullanır; düğüm gerilimi/akımı içermemeli.
- Olay seçiciler: `rise/fall/cross=n` veya `last`, gecikme `td`. `last` ayrılmış sözcüktür.
- Başarısız ölçüm `0.0e0` yazar (listede FAILED).
- Önceki ölçüm sonucunu kullanan ölçüm, o sonuç bulunana kadar 0 verir.
- `avg/rms/integ` DC taramada anlamsız (uyarı).
- Kurallı örnekler (ek bölüm): kazanç `max vdb(out)`, ugf `trig at=1 targ vdb(out) val=0 fall=1`, PM `find vp(out) when vdb(out)=0`, slew `trig/targ ... rise=1`, `deriv ... when`.

## Verilog-A (bölüm 31, s.760-795), henüz promptlara eklenmedi
- Cihaz bir **X elemanıdır**: `X<ad> <düğümler> <modül> param=değer`.
- `.hdl` ana devrede herhangi bir yerde olabilir, `.subckt` veya IF bloğu içinde **olamaz** (hata).
- Aynı adlı modül ikinci kez yüklenirse yok sayılır (büyük/küçük harf farkı da sayılmaz).
- Modül adı şunlar olamaz: AMP, C, CORE, D, L, NJF, NMOS, NPN, OPT, PJF, PLOT, PMOS, PNP, R, U, W, SP (uyarı verilip modül yok sayılır). Özellikle `amp` yasak.
- Aynı adlı alt devre varsa varsayılan olarak **alt devre kazanır** (`.option vamodel` ile değişir).
- Dosya arama sırası: çalışma dizini, `-hdlpath`, `HSP_HDL_PATH`.
- Modül parametreleri cihaz parametresidir; `.PARAM` ile doğrudan değiştirilemez, örnek satırında verilir.
