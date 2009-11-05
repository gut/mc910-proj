#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import ply.lex as lex

class CPLLexer():
	#reserved strings in cpl
	reserved = {
		'BEGIN': 'BEGIN',
		'END':'END',
		'NEWSPAPER':'NEWSPAPER',
	}
	
	#Tokens parsed by this lexer
	tokens = [
		'COMMENT',
		'STRING', 
		'FIELD',
	] + list(reserved.values())

	#literals used in cpl
	literals = ['{','}']
	
	t_ignore = " \t"

	#parse comments
	def t_COMMENT(self, t):
		r'//.*'
		pass

	#parse a field, i.e. A string followed by ':'
	def t_FIELD(self, t):
		r'[a-zA-Z][a-zA-Z0-9_]*:'
		return t

	#parse regular strings and reserved words
	def t_STRING(self, t):
		u'([^{}\n])+'
		t.type = self.reserved.get(t.value.upper(),'STRING')	 # Check for reserved words
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

