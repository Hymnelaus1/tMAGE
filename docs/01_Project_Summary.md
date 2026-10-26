---
tags: [tmage, project]
---
# Project summary

**Problem:** A separate testbench is built for every specification (gain, bandwidth, phase margin, power, noise) and every PDK corner. A wrong bias or a wrong `.meas` statement gives misleading results even when the circuit is correct. A testbench is specific to the circuit and the PDK, so it is rewritten from scratch whenever the design changes.

**Goal:** Automate testbench generation with PDK-aware LLM agents. The user provides their circuit and picks a topology; the system generates the testbench, simulates it, verifies it and writes a report.

**Out of scope:** Circuit sizing (W/L optimisation).

**Target circuits (easy to hard):** DA (differential amplifier), FCO (folded-cascode OTA), TSO (two-stage op-amp), BGR (bandgap). The kit also has a comparator (COMP), a CMOS oscillator (OSC) and an LNA; they were added to the UI.

**Main technology:** SAED 90 nm (HSPICE). The kit references are 130 nm; SKY130/ngspice is the fallback plan.

**LLM infrastructure:** Ollama on an NVIDIA Jetson Orin Nano (local, free); cloud models are optional.

**Output (for each circuit):** testbench, simulation result, verification, report.

Related: [[02_Architecture]]
