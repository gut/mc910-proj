#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import ply.lex as lex

class CPLLexer():

	states = (("FORMATEDTEXT", "inclusive"),)

	#reserved strings in cpl
	reserved = {
		'BEGIN': 'BEGIN',
		'END':'END',
		'NEWSPAPER':'NEWSPAPER',
		'STRUCTURE' : 'STRUCTURE',
		'CONTENT' : 'CONTENT',
	}
	
	#Tokens parsed by this lexer
	tokens = [
		'COMMENT',
		'STRING',
		'NUMBER',
		'FIELD',
		'ID',
		'RBRACKET',
		'LBRACKET',
		'DOT',
	] + list(reserved.values())

	#literals used in cpl
	#literals = []
	t_LBRACKET = r'{'
	t_ignore = " \t"
	t_DOT = "."

	def t_RBRACKET(self, t):
		r'}'
		t.lexer.begin("INITIAL")
		return t

	def t_COMMENT(self, t):
		r'//.*'
		pass

	def t_FIELD(self, t):
		r'[a-zA-Z][a-zA-Z0-9_]*:[ ]+'
		t.lexer.begin('FORMATEDTEXT')
		return t

	def t_NUMBER(self, t):
	    r'\d+'
	    try:
		t.value = int(t.value)
	    except ValueError:
		print "Integer value too large", t.value
		t.value = 0
	    return t

	def t_ID(self, t):
		r'[a-zA-Z][a-zA-Z0-9_]*'
		t.type = self.reserved.get(t.value.upper(),'ID') # Check for reserved words
		return t

	t_FORMATEDTEXT_COMMENT = t_COMMENT

	t_FORMATEDTEXT_FIELD = t_FIELD

	t_FORMATEDTEXT_NUMBER = t_NUMBER

	def t_FORMATEDTEXT_STRING(self, t):
		u'([^{}\n])+'
		return t

	def t_newline(self, t):
		r'\n+'
		t.lexer.lineno += t.value.count("\n")
	
	def t_error(self, t):
		print "Illegal character '%s'" % t.value[0]
		t.lexer.skip(1)

	# Build the lexer
	def build(self, **kwargs):
		self.lexer = lex.lex(module=self, **kwargs)

if __name__ == "__main__":
	"""Runs a small test with the lexer"""
	import sys
	if len(sys.argv) < 2:
		print "first argument must be the cpl file."
		sys.exit(1)

	# Build the lexer
	cpllexer = CPLLexer()
	cpllexer.build()
	f=open(sys.argv[1])
	cpllexer.lexer.input(f.read())
	f.close()
	for i in cpllexer.lexer:
		print i

