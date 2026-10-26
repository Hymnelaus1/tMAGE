---
tags: [tmage, index]
---
# tMAGE: Project Notes

**tMAGE** (testbench Multi-Agent Generation Engine) is a GTU ELM491 graduation project that automates testbench generation for analog circuits with a multi-agent LLM system. This folder is both an Obsidian vault and the repository documentation; every change is recorded together with **how it was done**.

## Reading order
1. [[01_Project_Summary]]: what we are building and why
2. [[02_Architecture]]: parts and flow
3. [[03_Environment_Setup]]: MSI, Tailscale, remote desktop
4. [[04_Synopsys_Install]]: HSPICE and the PDK
5. [[05_VPN_Split_Tunnel]]: access to the license server
6. [[06_Technology_Adaptation_90nm]]: adapting 130 nm netlists to SAED90
7. [[07_UI_and_API]]: the web UI
8. [[08_Agent_Data_Handoff]]: stage schemas
9. [[09_Logging]]
10. [[10_Verification_Voting]]: why voting instead of a judge model
11. [[11_Jetson_LLM_Benchmark]]: choosing a model for each agent
12. [[12_Smoke_Test_Results]]: first HSPICE results
13. [[16_Report_Jetson_LLM]]: model comparison report and improvements

## Operations
- [[13_Troubleshooting]]: errors we met and their fixes
- [[14_To_Do]]
- [[15_Change_Log_Early]]
- [[18_Change_Log_Benchmark]]
- [[20_Observed_Errors]], [[21_HSPICE_Manual_Notes]], [[19_Agent_Prompts]], [[22_Benchmark_Findings]]

## Quick start
```bash
source ~/tmage/config/env.sh        # HSPICE path and license
~/tmage/run.sh                      # UI: http://127.0.0.1:8765
sudo openvpn --config ~/vpn/gtu.ovpn  # for the license (keep it open in a separate terminal)
```
