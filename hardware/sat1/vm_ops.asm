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
	rcall	vm_popd
	rjmp	tick_done1

op_swap:
	get_params

	; swap them
	rcall	vm_pushd
	movw	YH:YL, TEMPH:TEMPL
	rcall	vm_pushd

	rjmp	tick_done1

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
	get_params

	; subtract them
	sub		YL, TEMPL
	sbc		YH, TEMPH

	; push result
	rcall	vm_pushd

	rjmp	tick_done1

op_mul:
	get_params

	; multiply them
	mul		YH, TEMPH
	mov		TEMP4, r0
	mov		TEMP5, r1

	mul		YL, TEMPL
	mov		TEMP2, r0
	mov		TEMP3, r1

	mul		YH, TEMPL
	add		TEMP3, r0
	adc		TEMP4, r1

	mul		YL, TEMPH
	add		TEMP3, r0
	adc		TEMP4, r1

	clr		r0
	adc		TEMP5, r0

	; push results
	mov		YH, TEMP5
	mov		YL, TEMP4
	rcall	vm_pushd

	mov		YH, TEMP3
	mov		YL, TEMP2
	rcall	vm_pushd

	rjmp	tick_done1

op_div:
op_mod:
op_and:
	get_params

	; AND them
	and		YL, TEMPL
	and		YH, TEMPH

	; push result
	rcall	vm_pushd

	rjmp	tick_done1
	
op_or:
	get_params

	; OR them
	or		YL, TEMPL
	or		YH, TEMPH

	; push result
	rcall	vm_pushd

	rjmp	tick_done1

op_xor:
	get_params

	; XOR them
	eor		YL, TEMPL
	eor		YH, TEMPH

	; push result
	rcall	vm_pushd

	rjmp	tick_done1

op_not:
	rcall	vm_popd

	; NOT it
	com		YL
	com		YH

	; push result
	rcall	vm_pushd

	rjmp	tick_done1

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
