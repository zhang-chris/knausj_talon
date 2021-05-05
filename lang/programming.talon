tag: user.code_generic
-
block: user.code_block()

#todo should we have a keyword list? type list capture? stick with "word"?
#stay in: insert(" in ")
is not (none|null): user.code_is_not_null()
is (none|null): user.code_is_null()
#todo: types?
#word (dickt | dictionary): user.code_type_dictionary()
stay if: user.code_state_if()
stay else if: user.code_state_else_if()
stay else: user.code_state_else()
stay self: user.code_self()
#todo: this is valid for many languages,
# but probably not all
self dot:
    user.code_self()
    insert(".")
stay while: user.code_state_while()
stay for: user.code_state_for()
stay for in: user.code_state_for_each()
stay switch: user.code_state_switch()
stay case: user.code_state_case()
stay do: user.code_state_do()
stay goto: user.code_state_go_to()
stay return: user.code_state_return()
stay import: user.code_import()
from import: user.code_from_import()
stay class: user.code_type_class()
stay include: user.code_include()
stay include system: user.code_include_system()
stay include local: user.code_include_local()
stay type deaf: user.code_type_definition()
stay type deaf struct: user.code_typedef_struct()
stay (no | nil | null): user.code_null()
stay break: user.code_break()
stay next: user.code_next()
stay true: user.code_true()
stay false: user.code_false()

# show and print functions and libraries
toggle funk: user.code_toggle_functions()
funk <user.code_functions>:
    user.code_insert_function(code_functions, "")
funk cell <number>:
    user.code_select_function(number - 1, "")
funk wrap <user.code_functions>:
    user.code_insert_function(code_functions, edit.selected_text())
funk wrap <number>:
    user.code_select_function(number - 1, edit.selected_text())
dock string: user.code_document_string()