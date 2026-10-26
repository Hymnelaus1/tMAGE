**Folded Cascode



m1 3 inp 6 6  nfet l=LM1 w=WM1 ad=LM1 * WM1 as=LM1 * WM1 pd=2*(LM1 + WM1) ps=2*(LM1 + WM1)  	
m2 4 inn 6 6 nfet l=LM1 w=WM1 ad=LM1 * WM1 as=LM1 * WM1 pd=2*(LM1 + WM1) ps=2*(LM1 + WM1) 

m3 5 5 vss vss nfet l=LM2 w=WM2 ad=LM2 * WM2 as=LM2 * WM2 pd=2*(LM2 + WM2) ps=2*(LM2 + WM2)
m4 6 5 vss vss nfet l=LM2 w=WM2 ad=LM2 * WM2 as=LM2 * WM2 pd=2*(LM2 + WM2) ps=2*(LM2 + WM2)

m5 10 outn vss vss  nfet l=LM3 w=WM3 ad=LM3 * WM3 as=LM3 * WM3 pd=2*(LM3 + WM3) ps=2*(LM3 + WM3)  
m6 12 outn vss vss  nfet l=LM3 w=WM3 ad=LM3 * WM3 as=LM3 * WM3 pd=2*(LM3 + WM3) ps=2*(LM3 + WM3)  

m7 outn 8 10 10 nfet l=LM4 w=WM4 ad=LM4 * WM4 as=LM4 * WM4 pd=2*(LM4 + WM4) ps=2*(LM4 + WM4)  
m8 outp 8 12 12 nfet l=LM4 w=WM4 ad=LM4 * WM4 as=LM4 * WM4 pd=2*(LM4 + WM4) ps=2*(LM4 + WM4)  


m9 3 2 vdd vdd pfet l=LM5 w=WM5 ad=LM5 * WM5 as=LM5 * WM5 pd=2*(LM5 + WM5) ps=2*(LM5 + WM5)  
m10 4 2 vdd vdd pfet l=LM5 w=WM5 ad=LM5 * WM5 as=LM5 * WM5 pd=2*(LM5 + WM5) ps=2*(LM5 + WM5)  

m11 2 2 vdd vdd pfet l=LM6 w=WM6 ad=LM6 * WM6 as=LM6 * WM6 pd=2*(LM6 + WM6) ps=2*(LM6 + WM6)  
m12 13 2 vdd vdd pfet l=LM6 w=WM6 ad=LM6 * WM6 as=LM6 * WM6 pd=2*(LM6 + WM6) ps=2*(LM6 + WM6)  

m13 5 14 2 2 pfet l=LM7 w=WM7 ad=LM7 * WM7 as=LM7 * WM7 pd=2*(LM7 + WM7) ps=2*(LM7 + WM7)  
m14 14 14 13 13 pfet l=LM7 w=WM7 ad=LM7 * WM7 as=LM7 * WM7 pd=2*(LM7 + WM7) ps=2*(LM7 + WM7)  

m15 outn 7 3 3 pfet l=LM8 w=WM8 ad=LM8 * WM8 as=LM8 * WM8 pd=2*(LM8 + WM8) ps=2*(LM8 + WM8) 
m16 outp 7 4 4 pfet l=LM8 w=WM8 ad=LM8 * WM8 as=LM8 * WM8 pd=2*(LM8 + WM8) ps=2*(LM8 + WM8) 

R1 14 vss Rb

Vcm1 7 GND Vcm1
Vcm2 8 GND Vcm2

CL outp GND 0.5e-12

******Power Supply
Vdd vdd 0 DC 1.2
Vss 0 vss DC 1.2

******Inputs
vnin inn 0 dc 0
vin inp 0 dc 0 ac 1
*vpwl 10 0 PWL(100u 0.745 500u 0.755)

******feedback
*E1 444 0 4 0 1
*L1 444 9 1000
*Cx 9 0 1000

.option post = 1
.op
.INC 130nm.txt
.INC param_folded_pm2.cir
.PARAM AREA='2*WM1*LM1 + 2*WM2*LM2 + 2*WM3*LM3 + 2*WM4*LM4 + 2*WM5*LM5 + 2*WM6*LM6+ 2*WM7*LM7 + 2*WM8*LM8' * area of the Folded Cascode opamp
VX 1000 0 AREA
RX 1000 0 1K
*.option fast
*.option post
.option sim_mode = client/server
.option OPFILE=1

.ac dec 100 100 100000000000
.TRAN 2n 700u 

.MEAS AC gain max PAR('db(V(outp))')
*.MEAS AC tmp max par('gain-3')
.MEAS AC BW when par('db(V(outp))')= 0      
.MEASURE AC hreal FIND VR(outp) WHEN V(outp)=1
.MEASURE AC himg  FIND VI(outp) WHEN V(outp)=1  
.MEAS zPOWER AVG POWER 
.MEAS zSAREA avg PAR(AREA)


.END