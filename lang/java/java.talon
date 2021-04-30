mode: user.java
mode: command
and code.language: java

-
tag(): user.code_operators
tag(): user.code_generic
tag(): user.code_comment
tag(): user.code_block_comment

action(user.code_operator_indirection): skip()
action(user.code_operator_address_of): skip()
action(user.code_operator_lambda): " -> "
action(user.code_operator_subscript): 
	insert("[]")
	key(left)
action(user.code_operator_assignment): " = "
action(user.code_operator_subtraction): " - "
action(user.code_operator_subtraction_assignment): " -= "
action(user.code_operator_addition): " + "
action(user.code_operator_addition_assignment): " += "
action(user.code_operator_multiplication): " * "
action(user.code_operator_multiplication_assignment): " *= "
action(user.code_operator_exponent): " ^ "
action(user.code_operator_division): " / "
action(user.code_operator_division_assignment): " /= "
action(user.code_operator_modulo): " % "
action(user.code_operator_modulo_assignment): " %= "
action(user.code_operator_equal): " == "
action(user.code_operator_not_equal): " != "
action(user.code_operator_greater_than): " > "
action(user.code_operator_greater_than_or_equal_to): " >= "
action(user.code_operator_less_than): " < "
action(user.code_operator_less_than_or_equal_to): " <= "
action(user.code_operator_and): " && "
action(user.code_operator_or): " || "
action(user.code_operator_bitwise_and): " & "
action(user.code_operator_bitwise_or): " | "
action(user.code_operator_bitwise_exclusive_or): " ^ "
action(user.code_operator_bitwise_left_shift): " << "
action(user.code_operator_bitwise_left_shift_assignment): " <<= "
action(user.code_operator_bitwise_right_shift): " >> "
action(user.code_operator_bitwise_right_shift_assignment): " >>= "
action(user.code_self): "this"
action(user.code_null): "null"
action(user.code_is_null): " == null"
action(user.code_is_not_null): " != null"
action(user.code_state_if): 
    insert("if () {}")
    key(left)
    key(enter)
    key(up:1 right:2)
action(user.code_state_else_if): 
    insert("else if () {}")
    key(left)
    key(enter)
    key(up:1 right:9)
action(user.code_state_else): 
	insert("else {}")
    key(left)
    key(enter)
action(user.code_state_switch):
    insert("switch () {}") 
    key(left)
    key(enter)
    key(up:1 right:6)
action(user.code_state_case):
	insert("case :\n\nbreak;") 
    key(up:2 left:1)
action(user.code_state_for):
    insert('for () {}')
    key(left)
    key(enter)
    key(up:1 right:3)
action(user.code_state_while): 
    insert("while () {}")
    key(left)
    key(enter)
    key(up:1 right:5)
action(user.code_type_class): "class "
action(user.code_private_function):
	insert("private")
action(user.code_protected_function):
    user.code_private_function()
action(user.code_public_function):
	insert("public ")
action(user.code_state_return):
    insert("return ;")
    key(left)
action(user.code_break): "break;"
action(user.code_next): "continue;"
action(user.code_true): "true"
action(user.code_false): "false"
action(user.code_comment): "//"
action(user.code_block_comment):
    insert("/**")
    key(enter)
    # key(enter)
    # insert("*/")
    # edit.up()
action(user.code_import):
    "import ;"
    key(left)

(stay) {user.java_type_list}:
    insert("{java_type_list} ")