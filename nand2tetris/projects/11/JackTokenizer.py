
import sys
import re
import os
from pathlib import Path

class Token:
	def __init__(self, val, type, lineno, linetxt):
		self.val = val
		self.type = type
		self.lineno = lineno
		self.linetxt = linetxt
		return

class JackTokenizer:
	
	def xmltoken(self):
		# print(self.sourceTokens)
		outputfile = self.filepath[:len(self.filepath)-5]
		outputfile = outputfile + "T2.xml"
		output = open(outputfile, "w")
		output.write("<tokens>\n")
		while(self.hasMoreCommands()):
			tmp = self.advance()
			if(tmp == "<"):
				tmp = "&lt;"

			output.write("<{0}> {1} </{2}>\n".format(self.tokenType(), tmp.val, self.tokenType()))
		output.write("</tokens>\n")
		output.close()
		self.tokenIndex = -1
		return
	def index(self, i):
		self.tokenIndex += i
		return
	
	def next(self):
		self.tokenIndex = self.tokenIndex + 1
		if(self.tokenIndex >= len(self.sourceTokens)):
			print("code is invalid")
			exit()

		res =  self.sourceTokens[self.tokenIndex]
		return res
			

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
			self.lineno += 1
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


	def advance(self, i = 0):
		# print(self.tokenIndex, len(self.sourceTokens))
		j = self.tokenIndex + i
		if(j >= len(self.sourceTokens)):
			return None

		res =  self.sourceTokens[j]
		return res

	def tokenType(self):
		res =  self.sourceTokens[self.tokenIndex]
		return res.type

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
		

	def getType(self, txt):
		if(txt.startswith("\"")):
			return "stringConstant"
		if(re.match("^\\d+$", txt)):
			return "integerConstant"
		if(self.tokenTmp1.find(txt) > -1):
			return "symbol"
		if(self.tokenTmp2.find("|" + txt + "|") > -1):
			return "keyword"
		return "identifier"

	def parserLine(self, line, start, end, alen, res, lineno):

		if( start >= end or (start + alen) > end ):
			return

		txt = line[start:start+alen]

		# print("txt", txt)
		if(re.match(r"^\s$", txt)):
			self.parserLine(line, start+1, end, 1, res, lineno)
			return

		isend = line[start+(alen-1) : start+alen]

		if(txt.startswith("\"") ):
			
			tmp = line[start +1:]
			i = tmp.find("\"");
			res.append(Token(line[start+1:start+i+1], self.getType(line[start:start+i]), lineno, line))
			# print(tmp, i, start, end, line)

			self.parserLine(line, start + i + 2 , end, 1, res, lineno)

		elif(self.tokenTmp1.find(txt) > -1):
			txt2 = txt
			# if(txt2 == "<"):
			# 	txt2 = "&lt;"

			res.append(Token(txt2, self.getType(txt), lineno, line))
			self.parserLine(line, start + alen, end, 1, res, lineno)
		elif(self.tokenTmp1.find(isend) > -1 or re.match(r"^\s$", isend)):
			tv = txt[0:len(txt)-1]
			res.append(Token(tv, self.getType(tv), lineno, line))
			next = start + alen

			if(False == re.match(r"^\s$", isend)):
				res.append(Token(isend, self.getType(isend), lineno, line))
			else:
				next = next - 1
			self.parserLine(line, next, end, 1, res, lineno)
		else:
			self.parserLine(line, start, end, alen + 1, res, lineno)






	def __init__(self, filepath):
		self.filepath = filepath
		self.sourcefile = open(filepath, 'r')
		self.tokenTmp1 = "{}()[].,;+-*/&|<>=~"
		self.tokenTmp2 = "|class|constructor|function|method|field|static|var|int|char|boolean|void|true|false|null|this|let|do|if|else|while|return|"


		self.tokens = {
			"keywords" : [
				'class', 'constructor', 'function', 'method', 'field',  'static',
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
		self.lineno = 0

		# 读取每行代码, 进行token分割操作
		while self.nextline():
			startline = 0
			offset = 0;
			endline = len(self.linetxt)
			self.parserLine(self.linetxt, 0, endline, 1, self.sourceTokens, self.lineno)
		return




