
import sys
import re
import os
from pathlib import Path


class JackTokenizer:
	def xml(self):
		# print(self.sourceTokens)
		outputfile = self.filepath[:len(self.filepath)-5]
		outputfile = outputfile + "T2.xml"
		output = open(outputfile, "w")
		output.write("<tokens>\n")
		while(self.hasMoreCommands()):
			tmp = self.advance()
			if(tmp == "<"):
				tmp = "&lt;"

			output.write("<{0}> {1} </{2}>\n".format(self.tokenType(), tmp, self.tokenType()))
		output.write("</tokens>\n")
		output.close()
		return


	def hasMoreCommands(self):
		self.tokenIndex = self.tokenIndex + 1
		if(self.tokenIndex < len(self.sourceTokens)):
			return  True
		return False


	def nextline(self):
		comment = False
		while True:
			self.linetxt = self.sourcefile.readline()
			if(not self.linetxt):
				return False
			if(re.match(r".*/\*.*", self.linetxt)):
				comment = True
			if(re.match(r".*\*/.*", self.linetxt)):
				comment = False
				continue
			if(comment == True):
				continue


			# 忽略 注释行
			if(len(self.linetxt) > 0):
			  if( re.match(r".*//.*", self.linetxt)):
			    self.linetxt = self.linetxt[0 : self.linetxt.index("//")]

			  self.linetxt = self.linetxt.strip()
			  if(len(self.linetxt) > 0) :
			    return True

		return

	def advance(self):
		# print(self.tokenIndex, len(self.sourceTokens))
		res =  self.sourceTokens[self.tokenIndex]
		return res

	def tokenType(self):
		for keyword in self.tokens['keywords']:
			if(self.advance() == keyword):
				return "keyword"
		for keyword in self.tokens['symbols']:
			if(self.advance() == keyword):
				return "symbol"
		if(re.match(r"^\d+$", self.advance())):
				return "integerConstant"
		if(re.match(r"^\".*\"$", self.advance())):
				return "stringConstant"
		if(re.match(r"^[\da-zA-Z_]+$", self.advance())):
				return "identifier"
		
		return		
	def keyword(self):
		return self.advance()
	def keyword(self):
		return self.advance()
	def symbol(self):
		return self.advance()					
	def identifier(self):
		return self.advance()
	def intval(self):
		return self.advance()
	def stringval(self):
		return self.advance()

	# a=a+b;
	# function test(){}
	# if(a>b)
	# return a-b
	# print
	def parseToken(self, txt):
		terms = re.findall(self.regToken, txt)
		terms = terms[0]
		if(len(terms[0]) > 0):
			return terms[0]
		elif(len(terms[0]) == 0  and terms[1].startswith(terms[1])):
			return terms[1]
		else:
			return None
		



	def __init__(self, filepath):
		self.filepath = filepath
		self.sourcefile = open(filepath, 'r')
		tokenTmp1 = "{|}|\\(|\\)|[|]|\\.|,|;|\\+|-|\\*|/|&|\\||<|>|=|~";
		tokenTmp2 = "class|constructor|function|method|field|var|int|char|boolean|void|true|false|null|this|let|do|if|else|while|return"
		tokenTmp3 = r"({|}|\(|\)|\[|\]|\.|,|;|\+|-|\*|/|&|\||<|>|=|~|class|constructor|function|method|field|var|int|char|boolean|void|true|false|null|this|let|do|if|else|while|return)"
		self.regToken = "(.*?)?" + tokenTmp3 + "(.*?)?" + tokenTmp3 + "?"


		self.tokens = {
			"keywords" : [
				'class', 'constructor', 'function', 'method', 'field', 
				'var', 'int', 'char', 'boolean', 'void', 'true', 'false', 'null', 'this',
				'let', 'do', 'if', 'else', 'while', 'return'
				],
			'symbols' : [
				'{', '}', '(', ')', '[', ']', '.', ',', ';', 
				'+', '-', '*', '/', 
				'&', '|',
				'<', '>', '=', '~'
			]
		}
		self.sourceTokens = []
		self.tokenIndex = -1

		# 读取每行代码, 进行token分割操作
		while self.nextline():
			while True:
				res = self.parseToken(self.linetxt)

				if(None == res):
					break

				if(len(res.strip()) > 0):
					# print( re.match(r"^\".*", res) , re.match(r".+\s.+", res),res)
					if(None == re.match(r"^\".*", res) and re.match(r".+\s.+", res)):
						tmp = re.split(r"\s", res)
						for tmp1 in tmp:
							if(len(tmp1.strip()) == 0):
								continue
							self.sourceTokens.append(tmp1)
					else:
						self.sourceTokens.append(res.strip())


				sindex = self.linetxt.index(res) + len(res)
				self.linetxt = self.linetxt[sindex:]
				if(len(self.linetxt) == 0 ):
					break

		return