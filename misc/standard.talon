#(jay son | jason ): "json"
#(http | htp): "http"
#tls: "tls"
#M D five: "md5"
#word (regex | rejex): "regex"
#word queue: "queue"
#word eye: "eye"
#word iter: "iter"
#word no: "NULL"
#word cmd: "cmd"
#word dup: "dup"
#word shell: "shell".
zoom in: edit.zoom_in()
zoom out: edit.zoom_out()
scroll up: edit.page_up()
scroll down: edit.page_down()
copy that: edit.copy()
cut that: edit.cut()
(paste that | pasta): edit.paste()
undo that: edit.undo()
wipe: edit.undo()
redo that: edit.redo()
redo: edit.redo()
paste match: edit.paste_match_style()
file save: edit.save()
#wipe: key(backspace)    
(padding): 
	insert("  ") 
	key(left)

pad dash: " - "
pad arrow: " -> "

slap:
	edit.line_end()
	key(enter)