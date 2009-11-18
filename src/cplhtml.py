#!/usr/bin/env python
# -*- coding: UTF-8 -*-

class CPLHTML():



	def __init__(self, dictionary):
		self.dictionary = dictionary

	def getHeader(self, d):
		s = '<div id="header"> <h1>' + d['content']['newspaper']['title']
		if d['content']['newspaper'].has_key("date"):
			s += ' <p>' + d['content']['newspaper']['date'] + '</p>'
		s += '</div></h1>'
		return s

	def generateHTML(self):
		d = self.dictionary
		model = [
			'<HTML>', 
			'<HEAD> <meta http-equiv="content-type" content="text/html; charset=utf-8" />'
			'<TITLE>' + d['content']['newspaper']['title'] + '</TITLE>',
			'<link rel="stylesheet" type="text/css" href="style/style.css" media="screen" />',
			'<script type= "text/javascript"> </script>',
			'</HEAD>'
			'<BODY>',
			self.getHeader(d),
			'',
			'',
			'',
			'',
			'',
			'',
			'',
			'',
			]
		return "\n".join(model)

