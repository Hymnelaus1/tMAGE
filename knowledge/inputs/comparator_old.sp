*latch comp_two


.param WM5=6e-06
.param WM6=2e-06

M0	2	1	vdd	vdd	PFET	l=Lcm w=WM1 ad=Lcm*WM1 as=Lcm*WM1 pd=2*(Lcm+WM1) ps=2*(Lcm+WM1)
M1	1	2	vdd	vdd	PFET	l=Lcm w=WM1 ad=Lcm*WM1 as=Lcm*WM1 pd=2*(Lcm+WM1) ps=2*(Lcm+WM1)
M2	1	in	4	4	NFET	l=Lcm w=WM2 ad=Lcm*WM2 as=Lcm*WM2 pd=2*(Lcm+WM2) ps=2*(Lcm+WM2)
M3	2	ref	4	4	NFET	l=Lcm w=WM2 ad=Lcm*WM2 as=Lcm*WM2 pd=2*(Lcm+WM2) ps=2*(Lcm+WM2)
M4	4	bias	vss	vss	NFET	l=Lcm w=WM3 ad=Lcm*WM3 as=Lcm*WM3 pd=2*(Lcm+WM3) ps=2*(Lcm+WM3)
M5	1	1	vdd	vdd	PFET	l=Lcm w=WM4 ad=Lcm*WM4 as=Lcm*WM4 pd=2*(Lcm+WM4) ps=2*(Lcm+WM4)
M6	2	2	vdd	vdd	PFET	l=Lcm w=WM4 ad=Lcm*WM4 as=Lcm*WM4 pd=2*(Lcm+WM4) ps=2*(Lcm+WM4)
M7	3	1	vdd	vdd	PFET	l=Lcm w=WM4 ad=Lcm*WM4 as=Lcm*WM4 pd=2*(Lcm+WM4) ps=2*(Lcm+WM4)
M8	5	2	vdd	vdd	PFET	l=Lcm w=WM4 ad=Lcm*WM4 as=Lcm*WM4 pd=2*(Lcm+WM4) ps=2*(Lcm+WM4)
M9	5	3	vss	vss	NFET	l=Lcm w=WM3 ad=Lcm*WM3 as=Lcm*WM3 pd=2*(Lcm+WM3) ps=2*(Lcm+WM3)
M10	3	3	vss	vss	NFET	l=Lcm w=WM3 ad=Lcm*WM3 as=Lcm*WM3 pd=2*(Lcm+WM3) ps=2*(Lcm+WM3)
M11	out	5	vdd	vdd	PFET	l=Lcm w=WM5 ad=Lcm*WM5 as=Lcm*WM5 pd=2*(Lcm+WM5) ps=2*(Lcm+WM5)
M12	out	5	vss	vss	NFET	l=Lcm w=WM6 ad=Lcm*WM6 as=Lcm*WM6 pd=2*(Lcm+WM6) ps=2*(Lcm+WM6)



Cl1	out	GND	0.1p

Vdd	vdd	GND	dc	0.9
Vss	vss	GND	dc	-0.9
Vb	bias	GND	dc	0.1
Vin1	ref	GND	dc	0
Vip	in	GND	PWL(0.0001n -0.9 100n 0.9)
*Vip	in	GND	ac	1




.option post
.op
.INC 130nm.txt
.INC param_comp_old.cir
*.PARAM AREA='2*WM1*Lcm + WM2*Lcm + WM3*Lcm + WM4*Lcm + 2*WM6*Lcm +WM7*Lcm + 4*WM11*Lcm'
*VX 1000 0 AREA
*RX 1000 0 1K
.option fast
.option post
.option sim_mode = client/server


.ac dec 100 100 100000000000
.TRAN 0.1p 100n 

*.MEAS AC gain max PAR('db(V(4))')
*.MEAS AC tmp max par('gain-3')
*.MEAS AC BW when par('db(V(4))')= 0      
*.MEASURE AC hreal FIND VR(4) WHEN V(4)=1
*.MEASURE AC himg  FIND VI(4) WHEN V(4)=1  
.MEAS zPOWER AVG POWER 
*.MEAS zSAREA avg PAR(AREA)

.MEAS TRAN zzztemp FIND v(in) WHEN v(out)=0V rise=1
.MEAS TRAN zzztemps FIND V(in) WHEN v(in)=0V 
.MEAS TRAN offset max par('abs(zzztemp)')
.MEASURE TRAN tdlay TRIG V(in) VAL =0 TD =1n
+ TARG V(out) VAL =0 rise=1

.END