*** bandgap for opt


.INC "nfet_01v8_1.txt"
.INC "pfet_01v8.txt"
.INC "pnp_05v5_W3p40L3p40.txt"
.inc param_bgr.cir

.op 


.subckt banbaBGR VDD VSS vref

XM1 1 1 VDD VDD sky130_fd_pr__pfet_01v8 l=lm1 w=wm1 ad=0.29u*WM1 as=ad pd=0.29u*2+WM1*2 ps=pd
XM2 2 1 VDD VDD sky130_fd_pr__pfet_01v8 l=lm1 w=wm1 ad=0.29u*WM1 as=ad pd=0.29u*2+WM1*2 ps=pd

XM3 3 2 VDD VDD sky130_fd_pr__pfet_01v8 l=lm2 w=wm2 ad=0.29u*WM2 as=ad pd=0.29u*2+WM2*2 ps=pd

XM4 Va 2 VDD VDD sky130_fd_pr__pfet_01v8 l=lm3 w=wm3 ad=0.29u*WM3 as=ad pd=0.29u*2+WM3*2 ps=pd
XM5 Vb 2 VDD VDD sky130_fd_pr__pfet_01v8 l=lm3 w=wm3 ad=0.29u*WM3 as=ad pd=0.29u*2+WM3*2 ps=pd
XM6 vref 2 VDD VDD sky130_fd_pr__pfet_01v8 l=lm3 w=wm3 ad=0.29u*WM3 as=ad pd=0.29u*2+WM3*2 ps=pd

XMN1 1 Vb Vs Vs sky130_fd_pr__nfet_01v8 l=lm4 w=wm4 ad=0.29u*WM4 as=ad pd=0.29u*2+WM4*2 ps=pd
XMN2 2 Va Vs Vs sky130_fd_pr__nfet_01v8 l=lm4 w=wm4 ad=0.29u*WM4 as=ad pd=0.29u*2+WM4*2 ps=pd
XMN3 Vs 3 VSS VSS sky130_fd_pr__nfet_01v8 l=lm5 w=wm5 ad=0.29u*WM5 as=ad pd=0.29u*2+WM5*2 ps=pd
XMN4 3 3 VSS VSS sky130_fd_pr__nfet_01v8 l=lm5 w=wm5 ad=0.29u*WM5 as=ad pd=0.29u*2+WM5*2 ps=pd



XMS1 32 32 VDD VDD sky130_fd_pr__pfet_01v8 l=0.3u w=12u ad=0.29u*4u as=ad pd=0.29u*2+4u*2 ps=pd
XMS2 33 33 32 32 sky130_fd_pr__pfet_01v8 l=0.3u w=12u ad=0.29u*4u as=ad pd=0.29u*2+4u*2 ps=pd
XMS3 2 33 VSS VSS sky130_fd_pr__nfet_01v8 l=0.3u w=4u ad=0.29u*4u as=ad pd=0.29u*2+4u*2 ps=pd
XMS4 33 vref VSS VSS sky130_fd_pr__nfet_01v8 l=0.3u w=4u ad=0.29u*4u as=ad pd=0.29u*2+4u*2 ps=pd



R1 Va VSS Rb12
R2 Vb VSS Rb12
R3 VB d1 Rb3
R4 vref VSS Rb4
Q1 VSS VSS Va pnp_05v5_W3p40L3p40 mult=1
Q2 VSS VSS d1 pnp_05v5_W3p40L3p40 mult=8

.ends


X2 VDD VSS vref banbaBGR

V2 VDD GND 1.8 AC 1
V5 VSS GND 0

* .OPTION LISNEW=1
.OPTION post=1
.OPTION MEASFORM=1
.OPTION NOMOD=1
.OPTION MEASFAIL=0
.OPTION UNWRAP

* .dc VSUPS 1.65 1.95 0.01
* .MEAS DC vrefmax_VSUPS max PAR('V(vref_supsw)')
* .MEAS DC verefmin_VSUPS min PAR('V(vref_supsw)')
* * .MEAS DC dif_vsup PARAM = 'vrefmax_VSUPS-verefmin_VSUPS' 
* .MEAS DC volt3 find PAR('(V(vref))') at 1.8
* .MEAS DC dif_vsup PARAM = '(1/volt3)*((vrefmax_VSUPS-verefmin_VSUPS)/3)*1e6'
.ac dec 10 10 1000000000
.tran 2n 0.5m

.NOISE V(vref) V2
.PRINT ONOISE INOISE
.dc temp -40 125 1 
.MEAS AC PSRR find par('-db(V(vref))') at 100
.MEAS TRAN zPOWER AVG POWER 
.MEAS DC ref max PAR('V(vref)')
.MEAS DC refmin min PAR('V(vref)')
.MEAS DC volt find PAR('(V(vref))') at 25
.MEAS DC volt2 find PAR('(V(vref))') at 25
.MEAS AC tot_noise INTEGRAL ONOISE from=1e3 to=1e7 print=0
.MEAS AC noise PARAM='tot_noise/1e5'
.MEAS DC ppm PARAM = '(1/volt)*((ref-refmin)/165)*1e6'   

*.MEAS zSAREA avg PAR(AREA)

.end


