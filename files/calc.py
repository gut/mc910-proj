#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
# calc.py
#
# A simple calculator with variables.   This is from O'Reilly's
# "Lex and Yacc", p. 63.
# -----------------------------------------------------------------------------

import sys
sys.path.insert(0,"../..")

reserved = {
	'begin': 'BEGIN',
	'end':'END',
	'newspaper':'NEWSPAPER',
}

tokens = [
	'AAA',
    'COMMENT',
    'STRING', 
    'FIELD',
    ] + list(reserved.values())

literals = ['{','}']

# Tokens
#t_COMMENT = r'//.*'
#t_STRING    = r'[a-zA-Z_][a-zA-Z0-9_ ]*'

def t_COMMENT(t):
	'//.*'
	pass

def t_FIELD(t):
	r'[a-zA-Z][a-zA-Z0-9_]*:'
	return t

def t_STRING(t):
	u'.+'
	t.type = reserved.get(t.value,'STRING')    # Check for reserved words
	return t

t_ignore = " \t"

def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")
    
def t_error(t):
    print "Illegal character '%s'" % t.value[0]
    t.lexer.skip(1)
    
# Build the lexer
import ply.lex as lex
lexer= lex.lex()
f=open('exemplo.cpl')
lexer.input(f.read())
f.close()
for i in lexer:
	print i

