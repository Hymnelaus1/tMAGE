---
tags: [tmage, proje]
---
# Proje özeti

**Problem:** Her spesifikasyon (kazanç, BW, faz payı, güç, gürültü) ve her PDK köşesi için ayrı testbench kurulur. Yanlış bias ya da yanlış `.meas` ifadesi, devre doğru olsa bile yanıltıcı sonuç verir. Testbench devreye ve PDK'ya özeldir; tasarım değişince baştan yazılır.

**Amaç:** Testbench üretimini PDK'ya duyarlı LLM ajanlarıyla otomatikleştirmek. Kullanıcı kendi devresini verir, topolojiyi seçer; sistem testbench'i üretir, simüle eder, doğrular ve raporlar.

**Kapsam dışı:** Devre boyutlandırma (W/L optimizasyonu).

**Hedef devreler (kolaydan zora):** DA (fark yükselteci), FCO (katlanmış kaskod OTA), TSO (iki katlı opamp), BGR (bandgap). Kitte ayrıca comparator (COMP), CMOS osilatör (OSC) ve LNA örnekleri var; arayüze eklendi.

**Ana teknoloji:** SAED 90 nm (HSPICE). Kitteki referanslar 130 nm; SKY130/ngspice B planıdır.

**LLM altyapısı:** NVIDIA Jetson Orin Nano üzerinde Ollama (yerel, maliyetsiz); bulut modelleri isteğe bağlı.

**Çıktı (her devre için):** testbench, simülasyon sonucu, doğrulama, rapor.

İlgili: [[02_Mimari]]
