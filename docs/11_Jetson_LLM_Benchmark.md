---
tags: [tmage, llm, benchmark, jetson]
---
# Jetson LLM karşılaştırması

**Amaç:** Her ajan (spec, scenario, stimulus, measure) için en uygun yerel modeli bulmak. Araç: `engine/bench.py`.

## Modeller (Orin Nano, Ollama)
qwen2.5:0.5b · llama3.2:1b · qwen3:4b-instruct · qwen3.5:4b · mistral · qwen2.5:7b · command-r7b · ministral-3:8b · gpt-oss:20b (13.8 GB, belleğe sığmayabilir).

## Adil karşılaştırma yöntemi
Her ajan, **diğer aşamaların referans çıktısıyla** denenir:
| Ajan | Girdi | Puan |
|---|---|---|
| spec | devre | doğru port rolü oranı |
| scenario | referans spec | seçilen analizlerin kapsanması |
| stimulus | referans spec/senaryo + referans `.meas` | HSPICE ölçümleri referansın %10'u içinde mi |
| measure | referans testbench | aynı |

Referans: elle yazılmış DA testbench'i (tek besleme 1.2 V, Vcm=0.6 V) önce koşturulur; ölçümleri hedef olur. Kayıt: puan, süre, deneme sayısı, token/sn.

## Çalıştırma
```bash
python3 engine/bench.py                 # tüm modeller
python3 engine/bench.py --models qwen3.5:4b,mistral:latest --timeout 420
```
Çıktı: `bench/<tarih>/report.md` (tablo + ajan başına öneri), `results.json`, model başına tam loglar. VPN bağlı olmalı.

## İlk gözlemler (qwen3.5:4b, tek koşu)
| Aşama | Süre | Token |
|---|---|---|
| spec | 96 sn | 633 |
| scenario | 39 sn | 408 |
| stimulus | 131 sn | 1321 |
| measure | 33 sn | 283 |
~6.6 token/sn. JSON geçerliydi ama testbench'te yer tutucu ve eksik kaynak vardı → [[08_Ajanlar_Arasi_Veri_Aktarimi]] kuralları ve ön doğrulama eklendi.

Sonuçlar ve öneriler: [[16_Rapor_Jetson_LLM]].
