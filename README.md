# tMAGE

Analog devreler için **çok ajanlı testbench üretim motoru** (GTÜ ELM491 bitirme projesi). Kullanıcı devresini ve topolojisini seçer; sistem LLM ajanlarıyla testbench üretir, HSPICE ile simüle eder, doğrular ve raporlar.

Ayrıntılı belgeler ve **nasıl yapıldığı** notları: [`docs/`](docs/00_Ana_Sayfa.md) (Obsidian kasası olarak da açılır: Obsidian → *Open folder as vault* → `docs/`).

## Hızlı başlangıç
```bash
cp config/env.sh.example config/env.sh          # lisans ve yolları doldur
cp config/jetson.env.example config/jetson.env   # Ollama (Jetson) adresi
./run.sh                                         # arayüz: http://127.0.0.1:8765
```
Gereksinimler: Python 3.9 (yalnızca standart kütüphane), HSPICE X-2025.06-SP2 + SAED90nm PDK, VPN (lisans için), Ollama sunucusu.

## Yapı
`app/` web arayüzü · `engine/` boru hattı, loglama, benchmark · `config/` katalog ve şemalar · `docs/` belgeler · `runs/` koşu çıktıları (depoya girmez)

## Gizlilik
`.ovpn` dosyaları, `env.sh`, `jetson.env`, koşu çıktıları ve loglar `.gitignore` ile dışarıda tutulur. Lisans/Site ID bilgileri depoya yazılmaz. Depoyu uzağa itecekseniz **özel (private)** tutun.
