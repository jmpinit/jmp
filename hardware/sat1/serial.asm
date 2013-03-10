;INPUT: r16-r17 baud rate
ser_init:
	; make tx pin output
	sbi		DDR_UART, PIN_TX

	; set baud rate
	out		UBRRH, r17
	out		UBRRL, r16

	; enable transmitter & receiver
	ldi		r16, (1<<RXEN)|(1<<TXEN)
	out		UCSRB, r16

	; set frame format: 8 data, 2 stop
	ldi		r16, (1<<URSEL)|(1<<USBS)|(3<<UCSZ0)
	out		UCSRC, r16

	ret

ser_tx:
	; wait for empty tx buffer
	sbis	UCSRA, UDRE
	rjmp	ser_tx
	
	out		UDR, r16

	ret

ser_rx:
	; TODO implement
	ret
