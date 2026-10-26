***netlist
*.param l1 ='lM1'
*.param l2 ='lM2'
*.param l3 ='lM3'

*.param w1 ='WM1'
*.param w2 ='WM2'
*.param w3 ='WM3'




.temp 27
.options post=1
.param Vdd=2.4
.global gnd
.inc 130nm.txt
.inc param_lna_h.cir
.inc inductor.txt
**
** Cascode LNA tuned for operation near 1 GHz
**
M1 2 2 gnd gnd nfet l=lM1 w=WM1 ad=lM1*WM1 as=lM1*WM1 pd=2*(lM1+WM1) ps=2*(lM1+WM1)
M2 3 1 5 gnd nfet l=lM2 w=WM2 ad=lM2*WM2 as=lM2*WM2 pd=2*(lM2+WM2) ps=2*(lM2+WM2)
M3 5 6 7 gnd nfet l=lM3 w=WM3 ad=lM3*WM3 as=lM3*WM3 pd=2*(lM3+WM3) ps=2*(lM3+WM3)
r1 1 2 R_1
r2 2 6 R_2
X1 6 8 1 gnd l_cr20k_rf do=do_l1 w=wo_l1 s=st_l1 nt=nt_l1 afr=2.4e+9 d=500n tm=8
X2 1 3 1 gnd l_cr20k_rf do=do_l2 w=wo_l2 s=st_l2 nt=nt_l2 afr=2.4e+9 d=500n tm=8
X3 7 gnd 1 gnd l_cr20k_rf do=do_l3 w=wo_l3 s=st_l3 nt=nt_l3 afr=2.4e+9 d=500n tm=8

C1 9 8 1
C3 3 10 1
C2 3 gnd 0.5pF
*RL 3 gnd 50

vvdd 1 gnd dc=Vdd
.tran 1n 1m
.MEAS RPOWER AVG POWER
.param inputP=1u
*P1 9 gnd  port=1 z0=50 hb 'inputP' 0 1 1 hb 'inputP' 0 1 2
P1 9 gnd  port=1 z0=50 power=dBm hb 'inputP' 0 1 1 hb 'inputP' 0 1 2
P2 10 gnd  port=2 z0=50  



.AC DEC 5 100 50G
.LIN noisecalc=1 sparcalc=1
.PRINT S11(DB) S21(DB) S12(DB) S22(DB) NF(DB)
.probe S11(DB) S21(DB) S12(DB) S22(DB) NF(DB)



.op

.meas AC S11 find S11(DB) at=2.4G  
.meas AC S12 find S12(DB) at=2.4G  
.meas AC S21 find S21(DB) at=2.4G  
*.meas AC S22 find S22(DB) at=2.4G
.meas AC znoise find NF(DB) at=2.4G
.END
