---
tags: [tmage, log]
---
# Change log (first day)

The later sessions are in [[18_Change_Log_Benchmark]].

## 2026-10-25
- Environment: Tailscale, xrdp + xorgxrdp, GNOME `.xsession`, sleep disabled, desktop shortcuts ([[03_Environment_Setup]])
- Synopsys: Installer Perl fix, Site ID with `-site_info`, 5 products + the SAED90 PDK ([[04_Synopsys_Install]])
- VPN: split-tunnel profile, license access verified ([[05_VPN_Split_Tunnel]])
- UI v1: circuit, topology, technology, analysis and LLM selection ([[07_UI_and_API]])
- 90 nm adaptation engine + the COMP/OSC/LNA topologies from the kit ([[06_Technology_Adaptation_90nm]])
- Data hand-off between agents: `context.json`, stage schemas ([[08_Agent_Data_Handoff]])
- Verification decision: voting + rules instead of a judge ([[10_Verification_Voting]])
- HSPICE smoke test: DA, SAED90 TT ([[12_Smoke_Test_Results]])
- Pipeline v0 and logging; the first run was cut short by a VPN drop ([[09_Logging]])
- Benchmark tool added ([[11_Jetson_LLM_Benchmark]])
- These documents and the local git repository were created
- Jetson benchmark run (4B+ models, baseline and improved mode); gpt-oss:20b crashed Ollama ([[16_Report_Jetson_LLM]])
- Improvements: script-first spec/scenario, draft testbench/`.meas`, RAG (`knowledge/`), JSON schema, truncation detection
- UI redesigned (presentation palette, logo, icons); an always-on VPN service with `scripts/vpn.sh` (kept local, not in the repository)
