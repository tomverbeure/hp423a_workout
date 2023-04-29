
* voltage divider netlist
*V1 in 0 1
* V1 in 0 DC 0 PULSE(0v 1.5v 100ps 50ps 50ps 200ps 500ps)
*                  init pulse delay  rise  fall   width   period
*V1 in 0 DC 0 PULSE(0v 1.0v    10ns   200ns  200ns 50ns   500ns)
V1 in 0 DC 0 PULSE(0v 6mv    10ns   200ns  200ns 1ns   401ns)
*V1 in 0 DC 0 sine(0v 500mv 1MEG)
*R1 in out 1k
*XD1 in out 1N4148
XD1 in out BAT62-02w_IN
R2 out 0 2000
.end

.TRAN 1n 1000ns
.PRINT trans v(in) v(out) 

.control
run
plot in out 0.37*v(in)*v(in) 
*plot in out 0.37*v(in)*v(in) v(out)-0.37*v(in)*v(in) 
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
