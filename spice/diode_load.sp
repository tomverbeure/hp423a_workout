
.options savecurrents 

* voltage divider netlist
*V1 in 0 1
* V1 in 0 DC 0 PULSE(0v 1.5v 100ps 50ps 50ps 200ps 500ps)

*                  init pulse delay  rise  fall   width   period
V1 in 0 DC 0 PULSE(0v 400mv    0ns   400ns  400ns 1ps   800ns)
*V1 in 0 DC 0.5 
*V1 in 0 DC 0 sine(0v 500mv 1MEG)

XD1 in out1 BAT63-03w_IN
R1 out1 id1 10k
Vid1 id1 0 DC 0

XD2 in out2 BAT63-03w_IN
R2 out2 id2 1000
Vid2 id2 0 DC 0

XD3 in out3 BAT63-03w_IN
R3 out3 id3 500
Vid3 id3 0 DC 0

XD4 in out4 BAT63-03w_IN
R4 out4 id4 250
Vid4 id4 0 DC 0

XD5 in out5 BAT63-03w_IN
R5 out5 id5 125
Vid5 id5 0 DC 0

XD8 in id8  BAT63-03w_IN
*R8 out8 0 0.01
Vid8 id8 0 DC 0

.end

*.tran 1n 1000ns
.tran 0.1n 395ns
*.tran 0.1n 80ns
.print trans v(in) v(out1) 

.control
run
plot v(out1) v(out2) v(out3) v(out4) v(out5) v(in)
*plot (v(out1)/100k) (v(out2)/1000) (v(out3)/500)
plot v(in)-v(out1) v(in)-v(out2) v(in)-v(out3) v(in)-v(out4) v(in)-v(out5) v(in)
plot i(Vid1) i(Vid2) i(Vid3) i(Vid4) i(Vid5)
plot v(out3) v(in)/14 0.72*v(in)*v(in)+0.0005

* Diode resistance
*plot (v(in)-v(out1))/i(Vid1) (v(in)-v(out2))/i(Vid2) (v(in)-v(out3))/i(Vid3) (v(in)-v(out4))/i(Vid4) (v(in)-v(out5))/i(Vid5) v(in)*10000
* Total resistance
*plot v(in) v(out1)/i(Vid1) v(out2)/i(Vid2) v(out3)/i(Vid3) v(out4)/i(Vid4) v(out5)/i(Vid5) 

*plot i(v8)

*plot v(out3)
*plot (v(out3)/0.01)
*plot in out1 0.37*v(in)*v(in) 
*plot in out1 0.37*v(in)*v(in) v(out1)-0.37*v(in)*v(in) 
.endc

.SUBCKT 1N4148 1 2 
*
* The resistor R1 does not reflect 
* a physical device. Instead it
* improves modeling in the reverse 
* mode of operation.
*
R1 1 2 5.827E+9 
D1 1 2 1N4148
*
.MODEL 1N4148 D 
+ IS = 4.352E-9 
+ N = 1.906 
+ BV = 110 
+ IBV = 0.0001 
+ RS = 0.6458 
+ CJO = 7.048E-13 
+ VJ = 0.869 
+ M = 0.03 
+ FC = 0.5 
+ TT = 3.48E-9 
.ENDS

.SUBCKT BAT62-02w_IN 100 200 
*Package SCD80:
LAIL1  1   10    0.45nH
CACC2 10    2    90fF
LAOL2 10  100    0.15nH
LCOL3 2   200    0.1nH   
*interne Dioden:
D1 1 2 D1
R1 1 2 40e6
.MODEL D1 D(IS=250.0n N=1.04 RS=190.0 XTI=1.5 EG=0.53 
+ CJO=284.2f M=0.17 VJ=0.224 FC=0.5 TT=25.0p BV=59.3 IBV=10.0u)
.ENDS BAT62-02w_IN 

.SUBCKT BAT63-03w_IN 100 200 
*Package SOD323:
L1       1   10  0.55nH
C2      10    2  110fF
L2      10  100  0.67nH
L3      2   200  0.55nH  
*interne Diode:
D1 1 2 D1
R1 1 2 20e6
.MODEL D1 D(IS=761.0n N=1.06 RS=2.633 XTI=1.5 EG=0.59 
+ CJO=628.0f M=0.185 VJ=0.224 FC=0.5 TT=25.0p BV=14.4 IBV=100.0u)
.ENDS BAT63-03w_IN
