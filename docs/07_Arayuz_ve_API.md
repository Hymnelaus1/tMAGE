---
tags: [tmage, arayuz]
---
# Arayüz ve API

Yerel web arayüzü, tek dosya (`app/static/index.html`, bağımlılıksız JS) + Python `http.server` (`app/server.py`). Başlatma: `~/tmage/run.sh` → `http://127.0.0.1:8765`. Başka PC'den: `TMAGE_HOST=0.0.0.0 ./run.sh` (yalnızca Tailscale/yerel ağ).

## Bölümler
1. **Devre:** dosya gezgini (USB `tb/inputs` kısayolu) ya da yapıştırma; `.subckt`, port, `.param`, mevcut analizler çıkarılır; teknoloji uyumsuzsa uyarlama bandı.
2. **Topoloji:** DA, FCO, TSO, BGR, COMP, OSC, LNA, özel. Dosya adı/subckt'ten tahmin.
3. **Teknoloji:** SAED90 / SKY130 / 130 nm, simülatör, VDD, PDK yolu, sıcaklıklar, köşeler.
4. **Analizler:** katalogdaki 16 analiz, topolojiye göre varsayılan işaretli, parametreleri düzenlenir.
5. **LLM:** Ollama (Jetson, modeller canlı listelenir), OpenAI uyumlu; her ajana ayrı model.
Sağ panel: özet, eksik uyarıları, kaydet, son işler, **koşu paneli** (canlı log, aşama durumu, rapor).

## API
| Uç | İş |
|---|---|
| `GET /api/config` | Katalog + ortam |
| `GET /api/fs`, `/api/file` | Dosya gezgini (yalnızca ev, `/run/media`, `/data`, `/opt/synopsys`) |
| `POST /api/parse`, `/api/adapt` | Netlist çözümleme, teknolojiye uyarlama |
| `GET /api/models?url=` | Ollama model listesi (yalnızca özel/Tailscale adresleri: SSRF koruması) |
| `GET/POST /api/state` | Arayüz durumu (`config/ui_state.json`) |
| `POST /api/jobs`, `GET /api/jobs` | İş kaydı/listesi |
| `POST /api/run/start`, `GET /api/run/log` | Koşu başlat, log izle |

## Güvenlik notları
Varsayılan olarak yalnızca `127.0.0.1`. Dosya erişimi izin verilen köklerle sınırlı; dosya okuma yalnızca metin uzantıları, ≤2 MB.

## Test yöntemi
Başsız Firefox ile ekran görüntüsü: `MOZ_HEADLESS=1 firefox --no-remote --profile <geçici> --screenshot out.png URL` (asenkron yükleme için geçici bir gecikme kancası gerekir).
