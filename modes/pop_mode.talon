mode: pop
-
settings():
    #stop continuous scroll/gaze scroll with a pop
    user.mouse_enable_pop_stops_scroll = 0
	#enable pop click with 'control mouse' mode
	user.mouse_enable_pop_click = 1

#this exists solely to prevent talon from waking up super easily in sleep mode at the moment with wav2letter
<phrase>: skip()
