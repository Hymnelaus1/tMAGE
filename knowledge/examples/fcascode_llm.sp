**Folded Cascode
.inc 130nm.txt
.inc param_fco.cir
.param Lcmd=0.24e-06


.subckt fco vinp vinn vout vdd vss

m1 3 vinp 6 6  nfet l=LM1 w=WM1 ad=Lcmd*WM1 as=Lcmd*WM1 pd=(Lcmd+WM1) ps=(Lcmd+WM1)  	
m2 4 vinn 6 6 nfet l=LM1 w=WM1 ad=Lcmd*WM1 as=Lcmd*WM1 pd=(Lcmd+WM1) ps=(Lcmd+WM1) 

m3 5 5 vss vss nfet l=LM2 w=WM2 ad=Lcmd*WM2 as=Lcmd*WM2 pd=(Lcmd+WM2) ps=(Lcmd+WM2)
m4 6 5 vss vss nfet l=LM2 w=WM2 ad=Lcmd*WM2 as=Lcmd*WM2 pd=(Lcmd+WM2) ps=(Lcmd+WM2)

m5 10 outn vss vss  nfet l=LM3 w=WM3 ad=Lcmd*WM3 as=Lcmd*WM3 pd=(Lcmd+WM3) ps=(Lcmd+WM3) 
m6 12 outn vss vss  nfet l=LM3 w=WM3 ad=Lcmd*WM3 as=Lcmd*WM3 pd=(Lcmd+WM3) ps=(Lcmd+WM3) 

m7 outn 8 10 10 nfet l=LM4 w=WM4 ad=Lcmd*WM4 as=Lcmd*WM4 pd=(Lcmd+WM4) ps=(Lcmd+WM4)  
m8 vout 8 12 12 nfet l=LM4 w=WM4 ad=Lcmd*WM4 as=Lcmd*WM4 pd=(Lcmd+WM4) ps=(Lcmd+WM4) 


m9 3 2 vdd vdd pfet l=LM5 w=WM5 ad=Lcmd*WM5 as=Lcmd*WM5 pd=(Lcmd+WM5) ps=(Lcmd+WM5)  
m10 4 2 vdd vdd pfet l=LM5 w=WM5 ad=Lcmd*WM5 as=Lcmd*WM5 pd=(Lcmd+WM5) ps=(Lcmd+WM5) 

m11 2 2 vdd vdd pfet l=LM6 w=WM6 ad=Lcmd*WM6 as=Lcmd*WM6 pd=(Lcmd+WM6) ps=(Lcmd+WM6)
m12 13 2 vdd vdd pfet l=LM6 w=WM6 ad=Lcmd*WM6 as=Lcmd*WM6 pd=(Lcmd+WM6) ps=(Lcmd+WM6) 

m13 5 14 2 2 pfet l=LM7 w=WM7 ad=Lcmd*WM7 as=Lcmd*WM7 pd=(Lcmd+WM7) ps=(Lcmd+WM7) 
m14 14 14 13 13 pfet l=LM7 w=WM7 ad=Lcmd*WM7 as=Lcmd*WM7 pd=(Lcmd+WM7) ps=(Lcmd+WM7) 

m15 outn 7 3 3 pfet l=LM8 w=WM8 ad=Lcmd*WM8 as=Lcmd*WM8 pd=(Lcmd+WM8) ps=(Lcmd+WM8)
m16 vout 7 4 4 pfet l=LM8 w=WM8 ad=Lcmd*WM8 as=Lcmd*WM8 pd=(Lcmd+WM8) ps=(Lcmd+WM8) 

R1 14 vss Rb

Vcm1 7 GND Vcm1
Vcm2 8 GND Vcm2

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

X0 vpin vnin vout aVDD1 aVSS1 fco
cl vout GND 0.5e-12


**** PSRR testbench  
Vdd3 aVDD3 GND DC pVDD AC 1
Vss3 aVSS3 GND DC pVSS

vin3 vpin3 GND

X3 vpin3 vout3 vout3 aVDD3 aVSS3 fco
cl3 vout3 GND 0.5e-12

**** Common-mode
Vdd5 aVDD5 GND DC pVDD
Vss5 aVSS5 GND DC pVSS

vin5 vpin5 GND dc 0 ac 0.5
vinn5 vnin5 GND dc 0 ac 0.5

X5 vpin5 vnin5 vout5 aVDD5 aVSS5 fco
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