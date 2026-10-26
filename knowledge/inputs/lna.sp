***lna netlist

.subckt lna in out vdd

m1 2 2 0 0  nfet l=L1 w=W1
m2 7 vdd 6 0  nfet l=L2 w=W2
m3 6 4 5 0  nfet l=L3 w=W3
X1 3 4 vdd gnd l_cr20k_rf do=do_l_1 w=wo_l_1 s=1.5u nt=3.5 afr=5e+9 d=500n tm=8 
X2 vdd 7 vdd gnd l_cr20k_rf do=do_l_2 w=wo_l_2 s=1.5u nt=3.5 afr=5e+9 d=500n tm=8 
X3 5 0 vdd gnd l_cr20k_rf do=do_l_3 w=wo_l_3 s=1.5u nt=3.5 afr=5e+9 d=500n tm=8 
Rb1 vdd 2 Rb
Rb2 2 3 Rb_2
Cxx in 3 10n
Cyy 7 out 10n
.ends lna
 
*R3 102 2 1
*.IC V(3)=0.6
.option post
*.option HBTOL=1e-6
.op
.option OPTFILE
.INC 130nm.txt
.INC param_lna.cir
.inc inductor.txt
.AC dec 1 1000 100000000000
.TRAN 1n 100n
*.PROBE tran V(2,3)
*.PRINT tran V(2,3)
*.probe tran I(M4) 
*.print tran I(M4)

.MEAS zPOWER AVG POWER
**** test bench
.LIN noisecalc=1
Pout outs gnd port=2 RDC=50 RAC=50 DC=0 AC=1 0
Pin ins gnd port=1 RDC=50 RAC=50 DC=0.5 AC=0.5 0
Vdd vdd1 gnd DC 3.3
xlna2 ins outs vdd1 lna



*.HBOSC tones= 5000Meg NHARMS=5 PROBENODE=2,3
*.nf v(out) dec 1 1k 100G 
*+listfreq=(all) 
*+listsources=on 
*+spurious=1

.probe nf
.print nf
.PROBE AC S11(DB)
.PRINT AC S11(DB)
.PROBE AC S21(DB)
.PRINT AC S21(DB)
.PROBE AC S12(DB)
.PRINT AC S12(DB)

*.MEASURE AC nfr find nf at 2.4G
.MEAS AC nf find '10*log10(nf)' at 5.5G
.MEASURE S11 find S11(DB) at 5.5G
.MEASURE S12 find S12(DB) at 5.5G
.MEASURE S21 find S21(DB) at 5.5G


*.probe  phasenoise phnoise V(2,3)
*.print  phasenoise phnoise V(2,3)
*.measure phasenoise freq find 'HERTZ[1]' at=5n
*.MEAS AC RPOWER AVG POWER


.END