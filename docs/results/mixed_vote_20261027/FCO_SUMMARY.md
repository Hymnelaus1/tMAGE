# Batch run summary

Date: 2026-10-27 17:51:26 · voting models: qwen3:4b-instruct, command-r7b:latest, deepseek-coder:6.7b · candidates N=3 · tolerance 5%

| Topology | Run | Status | Time | Clusters | Winner | Flags |
|---|---|---|---|---|---|---|
| FCO | 1 | done | 1546 s | [[0, 1]] | 0 | - |
| FCO | 2 | done | 1282 s | [[0, 1, 2]] | 0 | - |
| FCO | 3 | done | 858 s | [[0, 1]] | 0 | - |

## Measurements of the winning candidates

- **FCO / run 1**: bw=6.812e+06, cl_bw=7.259e+06, cl_gain=-0.006797, cl_gain_err=0.006797, cmrr=51.6, gain=29.71, gaincm=-21.89, gainpsrr=-43.78, phase_margin=90.89, psrr=43.78, slewrate=3.43e+06, t20=1.009e-06, t80=1.044e-06, tsettle=1.008e-07, tsettle_abs=1.101e-06, vfin=0.09145, vos=-0.007929, vos_drift=24.98, vos_max=-0.006218, vos_min=-0.01034, zpower=7.645e-05
  - candidate 0 (qwen3:4b-instruct): testbenches completed from script drafts=[], measurements completed=['tran_slew'], tests that fell back to the draft=[]
  - candidate 1 (command-r7b:latest): testbenches completed from script drafts=[], measurements completed=['psrr', 'tran_slew', 'cl_gain', 'offset', 'vos_temp', 'power_area'], tests that fell back to the draft=[]
  - candidate 2 (deepseek-coder:6.7b): testbenches completed from script drafts=[], measurements completed=['power_area', 'ac_loop', 'cmrr', 'psrr', 'tran_slew', 'power_area', 'ac_loop', 'cmrr', 'psrr', 'tran_slew', 'power_area'], tests that fell back to the draft=['ac_loop', 'tran_slew', 'offset']
- **FCO / run 2**: bw=6.812e+06, cl_bw=7.259e+06, cl_gain=-0.006797, cl_gain_err=0.006797, cmrr=51.6, gain=29.71, gaincm=-21.89, gainpsrr=-43.78, phase_margin=90.89, psrr=43.78, slewrate=3.43e+06, t20=1.009e-06, t80=1.044e-06, tsettle=1.008e-07, tsettle_abs=1.101e-06, vfin=0.09145, vos=-0.007929, vos_drift=24.98, vos_max=-0.006218, vos_min=-0.01034, zpower=7.645e-05
  - candidate 0 (qwen3:4b-instruct): testbenches completed from script drafts=[], measurements completed=['tran_slew'], tests that fell back to the draft=['cl_gain']
  - candidate 1 (command-r7b:latest): testbenches completed from script drafts=[], measurements completed=['psrr', 'tran_slew', 'cl_gain', 'offset', 'vos_temp', 'power_area'], tests that fell back to the draft=[]
  - candidate 2 (deepseek-coder:6.7b): testbenches completed from script drafts=[], measurements completed=[], tests that fell back to the draft=['ac_loop']
- **FCO / run 3**: bw=6.812e+06, cl_bw=7.259e+06, cl_gain=-0.006797, cl_gain_err=0.006797, cmrr=51.6, gain=29.71, gaincm=-21.89, gainpsrr=-43.78, phase_margin=90.89, psrr=43.78, slewrate=3.43e+06, t20=1.009e-06, t80=1.044e-06, tsettle=1.008e-07, tsettle_abs=1.101e-06, vfin=0.09145, vos=-0.007929, vos_drift=24.98, vos_max=-0.006218, vos_min=-0.01034, zpower=7.645e-05
  - candidate 0 (qwen3:4b-instruct): testbenches completed from script drafts=['cmrr', 'psrr', 'tran_slew', 'cl_gain', 'offset', 'vos_temp', 'power_area'], measurements completed=['tran_slew', 'cl_gain'], tests that fell back to the draft=[]
  - candidate 1 (command-r7b:latest): testbenches completed from script drafts=[], measurements completed=['psrr', 'tran_slew', 'cl_gain', 'offset', 'vos_temp', 'power_area'], tests that fell back to the draft=[]

## Specification checks

- FCO/1: ✓ Input offset: |vos| = 7.93 mV (limit 10 mV)
- FCO/1: ✓ Closed-loop gain error: 0.0068 dB (limit 1 dB)
- FCO/2: ✓ Input offset: |vos| = 7.93 mV (limit 10 mV)
- FCO/2: ✓ Closed-loop gain error: 0.0068 dB (limit 1 dB)
- FCO/3: ✓ Input offset: |vos| = 7.93 mV (limit 10 mV)
- FCO/3: ✓ Closed-loop gain error: 0.0068 dB (limit 1 dB)

## Skipped topologies

- **COMP**: comparator.sp is a flat netlist (no .subckt). Pipeline v0 instantiates the circuit as a subcircuit; a .subckt wrapper is needed first.
- **OSC**: cmos_osc.sp is a flat netlist (no .subckt) and uses harmonic-balance (HB) analysis, which v0 does not support.