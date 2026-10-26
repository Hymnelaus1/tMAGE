**aaaa
.inc 130nm.txt
.inc wafd_design.cir
m1 6  4  3 3 pfet l=lm1 w=wm1 ad=lm1*wm1 as=lm1*wm1 pd=2*(lm1+wm1) ps=2*(lm1+wm1)  
m2 7  5  3 3  pfet l=lm1 w=wm1 ad=lm1*wm1 as=lm1*wm1 pd=2*(lm1+wm1) ps=2*(lm1+wm1)  
m3 2  2  1 1 pfet l=lm2 w=wm2 ad=lm2*wm2 as=lm2*wm2 pd=2*(lm2+wm2) ps=2*(lm2+wm2)  
m4 3  2  1 1 pfet l=lm2 w=wm2 ad=lm2*wm2 as=lm2*wm2 pd=2*(lm2+wm2) ps=2*(lm2+wm2)  
m5 6  6  8 8 nfet l=lm3 w=wm3 ad=lm3*wm3 as=lm3*wm3 pd=2*(lm3+wm3) ps=2*(lm3+wm3)  
m6 7  7  8 8  nfet l=lm3 w=wm3 ad=lm3*wm3 as=lm3*wm3 pd=2*(lm3+wm3) ps=2*(lm3+wm3)  
Rb 2 8 Rb



cl 7 0 0.2e-12
cl2 6 0 0.2e-12


Vdd 1 0 DC 0.6
Vss 0 8 DC 0.6
*Vbias 19 0 dc Vbias

vnin 0 5 dc 0 ac 0.5 sin (0, 0.2V, 10kHz)
vin 4 0 dc 0 ac 0.5 sin (0, 0.2V, 10kHz)

.op
.PARAM AREA='2*WM1*LM1 + 2*WM2*LM2 + 2*WM3*LM3'
VX 1000 0 AREA
RX 1000 0 1K
*.option fast
.option post=1
.option sim_mode = client/server
.option OPFILE=1
*.op
.ac dec 100 100 10000000000
.TRAN 2n 600u 

.MEAS AC gain max PAR('db(V(7)-V(6))')
.MEAS AC tmp max PAR('gain-3')
.MEAS AC BW when par('db(V(7)-V(6))')=tmp
.MEAS volt max PAR('(V(7))')
.MEAS volt2 max PAR('(V(6))')
.MEAS vdb max PAR('(V(3)-V(6))')
*.MEAS AC BW when par('db(V(7))')= 0      
*.MEASURE AC hreal FIND VR(7) WHEN V(7)=1
*.MEASURE AC himg  FIND VI(7) WHEN V(7)=1
.MEAS TRAN vsp max V(7,6) FROM='50u' TO='200u'
.MEAS TRAN vsn min V(7,6) FROM='50u' TO='200u'  
.MEAS zPOWER AVG POWER

*.MEAS zSAREA avg PAR(AREA)
.END