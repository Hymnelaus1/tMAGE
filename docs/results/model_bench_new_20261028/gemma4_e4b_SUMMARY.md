# Batch run summary

Date: 2026-10-29 06:30:10 · voting models: gemma4:e4b, gemma4:e4b, gemma4:e4b · candidates N=3 · tolerance 5%

| Topology | Run | Status | Time | Clusters | Winner | Flags |
|---|---|---|---|---|---|---|
| DA | 1 | done | 703 s | [[0]] | 0 | No majority: largest cluster 1/3. |
| DA | 2 | done | 592 s | [[0]] | 0 | No majority: largest cluster 1/3. |
| DA | 3 | done | 525 s | [[0], [2]] | 0 | No majority: largest cluster 1/3. |
| FCO | 1 | failed | 490 s | [] | None | No candidate passed the sanity rules. |
| FCO | 2 | failed | 481 s | [] | None | No candidate passed the sanity rules. |
| FCO | 3 | done | 468 s | [[1]] | 1 | No majority: largest cluster 1/3. |
| TSO | 1 | failed | 366 s | [] | None | No candidate passed the sanity rules. |
| TSO | 2 | failed | 739 s | [] | None | No candidate passed the sanity rules. |
| TSO | 3 | failed | 856 s | [] | None | No candidate passed the sanity rules. |

## Measurements of the winning candidates

- **DA / run 1**: bw_3db=6.998e+07, cl_gain=-0.05721, cmrr=67.84, gain=42.58, gaincm=-25.25, gainpsrr=-72.36, gbw=6.998e+07, phase_margin=63.64, psrr=72.36, slewrate=2.463e+07, t20=1.001e-06, t80=1.006e-06, tsettle=1.004e-08, tsettle_abs=1.01e-06, vfin=0.6978, vos=-0.001605, vos_drift=3.368, vos_max=-0.001406, vos_min=-0.001962, zpower=0.0001614
  - candidate 0 (gemma4:e4b): testbenches completed from script drafts=['cl_gain', 'offset', 'vos_temp', 'power_area'], measurements completed=['offset', 'vos_temp', 'power_area'], tests that fell back to the draft=[]
  - candidate 1 (gemma4:e4b): testbenches completed from script drafts=['cl_gain', 'offset', 'vos_temp', 'power_area'], measurements completed=[], tests that fell back to the draft=[]
  - candidate 2 (gemma4:e4b): testbenches completed from script drafts=['cl_gain', 'offset', 'vos_temp', 'power_area'], measurements completed=[], tests that fell back to the draft=[]
- **DA / run 2**: bw_3db=6.998e+07, cl_bw=6.387e+07, cl_gain=-0.05721, cl_gain_err=0.05721, cmrr=67.84, gain=42.58, gaincm=-25.25, gainpsrr=-72.36, gbw=6.998e+07, phase_margin=63.64, psrr=72.36, slewrate=2.463e+07, t20=1.001e-06, t80=1.006e-06, tsettle=1.004e-08, tsettle_abs=1.01e-06, vfin=0.6978, vos=-0.001605, vos_drift=3.368, vos_max=-0.001406, vos_min=-0.001962, zpower=0.0001614
  - candidate 0 (gemma4:e4b): testbenches completed from script drafts=['cl_gain', 'offset', 'vos_temp', 'power_area'], measurements completed=['offset', 'vos_temp', 'power_area'], tests that fell back to the draft=['cl_gain']
  - candidate 1 (gemma4:e4b): testbenches completed from script drafts=['cl_gain', 'offset', 'vos_temp', 'power_area'], measurements completed=[], tests that fell back to the draft=[]
  - candidate 2 (gemma4:e4b): testbenches completed from script drafts=['cl_gain', 'offset', 'vos_temp', 'power_area'], measurements completed=[], tests that fell back to the draft=[]
- **DA / run 3**: bw_3db=6.998e+07, cl_bw=6.387e+07, cl_gain=-0.05721, cl_gain_err=0.05721, cmrr=67.84, gain=42.58, gaincm=-25.25, gainpsrr=-72.36, gbw=6.998e+07, phase_margin=63.64, psrr=72.36, slewrate=2.463e+07, t20=1.001e-06, t80=1.006e-06, tsettle=1.004e-08, tsettle_abs=1.01e-06, vfin=0.6978, vos=-0.001605, vos_drift=3.368, vos_max=-0.001406, vos_min=-0.001962, zpower=0.0001614
  - candidate 0 (gemma4:e4b): testbenches completed from script drafts=['cl_gain', 'offset', 'vos_temp', 'power_area'], measurements completed=['offset', 'vos_temp', 'power_area'], tests that fell back to the draft=['cl_gain']
  - candidate 1 (gemma4:e4b): testbenches completed from script drafts=['cl_gain', 'offset', 'vos_temp', 'power_area'], measurements completed=[], tests that fell back to the draft=[]
  - candidate 2 (gemma4:e4b): testbenches completed from script drafts=['cl_gain', 'offset', 'vos_temp', 'power_area'], measurements completed=['offset', 'vos_temp'], tests that fell back to the draft=['cl_gain']
- **FCO / run 1**: no winner. candidate failed: Stage 'measure' did not produce valid output in 3 attempts.; candidate failed: Stage 'measure' did not produce valid output in 3 attempts.; candidate failed: Stage 'measure' did not 
- **FCO / run 2**: no winner. candidate failed: Stage 'measure' did not produce valid output in 3 attempts.; candidate failed: Stage 'measure' did not produce valid output in 3 attempts.; candidate failed: Stage 'measure' did not 
- **FCO / run 3**: bw_3db=6.812e+06, cl_bw=7.259e+06, cl_gain=-0.006797, cl_gain_err=0.006797, cmrr=51.6, gain=29.71, gaincm=-21.89, gainpsrr=-43.78, gbw=6.812e+06, phase_margin=90.89, psrr=43.78, slewrate=3.43e+06, t20=1.009e-06, t80=1.044e-06, tsettle=1.008e-07, tsettle_abs=1.101e-06, vfin=0.09145, vos=-0.007929, vos_drift=24.98, vos_max=-0.006218, vos_min=-0.01034, zpower=7.645e-05
  - candidate 1 (gemma4:e4b): testbenches completed from script drafts=[], measurements completed=['cl_gain', 'offset', 'vos_temp', 'power_area'], tests that fell back to the draft=['tran_slew']
- **TSO / run 1**: no winner. candidate failed: Stage 'stimulus' did not produce valid output in 3 attempts.; candidate failed: Stage 'stimulus' did not produce valid output in 3 attempts.; candidate failed: Stage 'measure' did no
- **TSO / run 2**: no winner. candidate failed: Stage 'measure' did not produce valid output in 3 attempts.; candidate failed: Stage 'measure' did not produce valid output in 3 attempts.; candidate failed: Stage 'measure' did not 
- **TSO / run 3**: no winner. candidate failed: Stage 'measure' did not produce valid output in 3 attempts.; cl_gain_1: no measurement statements; cl_gain_10: no measurement statements; candidate failed: Stage 'measure' did not pr

## Specification checks

- DA/1: ✓ Input offset: |vos| = 1.6 mV (limit 10 mV)
- DA/2: ✓ Input offset: |vos| = 1.6 mV (limit 10 mV)
- DA/2: ✓ Closed-loop gain error: 0.0572 dB (limit 1 dB)
- DA/3: ✓ Input offset: |vos| = 1.6 mV (limit 10 mV)
- DA/3: ✓ Closed-loop gain error: 0.0572 dB (limit 1 dB)
- FCO/3: ✓ Input offset: |vos| = 7.93 mV (limit 10 mV)
- FCO/3: ✓ Closed-loop gain error: 0.0068 dB (limit 1 dB)

## Skipped topologies

- **COMP**: comparator.sp is a flat netlist (no .subckt). Pipeline v0 instantiates the circuit as a subcircuit; a .subckt wrapper is needed first.
- **OSC**: cmos_osc.sp is a flat netlist (no .subckt) and uses harmonic-balance (HB) analysis, which v0 does not support.