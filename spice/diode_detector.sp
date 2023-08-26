* Diode Detector with AM signal

* Carrier 
VC carrier 0 sine(0v 1v 200meg)

* Signal
*VS signal 0 DC 0 PULSE(-1v 1v 0ns 1us  1us 1ns 2us)
VS signal 0 DC 0 PULSE(-1v 1v 0ns 10us  10us 1ns 20us)

* AM signal
Bam source 0 V=1*(1+1.0*V(signal))*V(carrier)
*Vsource 0 DC 0 PULSE(-1v 1v 0ns 10us  10us 1ns 20us)

* 50 Ohm source resistance
Rsource source input 50

* 50 Ohm termination resistance at detector
Rterm input 0 50

* Detector diode
XD1 input out BAT62-02w_IN
*XD1 input out 1N4148

* Detector capacitor 
Cdetect out 0 10p

* Detector load
Rload out 0 560

*7ft Coax cable - RG8: 50 Ohm Z0, C=30pF/ft -> 50=sqrt(L/C) -> L=2500*C = 75nH
Ccoax out 0 210p
Lcoax out probe 75n

* Probe load 1M
Rprobe probe 0 1MEG
.end

.TRAN 20p 40.0us
.PRINT trans v(input) v(out) v(probe)

.control
run
*plot input out probe
*plot probe out
plot signal+1 6*out source
.endc

*============================================================
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

*============================================================
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

*============================================================

