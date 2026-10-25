---
tags: [tmage, ajan, sema]
---
# Ajanlar arası veri aktarımı

Kullanıcı seçimleri kaydedilir ve ajanlara **sabit biçimde** aktarılır (`engine/handoff.py`, `config/stages.json`).

## Koşu klasörü (`runs/<tarih>_<ad>/`)
| Dosya | Anlam |
|---|---|
| `job.json` | Kullanıcının seçimleri (değişmez) |
| `circuit.sp` | Devre (uyarlandıysa uyarlanmış hâli) |
| `context.json` | LLM'lere verilen standart özet (değişmez) |
| `stages/NN_ad.json` | Her aşamanın çıktısı |
| `trace.jsonl` | Kim, ne zaman, hangi model |

## `context.json` içeriği
Teknoloji (VDD, köşe başına `.lib` satırı, cihaz adları, notlar) · devre (subckt, portlar, **script'in ürettiği port rol ipuçları**, parametreler) · topoloji · seçilen analizler (metrikler, parametreler) · doğrulama ayarları · ajan→model eşlemesi.

## Aşamalar
`spec → scenario → stimulus → measure → verify → report`. Her aşamanın `needs` listesi vardır; ajan yalnızca `context` + o aşamaların çıktısını görür. Bitmemiş aşama istenirse hata verir.

## Kurallar
- Çıktı tek bir JSON nesnesi; şemadaki alanlar zorunlu (eksikse yazma reddedilir).
- Ajanlara: yalnızca context'teki bilgiyi kullan, uydurma, belirsizliği `open_questions` / `assumptions`'a yaz.
- **stimulus:** yer tutucu (`{...}`, `context.`) yasak, sayılar doğrudan yazılır; DUT çağrısı `X0 <portlar> <subckt>`; `.lib/.inc/.end/.meas` yazılmaz (sistem ekler); somut örnek istemde.
- **report** ve **verify** script ile üretilir; sayılar HSPICE çıktısından gelir.
