#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import ply.lex as lex

class StringLexer():

	#Tokens parsed by this lexer
	tokens = [
		'RECUO',
		'TITLE',
		'STRING',
	]

	#literals used in cpl

	def t_RECUO(self, t):
		r'[:]+'
		t.value = len(t.value)
		return t

	def t_TITLE(self, t):
		r'[=]+'
		t.value = len(t.value)
		return t

	def t_STRING(self, t):
		u'([^\n])+'
		t.value = t.value.strip()
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
		print "first argument must be the string."
		sys.exit(1)

	# Build the lexer
	stringlexer = StringLexer()
	stringlexer.build()
	stringlexer.lexer.input(sys.argv[1])
	for i in stringlexer.lexer:
		print i

