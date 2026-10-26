---
tags: [tmage, hspice, results]
---
# Smoke test: DA on SAED90

**Goal:** Check that the tool chain (HSPICE + license + SAED90 + adaptation) works.
**Circuit:** the kit's `amp_llm.sp` (130 nm), adapted by tMAGE, `.lib ... TT_12`. Sizes are taken unchanged from 130 nm.
**License:** `1(in_use)/50(total) FLOATING license(s)`.

| Measurement | SAED90 (TT) | Old 130 nm run (`amp.ma0`) |
|---|---|---|
| Gain | 40.38 dB | 33.83 dB |
| BW (0 dB) | 115 MHz | 30.35 kHz |
| Phase margin | 61.56 deg | n/a |
| CMRR | 103.3 dB | n/a |
| PSRR | 58.86 dB | n/a |
| Power | 0.853 mW | n/a |

## HSPICE warnings
- A +/-1.2 V dual supply is too much for 1.2 V devices (2.4 V). In real runs: single supply, VDD 1.2 V, VSS 0.
- In the PSRR testbench the source `vin3` has no value (HSPICE assumed zero).
- An `Acde` geometry warning on one transistor (W=24.7 um, L=1.0 um); the sizes are not suitable for 90 nm.

**Result:** the tool chain works; the numbers belong to an unsized circuit and are for verification only.
