---
tags: [tmage, mimari]
---
# Mimari

```
Kullanıcı arayüzü (web)  ──job.json──▶  runs/<id>/
                                          │  context.json  (LLM'lere standart özet)
                                          ▼
 spec ─▶ scenario ─▶ stimulus ─▶ measure ─▶ [HSPICE] ─▶ verify (kural + oylama) ─▶ report
 (LLM)    (LLM)       (LLM)       (LLM)       script        script                  script
```

## Klasörler (`~/tmage`)
| Yol | Görev |
|---|---|
| `app/server.py`, `app/static/index.html` | Web arayüzü ve API ([[07_Arayuz_ve_API]]) |
| `config/catalog.json` | Topolojiler, teknolojiler, analizler, ajanlar, sağlayıcılar |
| `config/stages.json` | Aşama şemaları ve ajan görevleri ([[08_Ajanlar_Arasi_Veri_Aktarimi]]) |
| `config/env.sh` | HSPICE yolu, lisans, PDK (örnek: `env.sh.example`) |
| `engine/handoff.py` | Bağlam üretimi, aşama doğrulama, istem oluşturma |
| `engine/pipeline.py` | Boru hattı ([[09_Loglama]], [[10_Dogrulama_Oylama]]) |
| `engine/llm.py`, `sim.py`, `log.py` | Ollama çağrısı, HSPICE koşusu, loglama |
| `engine/bench.py` | Model karşılaştırması ([[11_Jetson_LLM_Benchmark]]) |
| `runs/` | Koşu çıktıları (depoya girmez) |

## Tasarım kararları
- **Script ne yapabilirse script yapar:** netlist ayrıştırma, PDK satırı, köşe döngüsü, HSPICE koşusu, ölçüm okuma, kurallar, rapor biçimi. LLM yalnızca karar ve yaratıcılık gereken yerde.
- **Bağımlılıksız:** sunucu ve motor yalnızca Python standart kütüphanesi (3.9) kullanır.
- **Bilgi aktarımı sabit şemayla:** [[08_Ajanlar_Arasi_Veri_Aktarimi]].
- **Doğrulama:** LLM-as-judge yerine oylama + kural kontrolü ([[10_Dogrulama_Oylama]]).
