---
tags: [tmage, log]
---
# Loglama

`engine/log.py`. Her koşunun `logs/` klasörü:

| Dosya | İçerik |
|---|---|
| `run.log` | İnsan okuyabilir günlük (zaman, seviye, mesaj) |
| `events.jsonl` | Aynı olaylar, yapılandırılmış (süre, model, token, ölçümler) |
| `llm/NNN_aşama.json` | Her LLM çağrısının **tam** istek/yanıtı, süre, token, hata listesi |
| `sim/aday_test.txt` | Her HSPICE ekran çıktısı |
| `status.json` | `running/done/failed`, aşama, süre, pid |

Genel olaylar (iş kaydı, koşu başlatma): `~/tmage/logs/tmage.log`.

## Nasıl okunur
```bash
tail -f runs/<id>/logs/run.log
jq . runs/<id>/logs/llm/003_stimulus_c0_a1.json | less
```
Arayüzde koşu paneli aynı günlüğü canlı gösterir.

## Önlemler
- Koşu başlamadan ve her HSPICE'tan önce lisans portu denenir; VPN yoksa net mesajla durur (`LicenseError`), model suçlanmaz.
- `Unable to checkout` HSPICE çıktısında bulunursa lisans hatası sayılır.
- Süreç numarası kaydedilir; yarım kalan koşu "çalışıyor" görünüp yenisini engellemez.
