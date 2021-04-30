import re

from talon import Context, Module, actions, settings

mod = Module()
ctx = Context()
ctx.matches = r"""
mode: user.java
mode: command
and code.language: java
"""

type_list = {
    "boolean": "boolean",
    "bully": "boolean",
    "integer": "int",
    "int": "int",
    "string": "String",
    "void": "void",
    "float": "float",
    "long": "long",
    "double": "double",
    "byte": "byte",

# convenient to put here    
    "private": "private",
    "private static": "private static",
    "protected": "protected",
    "protected static": "protected static",
    "public": "public",
    "public static": "public static",
    "static": "static",
    "final": "final",
 
}

mod.list("java_type_list", desc="java types")
ctx.lists["user.java_type_list"] = type_list