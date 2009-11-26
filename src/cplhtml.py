#!/usr/bin/env python
# -*- coding: UTF-8 -*-

class CPLHTML():
	"""Class used to generate HTML code from a dictonary with information about a cpl file."""
	def __init__(self, dictionary):
		self.dictionary = dictionary

	def generateHTML(self):
		"""Generate HTML from whole webpageL"""
		d = self.dictionary
		model = [
			'<HTML>',
			'<HEAD> <meta http-equiv="content-type" content="text/html; charset=utf-8" />'
			'<TITLE>' + d['content']['newspaper']['title'] + '</TITLE>',
			'<link rel="stylesheet" type="text/css" href="style.css" media="screen" />',
			self.getJavaScript(),
			'</HEAD>'
			'<BODY>',
			self.getHeader(d),
			self.getTable(d),
			'</BODY>',
			'</HTML>',
			]
		return "\n".join(model)

	def getWindowHTML (self, content):
		"""Gets html from a subwindow"""
		html = ["<HTML><BODY>",
			"<HEAD><link rel='stylesheet' type='text/css' href='styleJanelas.css' /></HEAD>",
			content,
			"</BODY></HTML>"
			]

		return self.removeLineBreaksAndSingleQuotes("".join(html))

	def getHeader(self, d):
		"""Get header of the news website"""
		s = '<div id="header"><div id="logo"> <h1><a>' + d['content']['newspaper']['title']
		if d['content']['newspaper'].has_key("date"):
			s += '</a><p>' + d['content']['newspaper']['date'] + '</p>'
		s += '</div></h1><div id="separador"></div></div>'
		return s

	def removeLineBreaksAndSingleQuotes(self, string):
		"""Replaces \n for \\n and \" for \\' and \' for \\'
		This avoids string problems"""
		string = string.replace("\n", "\\n")
		string = string.replace("'", "\\'")
		string = string.replace('"', "\\'")
		return string

	def getTitle(self, n, news): 
		"""Gets the tag used to print the title of one news headline"""
		#if there is a field 'text'
		#or if there is an item window inside this news
		if d['content'][n[0]].has_key("text") or [i for i in news if i[0] == 'window'] != []: 
			window_content = []
			for l in news:
				if l[0] == 'window':
					if l[2] == 'title':
						l2 = 'title_window' #avoid link in a title in a window
					else:
						l2 = l[2] 
					window_content.append(self.getHTMLTagFromNews((l[1],l2), news))

			#if there is no description of window's content
			#the default form will be used.
			if window_content == []:
				window_content.append(self.getHTMLTagFromNews((n[0], 'title_window'), news))
				window_content.append(self.getHTMLTagFromNews((n[0], 'text'), news))
			window_content = self.getWindowHTML("".join(window_content))
			return '<a href="#" onClick="open_window(\'' + window_content + '\')">' + self.getHTMLTagFromNews((n[0], 'title_window'), news) + "</a>"
		else:
			return self.getHTMLTagFromNews((n[0], 'title_window'), news)


	def getHTMLTagFromNews(self, n, news):
		"""Get the tag from a news item."""
		if n[1] == 'title':
			return "<p>" + self.getTitle(n,news) + '</p>'
		elif n[1] == 'title_window':
			return "<p>" + '<H2>%s</H2>' % d['content'][n[0]]['title'] + '</p>'
		elif n[1] == 'image':
			return "<p>" + '<div id="figura"><img class="escala" src="%s"></img></div>' % d['content'][n[0]].get(n[1], '') + '</p>'
		elif n[1] == 'full_image':
			return "<p>" + '<center><img src="%s"></img></center>' % d['content'][n[0]].get(n[1], '') + '</p>'
		elif n[1] == 'source':
			return "<p>" + '<br><B>Fonte: </B> <a href="%s" target="_blank">%s</a>' % (d['content'][n[0]].get(n[1], ''), d['content'][n[0]].get(n[1])) + '</p>'
		elif n[1] == 'author':
			return "<p>" + '<br><B>Autor: </B> %s' % d['content'][n[0]].get(n[1], '') + '</p>'
		elif n[1] == 'date':
			return "<p>" + '<br><B>Data: </B> %s' % d['content'][n[0]].get(n[1]) + '</p>'
		else:
			return "<p>" + d['content'][n[0]].get(n[1]) + '</p>'
		

	def getNews(self, d, news):
		"""Get all html used to print a single news"""
		result = []
		for n in news:
			if n[0] == 'window':
				continue

			result.append(self.getHTMLTagFromNews(n, news))
		return "\n".join(result)

	def getTable(self, d):
		"""Returns the table printed in main website"""
		num_cols = d["structure"]["format"]["col"]
		current_col = 0
		table = []
		table.append('<TABLE cellSpacing=0 cellPadding=8 width="1024" border=0>')

		table.append("<TR>")
		for i in range(num_cols):
			table.append("<td width='" + str(100/num_cols) + "%'> </td>")
		table.append("</TR>")

		table.append("<TR>")
		#add the news 
		#rethink the way we arrange columns
		for news in d["structure"]["items"]:
			start_col = news["col_range"][0]-1 #here cols starts in 0
			end_col = news["col_range"][1]-1
			#fix col range
			if end_col > num_cols:
				end_en = num_cols
			if start_col > end_col:
				start_col = num_cols
			if end_col < start_col:
				end_col = start_col
			cols = end_col - start_col + 1
			if start_col < current_col:
				if current_col < num_cols:
					table.append("<td colspan='" + str(num_cols - current_col) + "'></td>")
				#add new line
				table.append("</TR>")
				table.append("<TR>")
				current_col = 0

			if current_col != start_col:
				table.append('<td colspan="' + str(start_col - current_col) + '"></td>')
			table.append('<td colspan="' + str(cols) + '">')
			table.append(self.getNews(d, news['item_content']))
			table.append('</td>')
			current_col += cols

		table.append('</TABLE>')

		return "\n".join(table)

	def getJavaScript(self):
		"""returns javascript code"""

		return "\n".join([
			'<script type= "text/javascript"> ',
			'function open_window(content) {'
			"var win = window.open('','headline','width=720,height=500,scrollbars=yes,screenX=400,screenY=200')",
			'var doc = win.document;',
			'doc.open("text/html", "replace");',
			'doc.write(content);',
			'doc.close();',
			'}',
			'</script>'])

if __name__ == "__main__":
	"""Runs a small test with the htmlgenerator"""
	import sys,os
	from cpllexer import CPLLexer
	from cplparser import CPLParser

	if len(sys.argv) < 2:
		print "first argument must be the cpl file."
		sys.exit(1)

	f=open(sys.argv[1])
	cpl_file = f.read()
	f.close()

	# Build the lexer
	cpllexer = CPLLexer()
	cpllexer.build()
	cplparser = CPLParser(cpllexer)
	cplparser.build()
	d = cplparser.parser.parse(cpl_file)
	if not d:
		print "Parsing failed!"
	else:
		cplhtml = CPLHTML(d)
	
	absolute_cpl_file_path = os.path.realpath(sys.argv[1])
	absolute_file_root = '.'.join(absolute_cpl_file_path.split('.')[:-1])  # removing extension
	html_file = '%s.html' % absolute_file_root
	handle = open(html_file, 'w')
	handle.write(cplhtml.generateHTML())
	handle.close()

	print 'Html file saved on "%s"' % html_file


