**aaaa


***Input Diff. Pair
m1 7  9  2  2  pfet l=LM1 w=WM1 ad=LM1*WM1 as=LM1*WM1 pd=(LM1+WM1) ps=(LM1+WM1) 
m2 5  10 2  2  pfet l=LM1 w=WM1 ad=LM1*WM1 as=LM1*WM1 pd=(LM1+WM1) ps=(LM1+WM1) 

****Active Load 1st Stage
m3 7  7  13 13 nfet l=LM3 w=WM3 ad=LM3*WM3 as=LM3*WM3 pd=(LM3+WM3) ps=(LM3+WM3)  
m4 5  7  13 13 nfet l=LM3 w=WM3 ad=LM3*WM3 as=LM3*WM3 pd=(LM3+WM3) ps=(LM3+WM3) 

****Output Stage
m6 4 5 13 13 nfet l=LM4 w=WM4 ad=LM4*WM4 as=LM4*WM4 pd=(LM4+WM4) ps=(LM4+WM4)

**** Input Stage Bias MOS
m5 2  3  1  1  pfet l=LM2 w=WM2 ad=LM2*WM2 as=LM2*WM2 pd=(LM2+WM2) ps=(LM2+WM2)  
**** Output Stage Bias MOS
m7 4  3  1  1  pfet l=LM5 w=WM5 ad=LM5*WM5 as=LM5*WM5 pd=(LM5+WM5) ps=(LM5+WM5) 

**** Input Stage Bias Mirror MOS
m8 3  3  1  1  pfet l=LM2 w=WM2 ad=LM2*WM2 as=LM2*WM2 pd=(LM2+WM2) ps=(LM2+WM2)   


****Bias REsistor***
Rb 3 13 Rbias
***Ccomp****
Cc 5 4 Ccomp
*Rc 31 4 Rcomp


******* Gain Measurment****


*****Cload********
cl 4 0 0.5e-12

******Power Supply
Vdd 1 0 DC 1.2
Vss 0 13 DC 0

******Inputs
vnin 9 0 dc Vb
vin 10 0 dc Vb ac 1
*vpwl 10 0 PWL(100u 0.745 500u 0.755)

******feedback
*E1 444 0 4 0 1
*L1 444 9 1000
*Cx 9 0 1000


.option post = 1
.op
.INC 130nm.txt
.INC param2_pm.cir
*.PARAM AREA='2*WM1*Lcm + WM2*Lcm + WM3*Lcm + WM4*Lcm + 2*WM6*Lcm +WM7*Lcm + 4*WM11*Lcm'
*VX 1000 0 AREA
*RX 1000 0 1K
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
*.MEAS zSAREA avg PAR(AREA)

*.MEAS TRAN zzztemp FIND v(10) WHEN v(4)=0.75V rise=1
*.MEAS TRAN zzztemps FIND V(10) WHEN v(10)=0.75V 
*.MEAS TRAN offset max par('abs(zzztemp)-0.75')
*.MEASURE TRAN tdlay TRIG V(10) VAL =0.75 TD =10n
*+ TARG V(4) VAL =0.75 rise=1

.END
