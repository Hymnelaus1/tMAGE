**aaaa


.inc 130nm.txt
.inc param_tso.cir
.param Lcmd=0.24e-06

.subckt tso vinp vinn vout vdd vss

***Input Diff. Pair
m1 7  vinn  2  2  pfet l=LM1 w=WM1 ad=Lcmd*WM1 as=Lcmd*WM1 pd=(Lcmd+WM1) ps=(Lcmd+WM1) 
m2 5  vinp 2  2  pfet l=LM1 w=WM1 ad=Lcmd*WM1 as=Lcmd*WM1 pd=(Lcmd+WM1) ps=(Lcmd+WM1) 

****Active Load 1st Stage
m3 7  7  vss vss nfet l=LM3 w=WM3 ad=Lcmd*WM3 as=Lcmd*WM3 pd=(Lcmd+WM3) ps=(Lcmd+WM3)  
m4 5  7  vss vss nfet l=LM3 w=WM3 ad=Lcmd*WM3 as=Lcmd*WM3 pd=(Lcmd+WM3) ps=(Lcmd+WM3) 

****Output Stage
m6 vout 5 vss vss nfet l=LM4 w=WM4 ad=Lcmd*WM4 as=Lcmd*WM4 pd=(Lcmd+WM4) ps=(Lcmd+WM4)

**** Input Stage Bias MOS
m5 2  3  vdd  vdd  pfet l=LM2 w=WM2 ad=Lcmd*WM2 as=Lcmd*WM2 pd=(Lcmd+WM2) ps=(Lcmd+WM2)  
**** Output Stage Bias MOS
m7 vout  3  vdd  vdd  pfet l=LM5 w=WM5 ad=Lcmd*WM5 as=Lcmd*WM5 pd=(Lcmd+WM5) ps=(Lcmd+WM5) 

**** Input Stage Bias Mirror MOS
m8 3  3  vdd  vdd  pfet l=LM2 w=WM2 ad=Lcmd*WM2 as=Lcmd*WM2 pd=(Lcmd+WM2) ps=(Lcmd+WM2)   


****Bias Resistor***
Rb 3 vss Rbias
***Ccomp****
Cc 5 vout Ccomp

.ends


******Power Supply
.PARAM pVDD=1.2
.PARAM pVSS=-1.2


* E1 444 0 vout 0 1
* L1 444 vnin 1000
* Cx vnin 0 1000


***** Open-loop Gain, Bandwidth, Phase Margin testbench
Vdd1 aVDD1 GND DC pVDD
Vss1 aVSS1 GND DC pVSS

vin vpin GND dc 0 ac 0.5
vinn GND vnin dc 0 ac 0.5

X0 vpin vnin vout aVDD1 aVSS1 tso
cl vout GND 0.5e-12


**** PSRR testbench  
Vdd3 aVDD3 GND DC pVDD AC 1
Vss3 aVSS3 GND DC pVSS

vin3 vpin3 GND

X3 vpin3 vout3 vout3 aVDD3 aVSS3 tso
cl3 vout3 GND 0.5e-12

**** Common-mode
Vdd5 aVDD5 GND DC pVDD
Vss5 aVSS5 GND DC pVSS

vin5 vpin5 GND dc 0 ac 0.5
vinn5 vnin5 GND dc 0 ac 0.5

X5 vpin5 vnin5 vout5 aVDD5 aVSS5 tso
cl5 vout5 GND 0.5e-12


* **** Slewrate testbench
* Vdd2 aVDD2 GND DC pVDD
* Vss2 aVSS2 GND DC pVSS
* Vin2 inp2 GND pulse(pVSS pVDD 1m 0 0 1m 0)

* X2 inp2 vout2 vout2 aVDD2 aVSS2 tso



********Simulation Options
.ac dec 1000 10 7G 
.tran 2n 0.5m


* .OPTION LISNEW=1
.OPTION post=1
.OPTION MEASFORM=1
.OPTION NOMOD=1
.OPTION MEASFAIL=0
.OPTION UNWRAP


************************** AC Analysis **************************
* .probe OP v(vout) print=1
.MEAS AC gain find PAR('db(V(vout))') at=1000
.MEAS AC gainVV find PAR('db(V(vout))') at=1000 print=0

* .MEAS AC BW_3dB when par('db(V(vout))') = 'gain-3'
.MEAS AC bw when par('db(V(vout))') = 0
.MEAS zPOWER rms p(X0)
.MEASURE AC hreal FIND VR(vout) WHEN V(vout)=1 
.MEASURE AC himg  FIND VI(vout) WHEN V(vout)=1
.measure ac phase_margin find par('180+vp(vout)') at=BW
* .MEAS AC zSAREA avg PAR(area)

* *** CMRR
.MEAS AC gainCM find PAR('db(V(vout5))') at=1000 print=0
.MEAS AC cmrr PARAM='gainVV-gainCM' 

* ** PSRR
.MEAS AC gainVVpsrr find PAR('(V(vout))') at=1MEG print=0
.MEAS AC gainPSRR find PAR('db(V(vout3))') at=1000 print=0
.MEAS AC psrr PARAM='-1*(gainPSRR)' 

************************* **Transient Analysis **************************

*** Slew Rate

* .MEAS TRAN v4_neg FIND V(vout2) at=1m print=0
* .MEAS TRAN v4_pos FIND V(vout2) at=16m print=0
* .MEAS TRAN perc PARAM='(v4_pos-v4_neg)*0.2' print=0

* .MEASURE TRAN tdlay2 TRIG V(vout2) VAL ='v4_neg+perc' TD =1n
* + TARG V(vout2) VAL ='v4_pos-perc' rise=1

* .MEAS TRAN slewrate PARAM='((v4_pos-perc)-(v4_neg+perc))/tdlay2'

.end