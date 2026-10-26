*** bandgap for opt


.INC "nfet_01v8_1.txt"
.INC "pfet_01v8.txt"
.INC "pnp_05v5_W3p40L3p40.txt"
.inc parambanba.cir

.op 
*.nodeset vref 0.2V
V5 8 GND 0
V2 1 GND 1.8

**badngap core

.subckt opamp ip in vd vs ou
M1 8 5 vs vs nfet_01v8 L=0.3u W=10u mult=1 m=1 sa=0 sb=0 sd=0 nf=1 
M2 5 5 vs vs nfet_01v8 L=0.3u W=10u mult=1 m=1 sa=0 sb=0 sd=0 nf=1 
M3 7 7 vd  vd Pfet_01v8  L=0.7u W=2.3u mult=1 m=1 sa=0 sb=0 sd=0 nf=1 
M4 7 ip 8 vs nfet_01v8 L=0.3u W=4u mult=1 m=1 sa=0 sb=0 sd=0 nf=1 
M5 ou in 8 vs nfet_01v8 L=0.3u W=4u mult=1 m=1 sa=0 sb=0 sd=0 nf=1 
M6 ou 7 vd vd Pfet_01v8 L=0.7u W=2.3u mult=1 m=1 sa=0 sb=0 sd=0 nf=1

Ib vd 5 50u

.ends opamp


M1 inp out 1 1 pfet_01v8 l=lm1 w=wm1 *mult=1 m=1 sa=0 sb=0 sd=0 nf=1
M2 inn out 1 1 pfet_01v8 l=lm1 w=wm1 *mult=1 m=1 sa=0 sb=0 sd=0 nf=1
M3 vref out 1 1 pfet_01v8 l=lm1 w=wm1 *mult=1 m=1 sa=0 sb=0 sd=0 nf=1
R0 inp 4 Rb
R1 inn 8 Rb1
R2 inp 8 Rb1
R3 vref 8 Rb2
Q1 8 8 inn pnp_05v5_W3p40L3p40
Q2 8 8 4 pnp_05v5_W3p40L3p40
Q3 8 8 4 pnp_05v5_W3p40L3p40
Q4 8 8 4 pnp_05v5_W3p40L3p40
Q5 8 8 4 pnp_05v5_W3p40L3p40
Q6 8 8 4 pnp_05v5_W3p40L3p40
Q7 8 8 4 pnp_05v5_W3p40L3p40
Q8 8 8 4 pnp_05v5_W3p40L3p40
Q9 8 8 4 pnp_05v5_W3p40L3p40
X1 inp inn 1 8 out opamp


*E1 out 0 inp inn 1

**biasing circuit

Ms1 2 2 1 1 pfet_01v8 l=lm2 w=wm2 *mult=1 m=1 sa=0 sb=0 sd=0 nf=1
Ms2 3 3 2 2 pfet_01v8 l=lm3 w=wm3 *mult=1 m=1 sa=0 sb=0 sd=0 nf=1
Ms3 out 3 8 8 nfet_01v8 l=lm4 w=wm4 *mult=1 m=1 sa=0 sb=0 sd=0 nf=1
Ms4 3 vref 8 8 nfet_01v8 l=lm5 w=wm5 *mult=1 m=1 sa=0 sb=0 sd=0 nf=1

*.PARAM AREA='2*WM1*LM1 + 2*WM2*LM2 + 2*WM3*LM3'
*VX 1000 0 AREA
*RX 1000 0 1K

.option post=1
.option sim_mode = client/server
.option OPFILE=1
.dc temp -40 125 1


.MEAS zPOWER AVG POWER 
*.MEAS DC ref max PAR('V(vref)')
*.MEAS DC refmin min PAR('V(vref)')
*.MEAS volt find PAR('(V(vref))') at 25    
.MEAS zSAREA avg PAR(AREA)

.end


*ad='int((nf+1)/2) * W/nf * 0.29' as='int((nf+2)/2) * W/nf * 0.29'
*+ pd='2*int((nf+1)/2) * (W/nf + 0.29)' ps='2*int((nf+2)/2) * (W/nf + 0.29)' nrd='0.29 / W' nrs='0.29 / W'

*****For W = 5u
*ad=1.45e-6 as=72.5e-6 pd=0.290005 ps=0.870015 *nrd=58e+3 nrs=58e+3  
*****For W = 1u
*ad=0.29e-6 as=43.5e-6  pd=0.580002 ps=0.290001 *nrd=29e+4 nrs=29e+4