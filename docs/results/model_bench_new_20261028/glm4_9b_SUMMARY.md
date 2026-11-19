# Batch run summary

Date: 2026-10-29 14:05:12 · voting models: glm4:9b, glm4:9b, glm4:9b · candidates N=3 · tolerance 5%

| Topology | Run | Status | Time | Clusters | Winner | Flags |
|---|---|---|---|---|---|---|
| DA | 1 | done | 2288 s | [[1, 2]] | 1 | - |
| DA | 2 | done | 2077 s | [[2]] | 2 | No majority: largest cluster 1/3. |
| DA | 3 | failed | 1918 s | [] | None | No candidate passed the sanity rules. |
| FCO | 1 | done | 1765 s | [[0, 2]] | 0 | - |
| FCO | 2 | done | 1778 s | [[1]] | 1 | No majority: largest cluster 1/3. |
| FCO | 3 | done | 979 s | [[2]] | 2 | No majority: largest cluster 1/3. |
| TSO | 1 | done | 2100 s | [[0]] | 0 | No majority: largest cluster 1/3. |
| TSO | 2 | done | 2421 s | [[0]] | 0 | No majority: largest cluster 1/3. |
| TSO | 3 | done | 1442 s | [[0, 1, 2]] | 0 | - |

## Measurements of the winning candidates

- **DA / run 1**: bw=6.998e+07, cl_bw=6.387e+07, cl_gain=-0.05721, cl_gain_err=0.05721, cmrr=67.84, gain=42.58, gaincm=-25.25, gainpsrr=-72.36, phase_margin=63.64, psrr=72.36, slewrate=2.463e+07, t20=1.001e-06, t80=1.006e-06, tsettle=1.004e-08, tsettle_abs=1.01e-06, vfin=0.6978, vos=-0.001605, vos_drift=3.368, vos_max=-0.001406, vos_min=-0.001962, zpower=0.0001614
  - candidate 0 (glm4:9b): testbenches completed from script drafts=['ac_loop', 'cmrr', 'psrr', 'tran_slew', 'cl_gain', 'offset', 'vos_temp', 'power_area'], measurements completed=['tran_slew', 'cl_gain', 'offset', 'vos_temp', 'power_area', 'ac_loop', 'cmrr', 'psrr', 'tran_slew', 'cl_gain', 'offset', 'vos_temp', 'power_area'], tests that fell back to the draft=[]
  - candidate 1 (glm4:9b): testbenches completed from script drafts=['cmrr', 'psrr', 'tran_slew', 'cl_gain', 'offset', 'vos_temp', 'power_area'], measurements completed=['psrr', 'tran_slew', 'cl_gain', 'offset', 'vos_temp', 'power_area'], tests that fell back to the draft=['ac_loop']
  - candidate 2 (glm4:9b): testbenches completed from script drafts=['ac_loop', 'cmrr', 'psrr', 'tran_slew', 'cl_gain', 'offset', 'vos_temp', 'power_area'], measurements completed=['psrr', 'tran_slew', 'cl_gain', 'offset', 'vos_temp', 'power_area', 'ac_loop', 'cmrr', 'psrr', 'tran_slew', 'cl_gain', 'offset', 'vos_temp', 'power_area', 'ac_loop', 'cmrr', 'psrr', 'tran_slew', 'cl_gain', 'offset', 'vos_temp', 'power_area', 'cl_gain'], tests that fell back to the draft=[]
- **DA / run 2**: bw=6.998e+07, cl_bw=6.387e+07, cl_gain=-0.05721, cl_gain_err=0.05721, cmrr=67.84, gain=42.58, gaincm=-25.25, gainpsrr=-72.36, phase_margin=63.64, psrr=72.36, slewrate=2.463e+07, t20=1.001e-06, t80=1.006e-06, tsettle_abs=1.01e-06, vfin=0.6978, vos=-0.001605, vos_drift=3.368, vos_max=-0.001406, vos_min=-0.001962, zpower=0.0001614
  - candidate 0 (glm4:9b): testbenches completed from script drafts=['ac_loop', 'cmrr', 'psrr', 'tran_slew', 'cl_gain', 'offset', 'vos_temp', 'power_area'], measurements completed=[], tests that fell back to the draft=[]
  - candidate 1 (glm4:9b): testbenches completed from script drafts=['ac_loop', 'cmrr', 'psrr', 'tran_slew', 'cl_gain', 'offset', 'vos_temp', 'power_area'], measurements completed=['tran_slew', 'cl_gain', 'offset', 'vos_temp', 'power_area'], tests that fell back to the draft=[]
  - candidate 2 (glm4:9b): testbenches completed from script drafts=['cmrr', 'psrr', 'tran_slew', 'cl_gain', 'offset', 'vos_temp', 'power_area'], measurements completed=['cl_gain', 'offset', 'vos_temp', 'power_area'], tests that fell back to the draft=['ac_loop']
- **DA / run 3**: no winner. candidate failed: Stage 'measure' did not produce valid output in 3 attempts.; candidate failed: Stage 'stimulus' did not produce valid output in 3 attempts.; candidate failed: Stage 'stimulus' did no
- **FCO / run 1**: bw=6.812e+06, cl_bw=7.259e+06, cl_gain=-0.006797, cl_gain_err=0.006797, cmrr=51.6, gain=29.71, gaincm=-21.89, gainpsrr=-43.78, phase_margin=90.89, psrr=43.78, slewrate=3.43e+06, t20=1.009e-06, t80=1.044e-06, tsettle=1.008e-07, tsettle_abs=1.101e-06, vfin=0.09145, vos=-0.007929, vos_drift=24.98, vos_max=-0.006218, vos_min=-0.01034, zpower=7.645e-05
  - candidate 0 (glm4:9b): testbenches completed from script drafts=['cmrr', 'psrr', 'tran_slew', 'cl_gain', 'offset', 'vos_temp', 'power_area'], measurements completed=[], tests that fell back to the draft=['ac_loop', 'tran_slew']
  - candidate 1 (glm4:9b): testbenches completed from script drafts=['ac_loop', 'cmrr', 'psrr', 'tran_slew', 'cl_gain', 'offset', 'vos_temp', 'power_area'], measurements completed=['offset', 'vos_temp', 'power_area', 'ac_loop', 'cmrr', 'psrr', 'tran_slew', 'cl_gain', 'offset', 'vos_temp', 'power_area', 'ac_loop', 'cmrr', 'psrr', 'tran_slew', 'cl_gain', 'offset', 'vos_temp', 'power_area'], tests that fell back to the draft=[]
  - candidate 2 (glm4:9b): testbenches completed from script drafts=['cmrr', 'psrr', 'tran_slew', 'cl_gain', 'offset', 'vos_temp', 'power_area'], measurements completed=['cl_gain', 'offset', 'vos_temp', 'power_area', 'ac_loop', 'cmrr', 'psrr', 'tran_slew', 'cl_gain', 'offset', 'vos_temp', 'power_area'], tests that fell back to the draft=['ac_loop']
- **FCO / run 2**: bw=6.812e+06, cl_bw=7.259e+06, cl_gain=-0.006797, cl_gain_err=0.006797, cmrr=51.6, gain=29.71, gaincm=-21.89, gainpsrr=-43.78, phase_margin=90.89, psrr=43.78, slewrate=3.43e+06, t20=1.009e-06, t80=1.044e-06, tsettle=1.008e-07, tsettle_abs=1.101e-06, vfin=0.09145, vos=-0.007929, vos_drift=24.98, vos_max=-0.006218, vos_min=-0.01034, zpower=7.645e-05
  - candidate 1 (glm4:9b): testbenches completed from script drafts=['cmrr', 'psrr', 'tran_slew', 'cl_gain', 'offset', 'vos_temp', 'power_area'], measurements completed=[], tests that fell back to the draft=['ac_loop', 'tran_slew']
  - candidate 2 (glm4:9b): testbenches completed from script drafts=['cmrr', 'psrr', 'tran_slew', 'cl_gain', 'offset', 'vos_temp', 'power_area'], measurements completed=['vos_temp', 'power_area'], tests that fell back to the draft=[]
- **FCO / run 3**: bw=6.812e+06, cl_bw=7.259e+06, cl_gain=-0.006797, cl_gain_err=0.006797, cmrr=51.6, gain=29.71, gaincm=-21.89, gainpsrr=-43.78, phase_margin=90.89, psrr=43.78, slewrate=3.43e+06, t20=1.009e-06, t80=1.044e-06, tsettle=1.008e-07, tsettle_abs=1.101e-06, vfin=0.09145, vos=-0.007929, vos_max=-0.006218, zpower=7.645e-05
  - candidate 0 (glm4:9b): testbenches completed from script drafts=['ac_loop', 'cmrr', 'psrr', 'tran_slew', 'cl_gain', 'offset', 'vos_temp', 'power_area', 'ac_loop', 'cmrr', 'psrr', 'tran_slew', 'cl_gain', 'offset', 'vos_temp', 'power_area', 'ac_loop', 'cmrr', 'psrr', 'tran_slew', 'cl_gain', 'offset', 'vos_temp', 'power_area'], measurements completed=[], tests that fell back to the draft=[]
  - candidate 2 (glm4:9b): testbenches completed from script drafts=['cmrr', 'psrr', 'tran_slew', 'cl_gain', 'offset', 'vos_temp', 'power_area'], measurements completed=['power_area', 'power_area'], tests that fell back to the draft=['ac_loop']
- **TSO / run 1**: bw=9.203e+06, cl_bw=1.066e+07, cl_gain=0.0942, cl_gain_err=0.0942, cmrr=43.08, gain=43.22, gaincm=0.1428, gainpsrr=-41.87, phase_margin=87.11, psrr=41.87, slewrate=5.498e+06, t20=1.005e-06, t80=1.027e-06, tsettle=8.533e-08, tsettle_abs=1.085e-06, vfin=0.7019, vos=0.000899, vos_drift=11.6, vos_max=0.001904, vos_min=-1.025e-05, zpower=0.0001721
  - candidate 0 (glm4:9b): testbenches completed from script drafts=['cmrr', 'psrr', 'tran_slew', 'cl_gain', 'offset', 'vos_temp', 'power_area'], measurements completed=[], tests that fell back to the draft=['tran_slew']
  - candidate 1 (glm4:9b): testbenches completed from script drafts=['ac_loop', 'cmrr', 'psrr', 'tran_slew', 'cl_gain', 'offset', 'vos_temp', 'power_area'], measurements completed=['cl_gain', 'offset', 'vos_temp', 'power_area'], tests that fell back to the draft=[]
- **TSO / run 2**: bw=9.203e+06, cl_bw=1.066e+07, cl_gain=0.0942, cl_gain_err=0.0942, cmrr=43.08, gain=43.22, gaincm=0.1428, gainpsrr=-41.87, phase_margin=87.11, psrr=41.87, slewrate=5.498e+06, t20=1.005e-06, t80=1.027e-06, tsettle=8.533e-08, tsettle_abs=1.085e-06, vfin=0.7019, vos=0.000899, vos_drift=11.6, vos_max=0.001904, vos_min=-1.025e-05, zpower=0.0001721
  - candidate 0 (glm4:9b): testbenches completed from script drafts=['cmrr', 'psrr', 'tran_slew', 'cl_gain', 'offset', 'vos_temp', 'power_area'], measurements completed=[], tests that fell back to the draft=['tran_slew']
  - candidate 1 (glm4:9b): testbenches completed from script drafts=['ac_loop', 'cmrr', 'psrr', 'tran_slew', 'cl_gain', 'offset', 'vos_temp', 'power_area'], measurements completed=['tran_slew', 'cl_gain', 'offset', 'vos_temp', 'power_area', 'ac_loop', 'cmrr', 'psrr', 'tran_slew', 'cl_gain', 'offset', 'vos_temp', 'power_area'], tests that fell back to the draft=[]
- **TSO / run 3**: bw=9.203e+06, cl_bw=1.066e+07, cl_gain=0.0942, cl_gain_err=0.0942, cmrr=43.08, gain=43.22, gaincm=0.1428, gainpsrr=-41.87, phase_margin=87.11, psrr=41.87, slewrate=5.498e+06, t20=1.005e-06, t80=1.027e-06, tsettle=8.533e-08, tsettle_abs=1.085e-06, vfin=0.7019, vos=0.000899, vos_drift=11.6, vos_max=0.001904, vos_min=-1.025e-05, zpower=0.0001721
  - candidate 0 (glm4:9b): testbenches completed from script drafts=['cmrr', 'psrr', 'tran_slew', 'cl_gain', 'offset', 'vos_temp', 'power_area'], measurements completed=[], tests that fell back to the draft=['tran_slew']
  - candidate 1 (glm4:9b): testbenches completed from script drafts=['cmrr', 'psrr', 'tran_slew', 'cl_gain', 'offset', 'vos_temp', 'power_area'], measurements completed=[], tests that fell back to the draft=['tran_slew']
  - candidate 2 (glm4:9b): testbenches completed from script drafts=['ac_loop', 'cmrr', 'psrr', 'tran_slew', 'cl_gain', 'offset', 'vos_temp', 'power_area', 'cmrr', 'psrr', 'tran_slew', 'cl_gain', 'offset', 'vos_temp', 'power_area'], measurements completed=['vos_temp', 'power_area', 'ac_loop', 'cmrr', 'psrr', 'tran_slew', 'cl_gain', 'offset', 'vos_temp', 'power_area'], tests that fell back to the draft=['ac_loop']

## Specification checks

- DA/1: ✓ Input offset: |vos| = 1.6 mV (limit 10 mV)
- DA/1: ✓ Closed-loop gain error: 0.0572 dB (limit 1 dB)
- DA/2: ✓ Input offset: |vos| = 1.6 mV (limit 10 mV)
- DA/2: ✓ Closed-loop gain error: 0.0572 dB (limit 1 dB)
- FCO/1: ✓ Input offset: |vos| = 7.93 mV (limit 10 mV)
- FCO/1: ✓ Closed-loop gain error: 0.0068 dB (limit 1 dB)
- FCO/2: ✓ Input offset: |vos| = 7.93 mV (limit 10 mV)
- FCO/2: ✓ Closed-loop gain error: 0.0068 dB (limit 1 dB)
- FCO/3: ✓ Input offset: |vos| = 7.93 mV (limit 10 mV)
- FCO/3: ✓ Closed-loop gain error: 0.0068 dB (limit 1 dB)
- TSO/1: ✓ Input offset: |vos| = 0.899 mV (limit 10 mV)
- TSO/1: ✓ Closed-loop gain error: 0.0942 dB (limit 1 dB)
- TSO/2: ✓ Input offset: |vos| = 0.899 mV (limit 10 mV)
- TSO/2: ✓ Closed-loop gain error: 0.0942 dB (limit 1 dB)
- TSO/3: ✓ Input offset: |vos| = 0.899 mV (limit 10 mV)
- TSO/3: ✓ Closed-loop gain error: 0.0942 dB (limit 1 dB)

## Skipped topologies

- **COMP**: comparator.sp is a flat netlist (no .subckt). Pipeline v0 instantiates the circuit as a subcircuit; a .subckt wrapper is needed first.
- **OSC**: cmos_osc.sp is a flat netlist (no .subckt) and uses harmonic-balance (HB) analysis, which v0 does not support.