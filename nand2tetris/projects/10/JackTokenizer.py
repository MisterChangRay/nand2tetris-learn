
import sys
import re
import os
from pathlib import Path

class Token:
	def __init__(self, val, type):
		self.val = val
		self.type = type
		return

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

			output.write("<{0}> {1} </{2}>\n".format(self.tokenType(), tmp.val, self.tokenType()))
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

	def parserLine(self, line, start, end, alen, res):

		if( start >= end or (start + alen) > end ):
			return

		txt = line[start:start+alen]

		# print("txt", txt)
		if(re.match(r"^\s$", txt)):
			self.parserLine(line, start+1, end, 1, res)
			return

		isend = line[start+(alen-1) : start+alen]

		if(txt.startswith("\"") ):
			
			tmp = line[start +1:]
			i = tmp.find("\"");
			res.append(Token(line[start+1:start+i+1], self.getType(line[start:start+i])))
			# print(tmp, i, start, end, line)

			self.parserLine(line, start + i + 2 , end, 1, res)

		elif(self.tokenTmp1.find(txt) > -1):
			txt2 = txt
			if(txt2 == "<"):
				txt2 = "&lt;"

			res.append(Token(txt2, self.getType(txt)))
			self.parserLine(line, start + alen, end, 1, res)
		elif(self.tokenTmp1.find(isend) > -1 or re.match(r"^\s$", isend)):
			tv = txt[0:len(txt)-1]
			res.append(Token(tv, self.getType(tv)))
			next = start + alen

			if(False == re.match(r"^\s$", isend)):
				res.append(Token(isend, self.getType(isend)))
			else:
				next = next - 1
			self.parserLine(line, next, end, 1, res)
		else:
			self.parserLine(line, start, end, alen + 1, res)






	def __init__(self, filepath):
		self.filepath = filepath
		self.sourcefile = open(filepath, 'r')
		self.tokenTmp1 = "{}()[].,;+-*/&|<>=~";
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

		# 读取每行代码, 进行token分割操作
		while self.nextline():
			startline = 0
			offset = 0;
			endline = len(self.linetxt)
			self.parserLine(self.linetxt, 0, endline, 1, self.sourceTokens)
		return




