.include "m32def.inc"

;**** Macros
.macro jumpto
	ldi	ZL, low(@0)
	ldi	ZH, high(@0)
	clr	r0
	add ZL, @1
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

; VM operations
op_const:
op_call:
op_jump:
op_jumpz:
op_jumpif:
	rjmp	tick_done

op_load:
	;ldi		r16, 'L'
	;rcall	ser_tx

	sbi		PORT_DEBUG, PIN_LED

	rjmp	tick_done

op_stor:
	;ldi		r16, 'S'
	;rcall	ser_tx

	cbi		PORT_DEBUG, PIN_LED

	rjmp	tick_done

op_return:
op_drop:
op_swap:
op_dup:
op_over:
op_str:
op_rts:
	rjmp	tick_done

op_add:
op_sub:
op_mul:
op_div:
op_mod:
op_and:
op_or:
op_xor:
op_not:
op_sgt:
op_slt:
op_sync:
op_next:
	rjmp	tick_done

tick:
	; TODO get the next instruction


	; execute the instruction
	jumpto	jmptable, r16
tick_done:
	ldi		r16, 10
	rcall	delay

	ret

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
	ldi		r16, 'h'
	rcall	ser_tx
	ldi		r16, 'i'
	rcall	ser_tx

forever:
	ldi		r16, VM_OP_LOAD
	rcall	tick

	ldi		r16, VM_OP_STOR
	rcall	tick

	ldi		r16, 't'
	rcall	ser_tx
	ldi		r16, 13
	rcall	ser_tx

	rjmp	forever

