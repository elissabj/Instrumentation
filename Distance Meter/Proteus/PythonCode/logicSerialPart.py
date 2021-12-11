import serial
import struct

com_serial = serial.Serial('COM2', baudrate = 9600, bytesize = 8, parity='N', stopbits=1)

def readSerial():
	cc = com_serial.read()
	return cc[0]

	


