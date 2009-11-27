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
		for l in d:
			for elem in l:
				if type(elem) is str:
					model.append(elem)
				elif type(elem) is dict:
					if elem['type'] == 'recuo':
						s = elem['string']
						for i in range(elem['size']):
							s = self.recuar(s)
						model.append(s)
					elif elem['type'] == 'title':
						model.append('<h%(size)s>%(string)s</h%(size)s>' % elem)
					elif elem['type'] == 'link':
						model.append('<a href="%(href)s">%(string)s</a>' % elem)

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

