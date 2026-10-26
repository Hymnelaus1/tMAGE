***netlist

m1 3 2 1 1  pfet l=L1 w=W1
m2 2 3 1 1  pfet l=L1 w=W1
m3 3 2 4 6  nfet l=L2 w=W2
m4 2 3 4 6  nfet l=L2 w=W2
m5 4 5 6 6  nfet l=L3 w=W3
m6 5 5 6 6 nfet l=L3 w=W3
Ib 1 5 Ib

X2 3 2 mimcaps_mml130e l=cap_l w=cap_w m=1
X1 3 2 1 gnd l_cr20k_rf do=do_l w=wo_l s=s_l nt=nt_l afr=5e+9 d=500n tm=8 

Cxx 2 0 1p
Cyy 3 0 1p

*R3 102 2 1
.IC V(3)=0.6
Vdd 1 gnd DC 1.2
Vss gnd 6 DC 1.2
.option post
*.option HBTOL=1e-6
*.op
.INC 130nm.txt
.INC param.cir
.inc inductor.txt
.inc mimcap.txt
.TRAN 1n 10n
.PROBE tran V(2,3)
.PRINT tran V(2,3)
.probe tran I(M4) 
.print tran I(M4)


.HBOSC tones= 5000Meg NHARMS=5 PROBENODE=2,3,1.2 
.phasenoise v(2,3) dec 100 100k 10Meg 
+listfreq=(all) 
+listsources=on 
+spurious=1


.probe  phasenoise phnoise V(2,3)
.print  phasenoise phnoise V(2,3)
.measure phasenoise freq find 'HERTZ[1]' at=5n
*.measure phasenoise freq2 find 'HERTZ[1]' at=5n
.MEASURE phasenoise pnoise FIND PHNOISE at=1Meg
*.MEASURE phasenoise pnoise2 FIND PHNOISE at=1Meg
.MEAS  RPOWER AVG POWER 
*.MEAS V23 max V(2,3)
.MEAS TRAN v30 max V(2,3) FROM='3n' TO='4n'
.MEAS TRAN v70 max V(2,3) FROM='7n' TO='8n'
.END