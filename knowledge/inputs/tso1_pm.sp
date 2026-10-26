**aaaa

.param Lcm=0.5e-6

***Input Diff. Pair
m1 7  9  2  2  pfet l=Lcm w=WM1 ad=Lcm*WM1 as=Lcm*WM1 pd=2*(Lcm+WM1) ps=2*(Lcm+WM1) 
m2 5  10 2  2  pfet l=Lcm w=WM1 ad=Lcm*WM1 as=Lcm*WM1 pd=2*(Lcm+WM1) ps=2*(Lcm+WM1) 

****Active Load 1st Stage
m3 7  7  13 13 nfet l=Lcm w=WM6 ad=Lcm*WM6 as=Lcm*WM6 pd=2*(Lcm+WM6) ps=2*(Lcm+WM6)  
m4 5  7  13 13 nfet l=Lcm w=WM6 ad=Lcm*WM6 as=Lcm*WM6 pd=2*(Lcm+WM6) ps=2*(Lcm+WM6) 

****Output Stage
m6 4 5 13 13 nfet l=Lcm w=WM7 ad=Lcm*WM7 as=Lcm*WM7 pd=2*(Lcm+WM7) ps=2*(Lcm+WM7)

**** Input Stage Bias MOS
m5 2  3  1  1  pfet l=Lcm w=WM2 ad=Lcm*WM2 as=Lcm*WM2 pd=2*(Lcm+WM2) ps=2*(Lcm+WM2)  
**** Output Stage Bias MOS
m7 4  3  1  1  pfet l=Lcm w=WM3 ad=Lcm*WM3 as=Lcm*WM3 pd=2*(Lcm+WM3) ps=2*(Lcm+WM3) 

**** Input Stage Bias Mirror MOS
m8 3  3  1  1  pfet l=Lcm w=WM4 ad=Lcm*WM4 as=Lcm*WM4 pd=2*(Lcm+WM4) ps=2*(Lcm+WM4)   

******Biasing Part******
m13 3 8 15 15 nfet l=Lcm w=WM11 ad=Lcm*WM11 as=Lcm*WM11 pd=2*(Lcm+WM11) ps=2*(Lcm+WM11)
m14 8 8 14 14 nfet l=Lcm w=WM11 ad=Lcm*WM11 as=Lcm*WM11 pd=2*(Lcm+WM11) ps=2*(Lcm+WM11)
m15 15 15 13 13 nfet l=Lcm w=WM11 ad=Lcm*WM11 as=Lcm*WM11 pd=2*(Lcm+WM11) ps=2*(Lcm+WM11)
m16 14 15 13 13 nfet l=Lcm w=WM11 ad=Lcm*WM11 as=Lcm*WM11 pd=2*(Lcm+WM11) ps=2*(Lcm+WM11)

****Bias REsistor***
Rb 1 8 Rbias
***Ccomp****
Cc 5 31 Ccomp
Rc 31 4 Rcomp


******* Gain Measurment****


*****Cload********
cl 4 0 0.5e-12

******Power Supply
Vdd 1 0 DC 0.75
Vss 0 13 DC 0.75

******Inputs
vnin 9 0 dc 0
vin 10 0 dc 0 ac 1
*vpwl 10 0 PWL(100u 0.745 500u 0.755)

******feedback
*E1 444 0 4 0 1
*L1 444 9 1000
*Cx 9 0 1000


.option post = 1
.op
.INC 130nm.txt
.INC param1_pm.cir
.PARAM AREA='2*WM1*Lcm + WM2*Lcm + WM3*Lcm + WM4*Lcm + 2*WM6*Lcm +WM7*Lcm + 4*WM11*Lcm'
VX 1000 0 AREA
RX 1000 0 1K
*.option fast
*.option post
.option sim_mode = client/server
.option OPFILE=1


.ac dec 100 100 100000000000
.TRAN 2n 700u 

.MEAS AC gain max PAR('db(V(4))')
*.MEAS AC tmp max par('gain-3')
.MEAS AC BW when par('db(V(4))')= 0      
.MEASURE AC hreal FIND VR(4) WHEN V(4)=1
.MEASURE AC himg  FIND VI(4) WHEN V(4)=1  
.MEAS zPOWER AVG POWER 
.MEAS zSAREA avg PAR(AREA)

*.MEAS TRAN zzztemp FIND v(10) WHEN v(4)=0.75V rise=1
*.MEAS TRAN zzztemps FIND V(10) WHEN v(10)=0.75V 
*.MEAS TRAN offset max par('abs(zzztemp)-0.75')
*.MEASURE TRAN tdlay TRIG V(10) VAL =0.75 TD =10n
*+ TARG V(4) VAL =0.75 rise=1

.END
