.include "m32def.inc"

;**** Macros
.macro jumpto
	ldi	ZL, low(@0)
	ldi	ZH, high(@0)
	add ZL, @1
	clr	r0
	adc ZH, r0 
	ijmp
.endmacro

;**** Constants
.include "vm_const.asm"
.equ BAUD	= 12 ; 38.4K baud

;**** Registers
.def VM_PC	= r15
.def VM_DP	= r14
.def VM_RP	= r13

;**** Pin definitions

.equ PORT_UART	= PORTD
.equ DDR_UART	= DDRD
.equ PIN_RX		= PD0
.equ PIN_TX		= PD1

.equ PORT_FS	= PORTC
.equ DDR_FS		= DDRC
.equ FS_SCLK	= PC0
.equ FS_SDO		= PC1
.equ FS_SDI		= PC2
.equ FS_CS		= PC3

.equ PORT_DEBUG	= PORTA
.equ DDR_DEBUG	= DDRA
.equ PIN_LED	= PA0

.cseg

.org 0
	rjmp	reset

;**** includes
.include "serial.asm"

;**** system routines

jmptable:
	rjmp op_const
	rjmp op_call
	rjmp op_jump
	rjmp op_jumpz
	rjmp op_jumpif

	rjmp op_load
	rjmp op_stor
	rjmp op_return
	rjmp op_drop
	rjmp op_swap
	rjmp op_dup
	rjmp op_over
	rjmp op_str
	rjmp op_rts

	rjmp op_add
	rjmp op_sub
	rjmp op_mul
	rjmp op_div
	rjmp op_mod
	rjmp op_and
	rjmp op_or
	rjmp op_xor
	rjmp op_not
	rjmp op_sgt
	rjmp op_slt
	rjmp op_sync
	rjmp op_next

tick:
	; get the next instruction
	

	; execute the instruction
	jumpto	jmptable, r16
tick_done:

;INPUT: r16 time
;DESTROYS: r0, r1, r2
delay:
	clr		r0
	clr		r1
delay0: 
	dec		r0
	brne	delay0
	dec		r1
	brne	delay0
	dec		r16
	brne	delay0
	ret

;***** Program Execution Starts Here

reset:
	; set stack ptr
	ldi		r16, low(RAMEND)
	out		SPL, r16
	ldi		r16, high(RAMEND)
	out		SPH, r16

	; set IO pins to output
	sbi		DDR_FS, FS_SCLK 
	sbi		DDR_FS, FS_SDO
	sbi		DDR_FS, FS_CS

	ldi		r16, $FF
	out		DDR_DEBUG, r16

	; setup serial
	ldi		r16, BAUD
	ldi		r17, $00
	rcall	ser_init

	; say hello
	ldi		r16, 100
	rcall	delay

	ldi		r16, 'h'
	rcall	ser_tx
	ldi		r16, 'i'
	rcall	ser_tx

forever:
	sbi		PORT_DEBUG, PIN_LED

	ldi		r16, 10
	rcall	delay

	cbi		PORT_DEBUG, PIN_LED

	ldi		r16, 10
	rcall	delay

	rjmp	forever

