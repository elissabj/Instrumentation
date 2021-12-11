import math
import serialp

VRESOLUCION = 0.019607
VREF_ = 0
AV = 5/3
E1 = 3
E = 6
R = 6
B = 6
M = -1/10

def getDistance():
	combinacion_binaria = serialp.readSerial()
	va = (combinacion_binaria*VRESOLUCION)+VREF_
	e2 = -((va/AV)-E1)
	dr = (E*R-(e2*2*R))/(E-e2)
	rsen = R-dr
	dmm = (rsen - B)/M
	return math.ceil(dmm)

