---
tags: [tmage, saed90, adaptation]
---
# Adapting 130 nm / SKY130 to SAED 90 nm

The analyses in the kit were written for 130 nm. **The analysis and measurement commands (`.ac .tran .noise .dc .meas`) do not depend on the technology**; what changes is model names, the library line, the supply scheme, corners and sizes.

## SAED90nm (read from the PDK)
- Model file: `hspice/SAED90nm.lib`; corner sections `TT_12 FF_12 SS_12 FS_12 SF_12` (LVT/HVT: `*_12_LVT/HVT`).
- Devices: `n12`, `p12` (+ `_lvt`, `_hvt`); BJTs `VPNP`, `LPNP`.
- Core supply **1.2 V, single supply** (the 130 nm kit used a +/-1.2 V dual supply).
- The `BJT_12` library comes ready **only inside `TT_12`**; in other corners it is added separately (important for the bandgap).
- Usage: `.lib '<pdk>/hspice/SAED90nm.lib' TT_12`, transistor `M1 d g s b n12 w=... l=...`.

## Automatic adaptation (`server.py: adapt_netlist`)
1. Detects the source technology (`NFET/PFET` means gtu130, `sky130_fd_pr__*` means sky130).
2. Maps model names (`NFET` to `n12`, `PFET` to `p12`, `pnp_05v5_...` to `VPNP`).
3. Removes the old `.inc` model lines and adds a single `.lib` line.
4. Converts SKY130 subcircuit calls (`XM1`) to direct MOSFETs (`M1`) in SAED90.
5. Adds `BJT_12` when a BJT exists in a corner other than TT.
6. Produces a report: what was done and the **warnings** (supply scheme difference, Lmin difference, sizes belonging to the old technology).

The UI shows a warning band in section 1; the original is kept and there is a *Revert to original* button.

## Limits
- W/L and `param_*.cir` values are not adapted (sizing is out of scope). The DA still worked with the old values ([[12_Smoke_Test_Results]]).
- Supply source lines must be reviewed by hand.
- Pipeline v0 runs only SAED90.
