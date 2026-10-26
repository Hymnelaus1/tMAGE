# Görülen hatalar ve çözümler

Ayrıntılı bağlam: `17_Handoff_for_new_chat.md` bölüm 7-8. Promptlar: `19_Ajan_Promptlari.md`.

## Model çıktısı
| Hata | Çözüm |
|---|---|
| Çözülmemiş şablon yer tutucuları (`{context.analyses[0]...}`) | promptta "bilinen hatalar" listesi, statik kontrol |
| JSON içinde string birleştirme (mistral) | mistral yalnız measure için |
| Ardışık `\n\n\n...` ile çıktı bozulması, token sınırı | stop dizisi, şemasız yeniden deneme |
| Çift kaçışlı `\\n` | `post()` onarımı |
| Şema ile HTTP 500 (command-r7b), kesilmiş string (mistral) | şema yalnız ilk denemede |
| "Kısa tut" cümlesi testlerin atlanmasına yol açtı | kısalık yerine eksiksizlik istenir |
| Eksik testler (8'den 1) | eksikler script taslağından tamamlanır, "model katkısı" raporlanır |
| qwen2.5:7b DA'da CMRR 17.6 dB, PSRR 1.0 dB (diğerleri 67.8/72.4) | **henüz incelenmedi**; oylama yakaladı |

## Testbench / HSPICE
| Hata | Çözüm |
|---|---|
| Kaynak, CUT örneği veya analiz kartı eksik; AC kaynağı yok | statik kontrol |
| PSRR'da AC kaynağı girişte (besleme yerine) | prompt kuralı, sanity (PSRR 560 dB) |
| `.meas`: `v(out)(12u)`, min/max için `when`, settling için `fall=last` | `max/min`, `vfin` + `when ... rise=last` |
| CMRR testbench'ler arası referans | CMRR sistemde türetilir |
| 130 nm örneklerinden çift besleme | devreye duyarlı besleme (`supply_hint`) |
| FCO VSS=0 ile -7 dB (toprağa bağlı bias) | ±VDD/2 simetrik besleme |
| Aday çökmesi koşuyu düşürüyordu | yalnız o aday düşer, oylama sürer |
| Zombi `pipeline.py` koşuyu "çalışıyor" gösteriyordu | reaper thread + pid kontrolü |

## Altyapı
| Hata | Çözüm |
|---|---|
| `gpt-oss:20b` Ollama'yı çökertiyor | hariç |
| VPN düşünce HSPICE ~120 s bekleyip `Unable to checkout` | lisans portu ön kontrolü |
| Verilog-A: `stdio.h` yok | `gcc glibc-devel` kuruldu; **2026-10-26 duman testi geçti** |

## Benchmark 20261026'da bulunanlar (model_bench_20261026)

### A. Kod hatası: `engine/sim.py read_measures()` başarısız ölçümü yanlış sayıya çeviriyor
HSPICE başarısız ölçümü `failed` diye yazar. Ayrıştırıcı bu kelimeyi ayrı bir "ad" sayıyor, sayı sütunları kayıyor ve `temper` (25) / `alter#` (1) değeri ölçüm gibi okunuyor:
```
 vos     temper    alter#
    failed  25.0000  1        ->  vos = 25.0   (gerçekte: ölçüm başarısız)
```
Etkisi: sahte `vos=25`, `gaincm=25`, `gainpsrr=25`, `psrr=1`, `vfin=25`, `cl_gain=25`. Bu 26+ aday sonucunda görüldü (qwen3:4b-instruct 1, qwen3.5:4b 8, qwen2.5:7b 17). Sanity kuralı bunların bir kısmını yakaladı (vos), bir kısmını kaçırdı (ör. vfin=25 V aralığa takılmayabilir).
**Muhtemelen** eski "qwen2.5:7b PSRR 1.0 dB / CMRR 17.6 dB" uyuşmazlığının da sebebi budur; model değil ayrıştırıcı. Doğrulanmadı, eski batch dosyalarına bakılmalı.
Düzeltme önerisi: `failed` belirtecini o sütunun değeri olarak (NaN) kabul et, `temper`/`alter#` sütunlarını ada göre eşle ve başarısız ölçümü "ölçüm yok" olarak raporla. Düzeltme benchmark bitince yapılacak; kayıtlı `.ms0/.mt0` dosyalarından sonuçlar HSPICE'ı yeniden koşmadan yeniden hesaplanabilir.

### B. Model hatası: ofset ölçümünde `at=` değeri tarama aralığı dışında
qwen2.5:7b FCO'da `.dc Vin -0.05 0.05` taraması + `.meas ... at=0.6`. 0.6 aralık dışı, ölçüm başarısız (HSPICE uyarısı: "Measurement time value specified exceeds analysis limit"). 3 aday x 3 deneme boşa gitti, koşu ~41 dk sürdü ve başarısız oldu (FCO run 1 ve 2). Kök neden: tek besleme (VDD/2=0.6) ortak modu, simetrik besleme (±0.6 V, merkez 0) olan FCO'ya taşınmış.
Pitfall önerileri: `config/prompt_versions/v3_pending_pitfalls.json` (henüz aktif değil).
