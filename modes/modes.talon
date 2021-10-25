#defines the various mode commands
mode: all
-
# welcome back:
#     user.mouse_wake()
#     user.history_enable()
#     user.talon_mode()
# sleep all:
#     user.switcher_hide_running()
#     user.history_disable()
#     user.homophones_hide()
#     user.help_hide()
#     user.mouse_sleep()
#     speech.disable()
#     user.engine_sleep()
(talon | dragon | drag and) sleep: 
    speech.disable()
    user.help_hide()
    user.history_disable()
    user.mouse_sleep()
    user.engine_sleep()

(talon | dragon | drag and) wake: 
    speech.enable()
    user.history_enable()
    user.mouse_wake()

^dictation mode$:
    mode.disable("sleep")
    mode.disable("command")
    mode.enable("dictation")
    user.code_clear_language_mode()
    mode.disable("user.gdb")
^command mode$:
    mode.disable("sleep")
    mode.disable("dictation")
    mode.enable("command")
^pop mode$:
    mode.disable("sleep")
    mode.disable("dictation")
    mode.disable("command")
    mode.enable("user.pop")
