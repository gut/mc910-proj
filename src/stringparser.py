#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import ply.yacc as yacc
from color import *

class StringParser():
	def __init__(self, lexer):
		self.lex = lexer.lexer
		self.tokens = lexer.tokens

	def p_string_de(self, t):
		'''main : main2'''
		t[0] = [t[1],]

	def p_string_def2(self, t):
		'''main : main2 main'''
		t[0] = [t[1],] + t[2]

	def p_string_def3(self, t):
		'''main2 : recuo
			| string_s
			| link
			| title'''
		t[0] = [t[1],]

	def p_recuo_def(self, t):
		'recuo : RECUO string_s'
		t[0] = {'type' : 'recuo', 'size' : t[1], 'string' : t[2]}
	
	def p_link_def(self, t):
		'link : LINK_BEGIN string_s LINK_DELIMITER string_s LINK_END'
		t[0] = {'type' : 'link', 'href' : t[2], 'string' : t[4]}

	
	def p_title_def(self, t):
		'title : TITLE STRING TITLE'
		t[0] = {'type' : 'title', 'size' : t[1], 'string' : t[2]}

	def p_string_statement(self, t):
		"string_s : STRING string_s"
		t[0] = t[1] + '\n' + t[2]

	def p_string_def(self, t):
		'string_s : STRING'
		t[0] = t[1]

	def p_error(self, t):
		print "Syntax error at '%s'" % t.value


	def build(self, **kwargs):
		self.parser = yacc.yacc(module=self, **kwargs)

def printDictList(d, color = lambda x : x, lvl = 0):
	"Auxiliar for printing complex structures like list and dictionaries"
	ret = []
	lvl_string = '  '
	if type(d) is dict:
		ret.append('%s{' % (lvl*lvl_string))
		for i in d.iteritems():
			ret.append('%s%s : %s' % ((lvl+1)*lvl_string, green(i[0]), printDictList(i[1], color, lvl + 1)))
		ret.append('%s}' % (lvl*lvl_string))
		return '\n'.join(ret)
	elif type(d) is list:
		ret.append('%s[' % (lvl*lvl_string))
		for l in [printDictList(i, color, lvl + 1) for i in d]:
			ret.append('%s%s' % ((lvl+1)*lvl_string, l))
		ret.append('%s]' % (lvl*lvl_string))
		return '\n'.join(ret)
	elif type(d) is tuple:
		ret.append('%s(' % (lvl*lvl_string))
		for l in [printDictList(i, color, lvl + 1) for i in d]:
			ret.append('%s%s' % ((lvl+1)*lvl_string, l))
		ret.append('%s)' % (lvl*lvl_string))
		return '\n'.join(ret)
	else:
		return color(str(d))

if __name__ == "__main__":
	"""Runs a small test with the parser"""
	import sys
	from stringlexer import StringLexer

	if len(sys.argv) < 2:
		print "first argument must be the string."
		sys.exit(1)

	# Build the lexer
	stringlexer = StringLexer()
	stringlexer.build()
	stringparser = StringParser(stringlexer)
	stringparser.build()
	d = stringparser.parser.parse(sys.argv[1])
	if d:
		print printDictList(d, color = white)

