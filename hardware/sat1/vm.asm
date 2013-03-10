.include "m32def.inc"

;**** Macros
.macro get_params	; for instructions with 2 params
	rcall	vm_popd
	movw	TEMPH:TEMPL, YH:YL
	rcall	vm_popd
.endmacro

.macro inc_ptr
	clr		r0
	inc		@0L
	adc		@0H, r0
.endmacro

.macro dec_ptr
	clr		r0
	dec		@0L
	sbc		@0H, r0
.endmacro

.macro to_ptr
	st		X+, YH
	st		X, YL
.endmacro

.macro from_ptr
	ld		YH, X+
	ld		YL, X
.endmacro

.macro pc_to_X
	ldi		XH, high(SRAM_START)
	ldi		XL, low(SRAM_START)
	add		XL, VM_PCL	; offset by VM's PC
	adc		XH, VM_PCH
.endmacro

.macro ptr_to_X
	mov		XL, @0L		; start w/ raw data ptr
	mov		XH, @0H
	lsl		XL			; multiply by 2 for byte offset
	rol		XH
	ldi		r16, low(SRAM_START)
	add		XL, r16
	ldi		r16, high(SRAM_START)
	adc		XH, r16
.endmacro

.macro jumpto
	ldi	ZL, low(@0)
	ldi	ZH, high(@0)
	clr	r0
	add ZL, @1
	adc ZH, r0 
	ijmp
.endmacro

;**** Constants
; VM's
.include "vm_const.asm"
.equ DATA_STACK		= 127
.equ RET_STACK		= 255

; general
.equ BAUD	= 12 ; 38.4K baud

;**** Registers
; VM's
.def VM_PCH	= r15
.def VM_PCL = r14
.def VM_DPH	= r13
.def VM_DPL	= r12
.def VM_RPH	= r11
.def VM_RPL	= r10

; general
.def TEMPH	= r9
.def TEMPL	= r8

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
	inc_ptr		VM_PC
	pc_to_X
	from_ptr
	rcall		vm_pushd
	rjmp		tick_done2

op_call:
op_jump:
op_jumpz:
op_jumpif:
	rjmp	tick_done

; addr, val
op_load:
	get_params

	; load mem
	movw	XH:XL, TEMPH:TEMPL
	from_ptr
	rcall	vm_pushd

	rjmp	tick_done1

; addr, val
op_stor:
	get_params

	; set mem
	movw	XH:XL, TEMPH:TEMPL
	to_ptr

	rjmp	tick_done1

op_return:
op_drop:
op_swap:
op_dup:
op_over:
op_str:
op_rts:
	rjmp	tick_done

op_add:
	get_params

	; add them
	add		YL, TEMPL
	adc		YH, TEMPH

	; push result
	rcall	vm_pushd

	rjmp	tick_done1
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

halt:
	sbi		PORT_DEBUG, PIN_LED
	rjmp	halt

tick:
	; get the next instruction
	pc_to_X
	ld		r16, X

	; check if done
	cpi		r16, $FF
	breq	halt

	; execute the instruction
	jumpto	jmptable, r16
tick_done3:		; increment PC by 3
	clr		r0
	inc		VM_PCL
	adc		VM_PCH, r0
tick_done2:		; increment PC by 2
	clr		r0
	inc		VM_PCL
	adc		VM_PCH, r0
tick_done1:		; increment PC by 1
	clr		r0
	inc		VM_PCL
	adc		VM_PCH, r0
tick_done:
	; ldi		r16, 10
	; rcall	delay

	ret

;**** VM helper functions

; pushes to VM data stack
;INPUT: Y contains data to push
vm_pushd:
	; get RAM location of ptr
	ptr_to_X	VM_DP
	inc_ptr		VM_DP
	rjmp	vm_push
vm_pushr:
	ptr_to_X	VM_RP
	inc_ptr		VM_RP
vm_push:
	; store the val
	to_ptr

	ret

; pops from VM data stack
;OUTPUT: Y contains val
vm_popd:
	dec_ptr		VM_DP 
	ptr_to_X	VM_DP
	from_ptr

	ret

; pops from VM return stack
;OUTPUT: r16 contains val
vm_popr:
	dec_ptr		VM_RP 
	ptr_to_X	VM_RP

	ld		YH, X+
	ld		YL, X

	ret

; loads program from PROGMEM into RAM
;INPUT: Z is address in PROGMEM
vm_load:
	ldi		XH, high(SRAM_START)
	ldi		XL, low(SRAM_START)

	ldi		r17, 8
vm_load_loop:
	lpm		r16, Z+
	st		X+, r16
	
	dec		r17
	brne	vm_load_loop

	ret

; resets the VM
vm_init:
	clr		VM_PCL
	clr		VM_PCH

	ldi		r16, low(DATA_STACK)
	mov		VM_DPL, r16
	ldi		r16, high(DATA_STACK)
	mov		VM_DPH, r16

	ldi		r16, low(RET_STACK)
	mov		VM_RPL, r16
	ldi		r16, high(RET_STACK)
	mov		VM_RPH, r16

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

	; init the VM
	rcall	vm_init

	; load the test program
	ldi		ZH, high(test_program<<1)
	ldi		ZL, low(test_program<<1)
	rcall	vm_load
forever:
	rcall	tick

	ldi		r16, 'T'
	rcall	ser_tx

	rjmp	forever

test_program:
	;.db		VM_OP_LOAD, VM_OP_STOR, VM_OP_LOAD, VM_OP_STOR, $FF, $FF
	.db		VM_OP_CONST, 0, 56, VM_OP_CONST, 0, 91, VM_OP_ADD, 255
