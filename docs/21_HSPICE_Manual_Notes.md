# What was taken from the HSPICE manual

Source: `~/Downloads/hspice_sa.pdf`, *HSPICE User Guide: Simulation and Analysis*, 1024 pages. Text: `knowledge/manual/hspice_sa.txt` (pdftotext). It is **not given to the models**; only the verified rules are passed into the prompts. The manual is Synopsys material and is not in the repository.

**Note:** the manual version is **B-2008.09**, the installed HSPICE is **X-2025.06-SP2**. The rules come from the older version and may have changed in the new one, so every rule must be checked with a small HSPICE run.

## .MEASURE (manual p.317-322), added to the `measure` agent
- A `.meas` binds to the **last analysis card** before it.
- If a measure name clashes with a `.param` name, HSPICE stops with an error.
- The equation form uses only the results of earlier measures; it must not contain node voltages/currents.
- Event selectors: `rise/fall/cross=n` or `last`, delay `td`. `last` is a reserved word.
- A failed measure writes `0.0e0` (FAILED in the listing).
- A measure that uses the result of an earlier measure gives 0 until that result is found.
- `avg/rms/integ` are meaningless in a DC sweep (warning).
- Canonical examples (appendix): gain `max vdb(out)`, ugf `trig at=1 targ vdb(out) val=0 fall=1`, PM `find vp(out) when vdb(out)=0`, slew `trig/targ ... rise=1`, `deriv ... when`.

## Verilog-A (chapter 31, p.760-795), not added to the prompts yet
- A device is an **X element**: `X<name> <nodes> <module> param=value`.
- `.hdl` can be anywhere in the top-level circuit; it **cannot** be inside a `.subckt` or an IF block (error).
- A module with the same name loaded a second time is ignored (a difference only in case does not count either).
- A module name cannot be: AMP, C, CORE, D, L, NJF, NMOS, NPN, OPT, PJF, PLOT, PMOS, PNP, R, U, W, SP (a warning is given and the module is ignored). `amp` in particular is forbidden.
- If a subcircuit has the same name, **the subcircuit wins** by default (changed with `.option vamodel`).
- File search order: the working directory, `-hdlpath`, `HSP_HDL_PATH`.
- Module parameters are device parameters; they cannot be changed directly with `.PARAM`, they are given on the instance line.
