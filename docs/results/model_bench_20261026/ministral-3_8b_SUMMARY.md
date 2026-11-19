# Batch run summary

Date: 2026-10-27 05:35:46 · voting models: ministral-3:8b, ministral-3:8b, ministral-3:8b · candidates N=3 · tolerance 5%

| Topology | Run | Status | Time | Clusters | Winner | Flags |
|---|---|---|---|---|---|---|
| DA | 1 | done | 2074 s | [[0], [1]] | 0 | No majority: largest cluster 1/3. |
| DA | 2 | running | - s | None | None | - |
| DA | 3 | done | 2636 s | [[0, 1], [2]] | 0 | - |
| FCO | 1 | done | 1022 s | [[1]] | 1 | No majority: largest cluster 1/3. |
| FCO | 2 | done | 1432 s | [[2]] | 2 | No majority: largest cluster 1/3. |
| FCO | 3 | done | 1894 s | [[0], [1]] | 0 | No majority: largest cluster 1/3. |
| TSO | 1 | done | 2178 s | [[0], [1]] | 0 | No majority: largest cluster 1/3. |
| TSO | 2 | running | - s | None | None | - |
| TSO | 3 | running | - s | None | None | - |

## Measurements of the winning candidates

- **DA / run 1**: bw=6.998e+07, cl_bw=6.387e+07, cl_gain=-0.05721, cmrr=120.3, gain=42.58, gaincm=-77.69, gainpsrr=-72.36, phase_margin=63.64, slewrate=2.463e+07, t20=1.001e-06, t80=1.006e-06, tsettle=1.004e-08, tsettle_abs=1.01e-06, vfin=0.6978, vos=-0.001605, vos_drift=3.368, vos_max=-0.001406, vos_min=-0.001962, zpower=0.0001615
  - candidate 0 (ministral-3:8b): testbenches completed from script drafts=[], measurements completed=['vos_temp'], tests that fell back to the draft=['ac_loop', 'tran_slew']
  - candidate 1 (ministral-3:8b): testbenches completed from script drafts=[], measurements completed=['vos_temp'], tests that fell back to the draft=['ac_loop', 'tran_slew', 'offset']
- **DA / run 2**: no winner. 
- **DA / run 3**: bw=6.998e+07, cl_bw=6.969e+07, cl_gain=0.3048, cl_gain_err=0.3048, cmrr=136.8, gain=42.58, gaincm=-94.19, gainpsrr=-72.36, phase_margin=63.64, psrr=72.36, slewrate=2.463e+07, t20=1.001e-06, t80=1.006e-06, tsettle=1.004e-08, tsettle_abs=1.01e-06, vfin=0.6978, vos=-0.001605, vos_drift=3.368, vos_max=-0.001406, vos_min=-0.001962, zpower=0.0001726
  - candidate 0 (ministral-3:8b): testbenches completed from script drafts=[], measurements completed=[], tests that fell back to the draft=['ac_loop', 'tran_slew']
  - candidate 1 (ministral-3:8b): testbenches completed from script drafts=[], measurements completed=[], tests that fell back to the draft=['ac_loop', 'tran_slew']
  - candidate 2 (ministral-3:8b): testbenches completed from script drafts=[], measurements completed=[], tests that fell back to the draft=['ac_loop', 'psrr', 'tran_slew', 'cl_gain', 'offset', 'vos_temp', 'power_area']
- **FCO / run 1**: bw=6.812e+06, cl_bw=1, cl_gain=25, cmrr=4.712, gain=29.71, gaincm=25, gainpsrr=25, phase_margin=90.89, psrr=1, slewrate=3.43e+06, t20=1.009e-06, t80=1.044e-06, tsettle=1.008e-07, tsettle_abs=1.101e-06, vfin=0.09145, vos=-0.007929, vos_drift=24.98, vos_max=-0.006218, vos_min=-0.01034, zpower=7.645e-05
  - candidate 0 (ministral-3:8b): testbenches completed from script drafts=['psrr', 'tran_slew', 'cl_gain', 'offset', 'vos_temp', 'power_area', 'psrr', 'tran_slew', 'cl_gain', 'offset', 'vos_temp', 'power_area'], measurements completed=[], tests that fell back to the draft=[]
  - candidate 1 (ministral-3:8b): testbenches completed from script drafts=['psrr', 'tran_slew', 'cl_gain', 'offset', 'vos_temp', 'power_area'], measurements completed=[], tests that fell back to the draft=['ac_loop', 'tran_slew']
  - candidate 2 (ministral-3:8b): testbenches completed from script drafts=['psrr', 'tran_slew', 'cl_gain', 'offset', 'vos_temp', 'power_area', 'psrr', 'tran_slew', 'cl_gain', 'offset', 'vos_temp', 'power_area'], measurements completed=[], tests that fell back to the draft=[]
- **FCO / run 2**: bw=6.812e+06, cl_bw=7.259e+06, cl_gain=-0.006797, cl_gain_err=0.006797, cmrr=4.712, gain=29.71, gaincm=25, gainpsrr=-43.78, phase_margin=90.89, psrr=43.78, slewrate=3.43e+06, t20=1.009e-06, t80=1.044e-06, tsettle=1.008e-07, tsettle_abs=1.101e-06, vfin=0.09145, vos=-0.007929, vos_max=-0.006218, vos_min=-0.01034, zpower=7.645e-05
  - candidate 0 (ministral-3:8b): testbenches completed from script drafts=['psrr', 'tran_slew', 'cl_gain', 'offset', 'vos_temp', 'power_area', 'psrr', 'tran_slew', 'cl_gain', 'offset', 'vos_temp', 'power_area'], measurements completed=[], tests that fell back to the draft=[]
  - candidate 1 (ministral-3:8b): testbenches completed from script drafts=['psrr', 'tran_slew', 'cl_gain', 'offset', 'vos_temp', 'power_area', 'psrr', 'tran_slew', 'cl_gain', 'offset', 'vos_temp', 'power_area'], measurements completed=[], tests that fell back to the draft=[]
  - candidate 2 (ministral-3:8b): testbenches completed from script drafts=['psrr', 'tran_slew', 'cl_gain', 'offset', 'vos_temp', 'power_area'], measurements completed=['power_area'], tests that fell back to the draft=['ac_loop', 'tran_slew', 'offset']
- **FCO / run 3**: bw=6.812e+06, cl_bw=1, cl_gain=25, cmrr=4.712, gain=29.71, gaincm=25, gainpsrr=25, phase_margin=90.89, slewrate=3.43e+06, t20=1.009e-06, t80=1.044e-06, tsettle=1.008e-07, tsettle_abs=1.101e-06, vfin=0.09145, vos=-0.007929, vos_max=-0.006218, vos_min=-0.01034, zpower=7.645e-05
  - candidate 0 (ministral-3:8b): testbenches completed from script drafts=['psrr', 'tran_slew', 'cl_gain', 'offset', 'vos_temp', 'power_area'], measurements completed=['power_area'], tests that fell back to the draft=['ac_loop', 'tran_slew', 'offset']
  - candidate 1 (ministral-3:8b): testbenches completed from script drafts=['psrr', 'tran_slew', 'cl_gain', 'offset', 'vos_temp', 'power_area'], measurements completed=['ac_loop', 'tran_slew', 'cl_gain', 'offset', 'vos_temp', 'power_area'], tests that fell back to the draft=['cl_gain']
  - candidate 2 (ministral-3:8b): testbenches completed from script drafts=['tran_slew', 'cl_gain', 'offset', 'vos_temp', 'power_area', 'tran_slew', 'cl_gain', 'offset', 'vos_temp', 'power_area'], measurements completed=[], tests that fell back to the draft=[]
- **TSO / run 1**: bw=9.203e+06, cl_gain=25, cmrr=18.22, gain=43.22, gaincm=25, gainpsrr=25, phase_margin=87.11, slewrate=5.498e+06, t20=1.005e-06, t80=1.027e-06, tsettle=8.533e-08, tsettle_abs=1.085e-06, vfin=0.7019, vos=0.000899, vos_max=0.001786, vos_min=-1.025e-05, zpower=0.0001721
  - candidate 0 (ministral-3:8b): testbenches completed from script drafts=['power_area'], measurements completed=[], tests that fell back to the draft=['ac_loop', 'tran_slew']
  - candidate 1 (ministral-3:8b): testbenches completed from script drafts=['power_area'], measurements completed=['vos_temp'], tests that fell back to the draft=['ac_loop', 'tran_slew', 'offset']
  - candidate 2 (ministral-3:8b): testbenches completed from script drafts=['power_area', 'power_area'], measurements completed=[], tests that fell back to the draft=[]
- **TSO / run 2**: no winner. candidate failed: Stage 'stimulus' did not produce valid output in 3 attempts.
- **TSO / run 3**: no winner. 

## Specification checks

- DA/1: ✓ Input offset: |vos| = 1.6 mV (limit 10 mV)
- DA/3: ✓ Input offset: |vos| = 1.6 mV (limit 10 mV)
- DA/3: ✓ Closed-loop gain error: 0.305 dB (limit 1 dB)
- FCO/1: ✓ Input offset: |vos| = 7.93 mV (limit 10 mV)
- FCO/2: ✓ Input offset: |vos| = 7.93 mV (limit 10 mV)
- FCO/2: ✓ Closed-loop gain error: 0.0068 dB (limit 1 dB)
- FCO/3: ✓ Input offset: |vos| = 7.93 mV (limit 10 mV)
- TSO/1: ✓ Input offset: |vos| = 0.899 mV (limit 10 mV)

## Skipped topologies

- **COMP**: comparator.sp is a flat netlist (no .subckt). Pipeline v0 instantiates the circuit as a subcircuit; a .subckt wrapper is needed first.
- **OSC**: cmos_osc.sp is a flat netlist (no .subckt) and uses harmonic-balance (HB) analysis, which v0 does not support.