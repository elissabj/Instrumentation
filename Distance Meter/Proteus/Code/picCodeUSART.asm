;************************************************************
;Control de la USART
;Desarrollado por:______________________________________
;************************************************************
	LIST P=PIC16F628A
	#include <p16f628a.inc>
	__CONFIG _INTOSC_OSC_NOCLKOUT&_WDT_OFF&_PWRTE_ON&_MCLRE_OFF&_BOREN_OFF&_BODEN_OFF&_LVP_OFF&_CPD_OFF&_CP_OFF
;************************************************************
; Declaración de Registros
;************************************************************
w equ 0x00
status equ 0x03
porta equ 0x05
portb equ 0x06
intcon equ 0x0b
pir1 equ 0x0c
rcsta equ 0x18
txreg equ 0x19
rcreg equ 0x1a
cmcon equ 0x1f
trisa equ 0x85
trisb equ 0x86
pie1 equ 0x8c
txsta equ 0x98
spbrg equ 0x99
var1 equ 0x20
var2 equ 0x21
var3 equ 0x22
TxUSART equ 0x23
RxUSART equ 0x24
;************************************************************
; Declaración de Bits
;************************************************************
c equ 0
z equ 2
rp0 equ 5
rp1 equ 6
cren equ 4
txif equ 4
rcif equ 5
rcie equ 5
peie equ 6 ;habilitador de interrupciones por periferico
adie equ 6
adif equ 6 ;bandera de interrupcion por fin de conversion a/d.
gie equ 7 ;habilitador general de interrupciones
spen equ 7
Led_Tx equ 6
Led_Rx equ 7
;************************************************************
; Inicio
;************************************************************
	org 0
	goto iniProg
	org 4
	bcf status,rp0 ;cambiar al banco 0
	bcf status,rp1
	btfsc pir1,rcif
	goto interserie
	retfie
;************************************************************
; Interrupciones
;************************************************************
interserie
	bcf status,rp0 ;cambiar al banco 0
	bcf status,rp1
	bsf portb,Led_Rx
	bcf intcon,gie ;desactivar habilitador general de interrupciones.
	movf rcreg,w ;recuperar el dato recibido por rs232
	movwf RxUSART
	bcf pir1,rcif
	bsf intcon,gie
	bcf portb,Led_Rx
	retfie
;************************************************************
; Programa principal
;************************************************************
iniProg
	bsf status,rp0 ;cambia al banco 1
	bcf status,rp1
	movlw 0xff ;configura el puerto a como entradas
	movwf trisa
	movlw b'00000010' ;bit 1 como entrada demas del puerto b como salidas
	movwf trisb
	bcf status,rp0 ;cambia al banco 0
	bcf status,rp1
	movlw 0x07
	movwf cmcon
	clrf porta
	clrf portb
;------------------------------------------------------------
; Activacion de la USART
;------------------------------------------------------------
	bsf status,rp0 ;cambiar al banco 1
	bcf status,rp1
	movlw b'00100110'
	movwf txsta
	movlw .25 ; .12
	movwf spbrg
	bcf status,rp0 ;cambiar al banco 0
	bcf status,rp1
	bsf rcsta,spen ;habilitacion del puerto de comunicacion serial
	bsf rcsta,cren
	bsf intcon,gie ;activar habilitador general de interrupciones.
	bsf intcon,peie ;activar habilitador general de interrupciones por perifericos.
	bsf status,rp0 ;cambiar al banco 1
	bcf status,rp1
	bsf pie1,rcie ;activar interrupción por fin de recepción por usart.
;------------------------------------------------------------
leePuerto ;Lee puerto para obtener valores del ADC externo
;------------------------------------------------------------
	bcf status,rp0 ;cambiar al banco 0
	bcf status,rp1
	movf porta,w
	movwf TxUSART
	bsf portb,Led_Tx
	call transmite
	bcf portb,Led_Tx
	call retardo1seg
	goto leePuerto
;************************************************************
; Subrutinas
;************************************************************
;------------------------------------------------------------
retardo1seg ;Retardo de 1 segundo
;------------------------------------------------------------
	movlw .250
	movwf var1
ciclo_3
	movlw .08
	movwf var2
ciclo_2
	movlw .166
	movwf var3
ciclo_1
	decfsz var3,1 ;497microsegundos=
	goto ciclo_1 ;aprox. 0.5 milisegundos
	decfsz var2,1
	goto ciclo_2
	decfsz var1,1
	goto ciclo_3
	return
;------------------------------------------------------------
transmite ;Rutina que se encarga de la transmisión
;------------------------------------------------------------
	bsf status,rp0 ;cambiar al banco 1
	bcf status,rp1
	movlw b'00100110'
	movwf txsta
	movlw .25 ;.12 .15
	movwf spbrg
	bcf status,rp0 ;cambiar al banco 0
	bcf status,rp1
	bsf rcsta,spen
	movf TxUSART,w
	movwf txreg
txespera
	btfss pir1,txif
	goto txespera
	return
	end