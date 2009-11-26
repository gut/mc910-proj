#!/usr/bin/env python
# -*- coding: UTF-8 -*-

class StringHTML():
	def __init__(self, dictionary):
		self.dictionary = dictionary
	
	def recuar(self, s):
		return '<dl><dd>%s</dd></dl>' % s


	def generateHTML(self):
		d = self.dictionary
		model = []
		for elem in d:
			value = d[elem]
			if elem == 'recuo':
				s = value['string']
				for i in range(value['size']):
					s = self.recuar(s)
				model.append(s)
			elif elem == 'title':
				model.append('<h%(size)s>%(string)s</h%(size)s>' % value)

		return "\n".join(model)

if __name__ == "__main__":
	"""Runs a small test with the htmlgenerator"""
	import sys
	from stringlexer import StringLexer
	from stringparser import StringParser

	if len(sys.argv) < 2:
		print "first argument must be the string."
		sys.exit(1)

	# Build the lexer
	stringlexer = StringLexer()
	stringlexer.build()
	stringparser = StringParser(stringlexer)
	stringparser.build()
	d = stringparser.parser.parse(sys.argv[1])
	if not d:
		print "Parsing failed!"
	else:
		stringhtml = StringHTML(d)
		print stringhtml.generateHTML()

