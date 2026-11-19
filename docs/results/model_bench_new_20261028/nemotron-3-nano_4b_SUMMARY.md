# Batch run summary

Date: 2026-10-29 07:58:01 · voting models: nemotron-3-nano:4b, nemotron-3-nano:4b, nemotron-3-nano:4b · candidates N=3 · tolerance 5%

| Topology | Run | Status | Time | Clusters | Winner | Flags |
|---|---|---|---|---|---|---|
| DA | 1 | failed | 874 s | [] | None | No candidate passed the sanity rules. |
| DA | 2 | failed | 893 s | [] | None | No candidate passed the sanity rules. |
| DA | 3 | done | 767 s | [[1], [2]] | 1 | No majority: largest cluster 1/3. |
| FCO | 1 | failed | 1677 s | [] | None | No candidate passed the sanity rules. |
| FCO | 2 | failed | 981 s | [] | None | No candidate passed the sanity rules. |
| FCO | 3 | failed | 1253 s | [] | None | No candidate passed the sanity rules. |
| TSO | 1 | failed | 660 s | [] | None | No candidate passed the sanity rules. |
| TSO | 2 | done | 789 s | [[1]] | 1 | No majority: largest cluster 1/3. |
| TSO | 3 | failed | 936 s | [] | None | No candidate passed the sanity rules. |

## Measurements of the winning candidates

- **DA / run 1**: no winner. candidate failed: Stage 'measure' did not produce valid output in 3 attempts.; candidate failed: Stage 'measure' did not produce valid output in 3 attempts.; candidate failed: Stage 'stimulus' did not
- **DA / run 2**: no winner. candidate failed: Stage 'measure' did not produce valid output in 3 attempts.; candidate failed: Stage 'measure' did not produce valid output in 3 attempts.; candidate failed: Stage 'measure' did not 
- **DA / run 3**: bw=6.998e+07, cl_bw=6.387e+07, cl_gain=-0.05721, cl_gain_err=0.05721, cmrr=67.84, gain=42.58, gaincm=-25.25, gainpsrr=-72.36, phase_margin=63.64, psrr=72.36, slewrate=2e+08, t20=1e-06, t80=1.001e-06, tsettle=9.9e-10, tsettle_abs=1.001e-06, vfin=0.7, vos=-0.001605, vos_drift=3.368, vos_max=-0.001406, vos_min=-0.001962, zpower=0.0001614
  - candidate 1 (nemotron-3-nano:4b): testbenches completed from script drafts=[], measurements completed=[], tests that fell back to the draft=['ac_loop', 'cmrr', 'psrr', 'cl_gain', 'offset', 'vos_temp']
  - candidate 2 (nemotron-3-nano:4b): testbenches completed from script drafts=[], measurements completed=['vos_temp', 'power_area'], tests that fell back to the draft=['ac_loop', 'cmrr', 'psrr', 'tran_slew', 'cl_gain', 'offset']
- **FCO / run 1**: no winner. cl_vel: no measurement statements; vos_vel: simulation error: **error** (vos_vel.sp:48) string misses dexter quotation mark, error is  before or at "'v(vout)-v(vinp)) at=0"; vos_vel: simulation error:
- **FCO / run 2**: no winner. candidate failed: Stage 'stimulus' did not produce valid output in 3 attempts.; candidate failed: Stage 'stimulus' did not produce valid output in 3 attempts.; candidate failed: Stage 'stimulus' did n
- **FCO / run 3**: no winner. candidate failed: Stage 'stimulus' did not produce valid output in 3 attempts.; candidate failed: Stage 'measure' did not produce valid output in 3 attempts.; candidate failed: Stage 'measure' did not
- **TSO / run 1**: no winner. candidate failed: Stage 'stimulus' did not produce valid output in 3 attempts.; candidate failed: Stage 'measure' did not produce valid output in 3 attempts.; candidate failed: Stage 'stimulus' did no
- **TSO / run 2**: bw=9.203e+06, cl_bw=1.066e+07, cl_gain=0.0942, cl_gain_err=0.0942, cmrr=43.08, gain=43.22, gaincm=0.1428, gainpsrr=-41.87, phase_margin=87.11, psrr=41.87, slewrate=2e+08, t20=1e-06, t80=1.001e-06, tsettle=9.9e-10, tsettle_abs=1.001e-06, vfin=0.7, vos=0.000899, vos_drift=11.6, vos_max=0.001904, vos_min=-1.025e-05, zpower=0.0001721
  - candidate 0 (nemotron-3-nano:4b): testbenches completed from script drafts=['ac_loop', 'cl_gain', 'offset', 'vos_temp', 'power_area'], measurements completed=[], tests that fell back to the draft=[]
  - candidate 1 (nemotron-3-nano:4b): testbenches completed from script drafts=[], measurements completed=[], tests that fell back to the draft=['ac_loop', 'cmrr', 'psrr', 'cl_gain', 'offset', 'vos_temp']
  - candidate 2 (nemotron-3-nano:4b): testbenches completed from script drafts=['ac_loop', 'cmrr', 'psrr', 'tran_slew', 'cl_gain', 'offset', 'vos_temp', 'power_area'], measurements completed=['tran_slew', 'cl_gain', 'vos_temp', 'power_area', 'ac_loop', 'cmrr', 'psrr', 'tran_slew', 'cl_gain', 'offset', 'vos_temp', 'power_area'], tests that fell back to the draft=[]
- **TSO / run 3**: no winner. candidate failed: Stage 'measure' did not produce valid output in 3 attempts.; candidate failed: Stage 'measure' did not produce valid output in 3 attempts.; ac_phase_margin: no measurement produced (

## Specification checks

- DA/3: ✓ Input offset: |vos| = 1.6 mV (limit 10 mV)
- DA/3: ✓ Closed-loop gain error: 0.0572 dB (limit 1 dB)
- TSO/2: ✓ Input offset: |vos| = 0.899 mV (limit 10 mV)
- TSO/2: ✓ Closed-loop gain error: 0.0942 dB (limit 1 dB)

## Skipped topologies

- **COMP**: comparator.sp is a flat netlist (no .subckt). Pipeline v0 instantiates the circuit as a subcircuit; a .subckt wrapper is needed first.
- **OSC**: cmos_osc.sp is a flat netlist (no .subckt) and uses harmonic-balance (HB) analysis, which v0 does not support.