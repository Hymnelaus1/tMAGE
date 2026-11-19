# Batch run summary

Date: 2026-10-27 16:41:46 · voting models: qwen3:4b-instruct, command-r7b:latest, deepseek-coder:6.7b · candidates N=3 · tolerance 5%

| Topology | Run | Status | Time | Clusters | Winner | Flags |
|---|---|---|---|---|---|---|
| DA | 1 | done | 1774 s | [[0], [1]] | 0 | No majority: largest cluster 1/3. |
| DA | 2 | done | 1078 s | [[0], [1], [2]] | 0 | No majority: largest cluster 1/3. |
| DA | 3 | done | 1317 s | [[0, 1]] | 0 | - |

## Measurements of the winning candidates

- **DA / run 1**: bw=6.998e+07, cl_bw=6.387e+07, cl_gain=-0.05721, cl_gain_err=0.05721, cmrr=67.84, gain=42.58, gaincm=-25.25, gainpsrr=-72.36, phase_margin=63.64, psrr=72.36, slewrate=2.463e+07, t20=1.001e-06, t80=1.006e-06, vfin=0.6978, vos=-0.001605, vos_drift=3.368, vos_max=-0.001406, vos_min=-0.001962, zpower=0.0001726
  - candidate 0 (qwen3:4b-instruct): testbenches completed from script drafts=[], measurements completed=['cl_gain', 'offset', 'vos_temp', 'power_area'], tests that fell back to the draft=['psrr']
  - candidate 1 (command-r7b:latest): testbenches completed from script drafts=[], measurements completed=['tran_slew', 'cl_gain', 'offset', 'vos_temp', 'power_area'], tests that fell back to the draft=[]
  - candidate 2 (deepseek-coder:6.7b): testbenches completed from script drafts=[], measurements completed=['tran_slew', 'offset', 'vos_temp'], tests that fell back to the draft=[]
- **DA / run 2**: bw=6.998e+07, cl_bw=6.387e+07, cl_gain=-0.05721, cl_gain_err=0.05721, cmrr=67.84, gain=42.58, gaincm=-25.25, gainpsrr=-72.36, phase_margin=63.64, psrr=72.36, slewrate=2.463e+07, t20=1.001e-06, t80=1.006e-06, tsettle=1.004e-08, tsettle_abs=1.01e-06, vfin=0.6978, vos=-0.001605, vos_drift=3.368, vos_max=-0.001406, vos_min=-0.001962, zpower=0.0001726
  - candidate 0 (qwen3:4b-instruct): testbenches completed from script drafts=[], measurements completed=['tran_slew'], tests that fell back to the draft=['psrr', 'cl_gain']
  - candidate 1 (command-r7b:latest): testbenches completed from script drafts=[], measurements completed=['tran_slew', 'cl_gain', 'offset', 'vos_temp', 'power_area'], tests that fell back to the draft=[]
  - candidate 2 (deepseek-coder:6.7b): testbenches completed from script drafts=[], measurements completed=['power_area'], tests that fell back to the draft=['ac_loop', 'cl_gain']
- **DA / run 3**: bw=6.998e+07, cl_bw=6.387e+07, cl_gain=-0.05721, cl_gain_err=0.05721, cmrr=67.84, gain=42.58, gaincm=-25.25, gainpsrr=-72.36, phase_margin=63.64, psrr=72.36, slewrate=2.463e+07, t20=1.001e-06, t80=1.006e-06, tsettle=1.004e-08, tsettle_abs=1.01e-06, vfin=0.6978, vos=-0.001605, vos_drift=3.368, vos_max=-0.001406, vos_min=-0.001962, zpower=0.0001614
  - candidate 0 (qwen3:4b-instruct): testbenches completed from script drafts=[], measurements completed=['tran_slew', 'cl_gain'], tests that fell back to the draft=[]
  - candidate 1 (command-r7b:latest): testbenches completed from script drafts=[], measurements completed=['tran_slew', 'cl_gain', 'offset', 'vos_temp', 'power_area'], tests that fell back to the draft=[]

## Specification checks

- DA/1: ✓ Input offset: |vos| = 1.6 mV (limit 10 mV)
- DA/1: ✓ Closed-loop gain error: 0.0572 dB (limit 1 dB)
- DA/2: ✓ Input offset: |vos| = 1.6 mV (limit 10 mV)
- DA/2: ✓ Closed-loop gain error: 0.0572 dB (limit 1 dB)
- DA/3: ✓ Input offset: |vos| = 1.6 mV (limit 10 mV)
- DA/3: ✓ Closed-loop gain error: 0.0572 dB (limit 1 dB)

## Skipped topologies

- **COMP**: comparator.sp is a flat netlist (no .subckt). Pipeline v0 instantiates the circuit as a subcircuit; a .subckt wrapper is needed first.
- **OSC**: cmos_osc.sp is a flat netlist (no .subckt) and uses harmonic-balance (HB) analysis, which v0 does not support.