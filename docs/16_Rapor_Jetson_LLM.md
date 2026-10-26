---
tags: [tmage, rapor, llm, benchmark]
---
# Rapor: Jetson LLM karşılaştırması ve iyileştirmeler (2026-10-25)

Yöntem: [[11_Jetson_LLM_Benchmark]]. Görev: SAED90nm üzerinde DA (fark yükselteci) için `ac_loop` + `power_area` testbench'i. Puan = ölçümlerin elle yazılmış referansın %10'u içinde kalma oranı. **Tek koşu, tek topoloji (DA).**

## Donanım karakteristiği
- Jetson Orin Nano (8 GB): saniyede ~4–13 token (4B modeller 7–13, 7–8B modeller 4–7). Süre ağırlıkla çıktı uzunluğuna bağlı.
- Modellerin hepsi **Q4_K_M** (gpt-oss MXFP4). `gpt-oss:20b` (13.8 GB) belleğe sığmıyor ve Ollama sunucusunu çökertiyor: kullanılamaz.
- 4B altı modeller (0.5B, 1B) elendi (ilk denemede geçerli JSON üretemedi).

## Önce / sonra (toplam süre ve puan)
| Model | Temel mod | İyileştirilmiş mod |
|---|---|---|
| qwen3:4b-instruct | stimulus 0.00, measure 0.00 · 319 sn | **1.00 / 1.00 · 78 sn** |
| qwen3.5:4b | stimulus 0.75, measure 0.00 · 150 sn | **1.00 / 1.00 · 91 sn** |
| qwen2.5:7b | stimulus 0.25, measure 0.00 · 252 sn | **1.00 / 1.00 · 91 sn** |

İyileştirilmiş mod diğer modeller: command-r7b 1.00/1.00 (131 sn) · mistral stimulus 0.00 (testbench'i kod gibi yazıyor), measure 1.00 · ministral-3:8b 0.75/0.25 (`.meas` sözdizimi hatası).

## Temel moddaki hata kalıpları
`{context...}` yer tutucuları, eksik kaynak, `duplicated subckt`, `.meas` sözdizimi hatası, uzun/gevşek JSON.

## Yapılan iyileştirmeler (`TMAGE_IMPROVED=1`)
1. **Script önce:** spec (port rolleri) ve scenario (seçilen analizler) script ile; LLM çağrısı gerekmedi (96 sn + 39 sn kazanç).
2. **Taslak → LLM düzeltir:** script, doğrulanmış sözdizimli taslak testbench ve `.meas` satırları üretir; model taslağı temel alır.
3. **RAG:** kitteki gerçek testbench ve `.meas` örnekleri topoloji/metriğe göre isteme eklenir (`knowledge/`, `engine/rag.py`).
4. **Şema + örnek:** Ollama JSON şeması (yalnızca ilk deneme), biçim örneği, token sınırı, kesilen çıktının tespiti.

Not: iyileştirmeler tek paket olarak ölçüldü; hangisinin ne kadar katkı yaptığı (ablation) henüz ayrılmadı.

## Ajan başına öneri
| Ajan | Öneri |
|---|---|
| spec | Script (port adı ipuçları); belirsiz port varsa `qwen2.5:7b` |
| scenario | Script; özel topolojide `qwen3:4b-instruct` |
| stimulus | `qwen3:4b-instruct` ≈ `qwen3.5:4b` ≈ `qwen2.5:7b` (46–52 sn); yedek `command-r7b` |
| measure | `qwen3:4b-instruct` (27 sn); yedek `mistral` (33 sn) |
| doğrulama | Oylama için farklı ailelerden: `qwen3:4b-instruct`, `qwen2.5:7b`, `command-r7b` ([[10_Dogrulama_Oylama]]) |

## Sınırlar
Tek koşu (LLM varyansı), yalnızca DA, referans testbench benim tasarımım, mistral/ministral sonuçları bu görev için geçerli. Taslak şablonları şimdilik DA benzeri (`ac_loop`, `cmrr`, `psrr`, `power_area`) için var.

## Sonraki iyileştirmeler
- FCO, TSO, BGR, COMP, OSC, LNA için taslak şablonları ve RAG örnekleri
- Ablation: her iyileştirmenin tek tek etkisi
- Tekrarlı koşu (varyans), farklı topolojilerde bench
- RAG'a gömme tabanlı arama (Jetson'a gömme modeli)
- 4B modellerin Q8 sürümleri (indirme onayı bekleniyor)
