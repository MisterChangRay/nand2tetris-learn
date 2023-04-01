
import sys
import re
import os
from JackTokenizer import JackTokenizer
import traceback
from pathlib import Path

class SymbolStack:
	stack = []
	def push(self,t):
			self.stack.append(t)
	def pop(self):
		if(len(self.stack) == 0):
			return None
		return self.stack.pop()
	def equal(self, tmp):
		if(tmp.type != "symbol"):
			return False 
		tmp = tmp.val
		res = self.pop()
		if(res == None):
			return True
		if(res == "{" and tmp == "}"):
			return True
		if(res == "(" and tmp == ")"):
			return True
		return False

	def __init__(self):
		self.tmp = []



class CompilationEngine:

	def error(self, tmp = None):
		if(tmp == None) :
			print("has no more code to parse!!!")	
			return

		print("error occur with line {0}: {1}".format(tmp.lineno, tmp.linetxt))
		for line in traceback.format_stack():
			print(line.strip())
		exit()
		return
	def getIndent(self):
		res = ""
		for x in range(self.indent):
			res = res + "  "
		return res

	def compileClass(self):
		for i in range(5):
			if(self.tokenizer. hasMoreCommands()):
				tmp = self.tokenizer.advance()
				if(i ==0 and tmp.type == "keyword" and tmp.val == "class"):
					self.outxml("<class>")
					self.indent = self.indent + 1
					self.outxml(tmp, 2)
				elif(i == 1 and tmp.type == "identifier"):
					self.outxml(tmp, 2)
				elif(i == 2 and tmp.type == "symbol" and tmp.val == "{"):
					self.symbleStack.push(tmp.val)
					self.outxml(tmp, 2)
					break
				else:
					self.error(tmp)
		self.compileClassVarDec()
		self.compileSubroutine()

		if(self.checkCouple("}")):
			self.indent = self.indent - 1
			self.outxml("</class>")
			self.outxml(tmp, 2)


		return
	def compileClassVarDec(self):
		# self.outxml("<classVarDec>")
		# self.indent = self.indent + 1

		# self.indent = self.indent - 1
		# self.outxml("</classVarDec>")
		return
	def checkCouple(self, t):
		if(False == self.tokenizer. hasMoreCommands()):
			self.error()
		tmp = self.tokenizer.advance()
		if(self.symbleStack.equal(tmp)):
			return True
		else:
			self.error(tmp)


	def compileSubroutineBody(self):
		i = -1
		while(True):
			i += 1
			if(False == self.tokenizer. hasMoreCommands()):
				self.error()
			tmp = self.tokenizer.advance()
			if(i == 0 and tmp.type == "symbol" and tmp.val == "{"):
				self.symbleStack.push(tmp.val)
				self.outxml("<subroutineBody>")
				self.indent += 1
				self.outxml(tmp, 2)
				break
		self.compileVarDec()
		self.compileStatements()

		if(self.checkCouple("}")):
				self.outxml("</subroutineBody>")
				self.outxml(tmp, 2)



		print(tmp.val)
		return
	def compileSubroutine(self):
		for i in range(10):
			if(self.tokenizer. hasMoreCommands()):
				tmp = self.tokenizer.advance()
				if(i == 0 and tmp.type == "keyword" and ( 
					tmp.val == "constructor" or tmp.val == "function" or tmp.val == "method")):

					self.outxml("<subroutineDec>")
					self.indent = self.indent + 1
					self.outxml(tmp, 2)
				elif(i == 1 and (tmp.val == "void" or tmp.type == "symbol")):
					self.outxml(tmp, 2)
				elif(i == 2 and (tmp.type == "identifier")):
					self.outxml(tmp, 2)
					self.compileParameterList()
					self.compileSubroutineBody()
					break
				else:
					self.error(tmp)
					return

		return
	def compileParameterList(self):
		# like (a1, b2)
		for i in range(1000):
			if(self.tokenizer. hasMoreCommands()):
				tmp = self.tokenizer.advance()
				if(i == 0 and tmp.type == "symbol" and ( tmp.val == "(" )):
					self.symbleStack.push(tmp.val)
					self.outxml(tmp, 2)
					self.outxml("<paramterList>")
					self.indent = self.indent + 1
				elif(i > 0 and tmp.type == "symbol" and ( tmp.val == ")" )):
					self.indent = self.indent - 1
					self.outxml("</paramterList>")			
					break			
				else:
					argsLen = 0
					for j in range(100):
						if(self.tokenizer.advance(1).val == ")") :
							break
						if(j == 0):
							tmp1 = tmp;
						else:
							if(self.tokenizer. hasMoreCommands()):
								tmp1 = self.tokenizer.advance()	

						if(self.tokenizer. hasMoreCommands()):
							tmp2 = self.tokenizer.advance()
						if(j ==0 and tmp2.type == "identifier" and (tmp1.type == "identifier" or tmp1.type == "keyword")):
							self.outxml(tmp1, 2)
							argsLen += 1
							self.outxml(tmp2, 2)
							argsLen += 1
						if(j > 0):
							if(self.tokenizer. hasMoreCommands()):
								tmp3 = self.tokenizer.advance()

							if(tmp1.type != "symbol" or tmp3.type != "identifier" or(tmp2.type != "identifier" and tmp2.type != "keyword")):
								self.error(tmp3)
								return

							self.outxml(tmp1, 2)
							argsLen += 1
							self.outxml(tmp2, 2)
							argsLen += 1
							self.outxml(tmp3, 2)
							argsLen += 1

		return
	def compileVarDec(self):
		self.outxml("<varDec>")
		self.indent += 1

		i = -1
		while(True):
			i += 1
			tt = self.tokenizer.advance(1);
			if(tt.type == "keyword" and tt.val == "var"):
				tmp = self.tokenizer.next()
				self.outxml(tmp, 2)

				dotModel = False
				for x in range(1000):
					tmp1 = self.tokenizer.next()
					tmp2 = self.tokenizer.next()

					if(dotModel == False):
						tmp3 = self.tokenizer.next()
						if(tmp1.type != "identifier" and tmp1.type != "keyword"):
							self.error(tmp1)
						if(tmp2.type != "identifier"):
							self.error(tmp2)
						# print(tmp1.val, tmp2.val, tmp3.val)
						if(tmp3.type != "symbol" and (tmp3.val != "," and tmp3.val != ";")):
							self.error(tmp3)
						self.outxml(tmp1, 2)
						self.outxml(tmp2, 2)
						self.outxml(tmp3, 2)

						if(tmp3.type == "symbol" and tmp3.val == ";"):
							dotModel = False
							break
					else:
						# print(tmp1.val, tmp2.val)

						if(tmp1.type != "identifier"):
							self.error(tmp1)
						self.outxml(tmp1, 2)
						self.outxml(tmp2, 2)
						if(tmp2.type == "symbol" and tmp2.val == ";"):
							dotModel = False
							break


					if(tmp3.val == ","):
						dotModel = True
							
			else:
				break				

		self.indent -= 1
		self.outxml("</varDec>")
		return

	def compileStatements(self):
		while(True):
			tmp = self.tokenizer.advance(1)
			if(tmp.type == "keyword" and tmp.val == "do"):
				self.compileDo()
			elif(tmp.type == "keyword" and tmp.val == "let"):
				self.compileLet()
			elif(tmp.type == "keyword" and tmp.val == "if"):
				self.compileIf()
			elif(tmp.type == "keyword" and tmp.val == "while"):
				self.compileWhile()
			elif(tmp.type == "keyword" and tmp.val == "return"):
				self.compileReturn()
			elif(tmp.type == "symbol" and tmp.val == "}"):
				break
			else:
				self.error(tmp)
		return
	def compileDo(self):
		return
	def compileLet(self):
		return
	def compileWhile(self):
		return
	def compileReturn(self):
		return
	def compileIf(self):
		return
	def compileExpression(self):
		return
	def compileTerm(self):
		return
	def compileExpressionList(self):
		return
	def outxml(self, line, type = 1):
		if(type == 1):
			self.xmlfile.write(self.getIndent() +  line  + "\n");
		elif(type == 2):
			self.outxml("<{0}> {1} </{2}>".format(line.type, line.val, line.type))
		else:
			print("invalid type :" + type)


	def outline(line):
		self.outputfile.write(line  + "\n");
	def __init__(self, inputfile, outputfile):
		self.inputfile =  open(inputfile, "r");
		self.outputfile = open(outputfile, "w");
		self.symbleStack = SymbolStack()
		xmlfilepath = self.inputfile.name[:len(self.inputfile.name)-5]
		xmlfilepath = xmlfilepath + "2.xml"
		self.xmlfile = open(xmlfilepath, "w")

		self.indent = 0
		self.tokenizer =  JackTokenizer(inputfile)
		self.tokenizer.xmltoken()
		self.compileClass()


def filename(file):
	return Path(file).stem

def parseFile(file):
	outputfile = file[:len(file)-5]
	outputfile = outputfile + ".vm"
	CompilationEngine(file, outputfile)
	return

def scanfiles(dir):
	for filepath,dirnames,filenames in os.walk(dir):
		for filename in filenames:
			if(filename.endswith(".jack")):

				parseFile(os.path.join(filepath, filename))
	return


def start(srouceFileOrDir):
	# file.write(stringb)

	srouceFileOrDir = os.path.realpath(srouceFileOrDir)
	if(srouceFileOrDir.endswith("\\")):
		srouceFileOrDir = srouceFileOrDir[0: len(srouceFileOrDir)  - 1]

	if(os.path.isfile(srouceFileOrDir)):
		if(False == srouceFileOrDir.endswith(".jack")) :
			print("invalid file -> " + srouceFileOrDir)
			return


	if(os.path.isfile(srouceFileOrDir)):
			parseFile(srouceFileOrDir)
	elif(os.path.isdir(srouceFileOrDir)):
		scanfiles(srouceFileOrDir)
	else:
		print(" invalid file or dir")

	return


if(len(sys.argv) == 1) :
  print("not found source file to compiler!");
  sys.exit();

srouceFileOrDir  =sys.argv[1];
start(srouceFileOrDir)
