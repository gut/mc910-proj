#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import ply.yacc as yacc

class CPLParser():
	def __init__(self, lexer):
		self.lex = lexer.lexer
		self.tokens = lexer.tokens

	def p_statement_assign(self, t):
		'statement : BEGIN END'
		print 'a'
	
	def build(self, **kwargs):
		self.parser = yacc.yacc(module=self, **kwargs)

if __name__ == "__main__":
	"""Runs a small test with the parser"""
	import sys
	from cpllexer import CPLLexer

	if len(sys.argv) < 2:
		print "first argument must be the cpl file."
		sys.exit(1)

	# Build the lexer
	cpllexer = CPLLexer()
	cpllexer.build()
	cplparser = CPLParser(cpllexer)
	cplparser.build()
	f=open(sys.argv[1])
	cplparser.parser.parse(f.read())
	f.close()

