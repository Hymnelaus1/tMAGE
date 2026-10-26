---
tags: [tmage, synopsys, hspice, setup]
---
# Synopsys installation

Source: the GTU installation kit (USB, `SYNOPSYS_KURULUM/`), version X-2025.06-SP2: CustomCompiler, FineSim, HSPICE, IC Validator, StarRC + the SAED90nm PDK. About 72 GB in total, target `/opt/synopsys/tools`.

## Method
A copy of the kit's `kur.sh` adapted to this machine is `/data/installers/kur_tmage.sh` (paths changed to `/opt/synopsys` and `/data`). Six steps: md5 check, system check, Installer, copy the `.spf` files, product installation, PDK.

## Two problems and their fixes
1. **`SynopsysInstaller_v5.11.run` did not run with bash** (`syntax error near unexpected token '('`). The file is a **Perl script** (`#!/usr/bin/perl`). Fix: in the script use `perl "$KIT/installer/...run"` instead of `bash "$KIT/installer/...run"`.
2. **`Invalid Site ID, Synopsys Tools NOT installed`.** The answer supplied with `yes yes` made the Site ID invalid. The Site ID is written in the kit's guide (`docs/Synopsys_Kullanim_Rehberi.txt`) and is **never written into the repository**. Fix: a `-site_info` file:
```
SiteId      :<number from the guide>
LicenseAdmin:GTU
PhoneOrEmail:<e-mail>
```
```bash
yes yes | /opt/synopsys/installer/installer \
  -source /data/installers/source_tmp -target /opt/synopsys/tools \
  -site_info /data/installers/site_info
```
- The GUI installer (`setup.sh`) is not used: there is no NVIDIA driver and it can crash. Text mode only.

## PDK and environment
```bash
tar -xf pdk/SAED90nm_PDK_10222017.tar -C /opt/synopsys/edk && chmod -R a-w /opt/synopsys/edk/SAED90nm_PDK_10222017
cp /opt/synopsys/edk/SAED90nm_PDK_10222017/install/lib.defs ~/lib.defs
```
`config/env.sh` (example file `env.sh.example`):
```bash
export HSPICE_HOME=/opt/synopsys/tools/hspice/X-2025.06-SP2/hspice
export PATH=$HSPICE_HOME/bin:$PATH
export SNPSLMD_LICENSE_FILE=27200@<license server>
export SAED90_PDK=/opt/synopsys/edk/SAED90nm_PDK_10222017
```
For license access see [[05_VPN_Split_Tunnel]].
