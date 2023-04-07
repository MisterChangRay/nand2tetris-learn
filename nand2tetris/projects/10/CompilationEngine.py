
import sys
import re
import os
from JackTokenizer import JackTokenizer
from JackTokenizer import Token
import traceback
from pathlib import Path

MAX = 1000000

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
			self.outxml(self.tokenizer.advance(), 2)
			self.indent = self.indent - 1
			self.outxml("</class>")


		return
	def compileClassVarDec(self):
		while True:
			tmp = self.tokenizer.advance(1)
			if(tmp.type == "keyword" and (tmp.val == "static" or tmp.val == "field")):
				self.outxml("<classVarDec>")
				self.indent = self.indent + 1

				self.outxml(self.tokenizer.next(), 2)
				self.outxml(self.tokenizer.next(), 2)
				self.outxml(self.tokenizer.next(), 2)

				for i in range(MAX):
					tmp = self.tokenizer.advance(1)
					if(tmp.type == "symbol" and tmp.val == ","):
						tmp = self.tokenizer.next()
						self.outxml(tmp, 2)
						tmp = self.tokenizer.next()
						self.outxml(tmp, 2)
					else:
						tmp = self.tokenizer.next()
						self.outxml(tmp, 2)
						break

				self.indent = self.indent - 1
				self.outxml("</classVarDec>")
			else:
				break
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
				break
			tmp = self.tokenizer.advance()
			if(i == 0 and tmp.type == "symbol" and tmp.val == "{"):
				self.symbleStack.push(tmp.val)
				self.outxml("<subroutineBody>")
				self.indent += 1
				self.outxml(tmp, 2)
				break
		self.compileVarDec()
		self.compileStatements()

		self.outxml(self.tokenizer.next(), 2)
		self.indent -= 1
		self.outxml("</subroutineBody>")
		return
	def compileSubroutine(self):
		hasEndTag = False
		for i in range(10000):
			if(self.tokenizer. hasMoreCommands()):
				tmp = self.tokenizer.advance()
				if(tmp.type == "keyword" and ( 
					tmp.val == "constructor" or tmp.val == "function" or tmp.val == "method")):

					hasEndTag = True
					self.outxml("<subroutineDec>")
					self.indent = self.indent + 1
					self.outxml(tmp, 2)

					tmp = self.tokenizer.next()
					self.outxml(tmp, 2)

					tmp = self.tokenizer.next()
					self.outxml(tmp, 2)
					self.compileParameterList()
					self.compileSubroutineBody()
					hasEndTag = False

					self.indent = self.indent - 1
					self.outxml("</subroutineDec>")
				else:
					self.tokenizer.index(-1)
					return



		return
	def compileParameterList(self):
		# like (a1, b2)
		tt = self.tokenizer.next()
		self.outxml(tt, 2)
		tmp = self.tokenizer.advance(1)

		
		self.outxml("<parameterList>")	
		self.indent = self.indent + 1

		if(tmp.type == "symbol" and tmp.val == ")"):
			pass
		else:
			self.outxml(self.tokenizer.next(), 2)
			self.outxml(self.tokenizer.next(), 2)
			while True:
				tmp = self.tokenizer.advance(1)
				if(tmp.type == "symbol" and tmp.val == ","):
					self.outxml(self.tokenizer.next(), 2)
					self.outxml(self.tokenizer.next(), 2)
					self.outxml(self.tokenizer.next(), 2)
				else:
					break

		self.indent = self.indent - 1
		self.outxml("</parameterList>")		
		self.outxml(self.tokenizer.next(), 2)
		return
	def compileVarDec(self):
	

		i = -1
		while(True):
			i += 1
			tt = self.tokenizer.advance(1)
			if(tt.type == "keyword" and tt.val == "var"):
				self.outxml("<varDec>")
				self.indent += 1

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
							self.indent -= 1

							self.outxml("</varDec>")
							dotModel = False
							break
					else:
						# print(tmp1.val, tmp2.val)

						if(tmp1.type != "identifier"):
							self.error(tmp1)
						self.outxml(tmp1, 2)
						self.outxml(tmp2, 2)
						if(tmp2.type == "symbol" and tmp2.val == ";"):
							self.indent -= 1
							self.outxml("</varDec>")
							dotModel = False
							break

					if(tmp3.val == ","):
						dotModel = True
							
			else:
				break				


		return

	def compileStatements(self):
		self.outxml("<statements>")
		self.indent +=1
		while(True):
			tmp = self.tokenizer.advance(1)

			print(90000003, tmp.val, tmp.type)
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
				self.indent -= 1
				self.outxml("</statements>")
				break
			else:
				self.error(tmp)

		return
	def compileSubroutineCall(self):
		tmp = self.tokenizer.next()
		self.outxml(tmp, 2)
		tmp = self.tokenizer.advance(1)
		# self.outxml(tmp, 2)
		if(tmp.type == "symbol" and tmp.val == "."):
			# obbbj.method()
			self.outxml(self.tokenizer.next(), 2)
			self.outxml(self.tokenizer.next(), 2)
			self.compileExpressionList()
			tmp = self.tokenizer.advance(1)
			tmp = self.tokenizer.advance(1)
			
		elif(tmp.type == "symbol" and tmp.val == "("):
			# mehotd()
			self.compileExpressionList()
			tmp = self.tokenizer.advance(1)
			tmp = self.tokenizer.advance(1)
			# tmp = self.tokenizer.next()
			# self.outxml(tmp, 2)
		else:
			self.error(tmp)
	def compileDo(self):
		self.outxml("<doStatement>")
		self.indent +=1
		tmp = self.tokenizer.next()
		self.outxml(tmp, 2)
		self.compileSubroutineCall()
		self.outxml(self.tokenizer.next(), 2)
		
		self.indent -=1
		self.outxml("</doStatement>")

		return
	def getSubSet(self, startFlag, endFlag):
		subset = []

		cupleCount = 0
		for i in range(MAX):
			tmp1 = self.tokenizer.advance(1)
			if(tmp1.type == "symbol" and startFlag != None and tmp1.val != startFlag and cupleCount == 0 and i == 0):
					return subset
			if(tmp1.type == "symbol" and tmp1.val == endFlag and cupleCount == 0):
					return subset

			tmp1 = self.tokenizer.next()
			if(tmp1.type ==  "symbol" and startFlag != None and tmp1.val == startFlag):
				cupleCount += 1
			if(tmp1.type ==  "symbol" and startFlag != None and tmp1.val == endFlag):
				cupleCount -= 1
			subset.append(tmp1)


		return subset


	def compileLet(self):
		self.outxml("<letStatement>")
		self.indent += 1
		

		self.outxml(self.tokenizer.next(), 2);
		self.outxml(self.tokenizer.next(), 2);
		tmp = self.tokenizer.next()
		if(tmp.type == "symbol" and tmp.val == "["):
			# a[i] = 1
			self.outxml(tmp, 2)
			self.compileExpression()
			self.outxml(self.tokenizer.next(), 2)
			self.outxml(self.tokenizer.next(), 2)
		else:
			self.outxml(tmp, 2)

		# self.outxml(self.tokenizer.next(), 2)
		tmp = self.tokenizer.advance(1)
		self.compileExpression()
		self.outxml(self.tokenizer.next(), 2)
		tmp = self.tokenizer.advance(1)
		self.indent -= 1
		self.outxml("</letStatement>")
		return
	
	def compileWhile(self):
		self.outxml("<whileStatement>")
		self.indent += 1
		
		tmp = self.tokenizer.next()
		self.outxml(tmp, 2)
		tmp = self.tokenizer.next()
		self.outxml(tmp, 2)
		self.compileExpression()
		tmp = self.tokenizer.next()
		self.outxml(tmp, 2)
		tmp = self.tokenizer.next()
		self.outxml(tmp, 2)
		self.compileStatements()
		tmp = self.tokenizer.next()
		self.outxml(tmp, 2)
	
		self.indent -= 1
		self.outxml("</whileStatement>")
		return
	def compileReturn(self):
		self.outxml("<returnStatement>")
		self.indent += 1

		self.outxml(self.tokenizer.next(), 2)
		tmp = self.tokenizer.advance(1)
		if(tmp.type != "symbol" and tmp.val != ";"):
			self.compileExpression()
		self.outxml(self.tokenizer.next(), 2)

		self.indent -= 1
		self.outxml("</returnStatement>")
		return
	def compileIf(self):
		self.outxml("<ifStatement>")
		self.indent += 1
		self.outxml(self.tokenizer.next(), 2)
		self.outxml(self.tokenizer.next(), 2)
		self.compileExpression()
		self.outxml(self.tokenizer.next(), 2)
		self.outxml(self.tokenizer.next(), 2)
		self.compileStatements()
		self.outxml(self.tokenizer.next(), 2)

		tmp = self.tokenizer.advance(1)
		if(tmp.type == "keyword" and tmp.val == "else"):
			tmp = self.tokenizer.next()
			self.outxml(tmp, 2)
			self.outxml(self.tokenizer.next(), 2)
			self.compileStatements()
			tmp = self.tokenizer.next()
			self.outxml(tmp, 2)
			
		self.indent -= 1
		self.outxml("</ifStatement>")
		return
	def compileExpression(self):
		self.outxml("<expression>")
		self.indent += 1

		self.compileTerm()
		for i in range(MAX):
			tmp = self.tokenizer.advance(1)
			if(self.isOp(tmp)):
				tmp = self.tokenizer.next()
				self.outxml(tmp, 2)
				self.compileTerm()
			else:
				break

		self.indent -= 1
		self.outxml("</expression>")
		return

	def getTermSets(self, aset):
		subsets = []

		if(len(aset) == 0):
			return subsets;
		itemset = []
		for item in aset:
			if(self.isOp(item)):
				subsets.append(itemset)
				subsets.append(item)
				itemset = []
			else:
				itemset.append(item)
		subsets.append(itemset)
		return subsets


	def isEndSymbol (self, endToken):
		res = self.tokenizer.advance(1)
		if(res.type == "symbol" and res.val == endToken):
			return True
		return False

	def isOp (self, tmp):
		res = tmp
		endOfTerm = {
			"+":"+",
			"-":"+",
			"*":"+",
			"/":"+",
			"&":"+",
			"|":"+",
			"<":"+",
			">":"+",
			"=":"+",
		}
		if(res.type == "symbol" and endOfTerm.get(res.val) != None):
			return True

		return False
	def isunaryOp(self, tmp):
		if(tmp.type == "symbol" and (tmp.val == "-" or tmp .val == "~")):
			return True
		else:
			return False

	def getExpiressionList(self, psets, startFlag, endFlag):
		sets = []
		eatSize = 0

		tmps = []
		cupleCount = 0
		for i in range(len(psets)):
			tmpi = psets[i]
			if(tmpi.type == "symbol" and tmpi.val == startFlag):
				if(i == 0):
					sets.append(tmpi)
				else:
					tmps.append(tmpi)
					eatSize+=1
					cupleCount +=1

			elif(tmpi.type == "symbol" and tmpi.val == endFlag):
				if(cupleCount == 0):
					sets.append(tmps)

					sets.append(tmpi)
					break
				else:
					cupleCount -= 1
					tmps.append(tmpi)
					eatSize+=1
			elif(tmpi.type == "symbol" and tmpi.val == ","):
				sets.append(tmpi)
				sets.append(tmps)
				tmps = []
			else:
				tmps.append(tmpi)
				eatSize+=1

		return sets, eatSize


	def compileTerm(self):
		self.outxml("<term>")
		self.indent += 1

		# print(9000000, subsets[1].type, subsets[1].val)
		for i in range(MAX):
			tmp = self.tokenizer.next()

			if(tmp.type == "integerConstant" or tmp.type == "stringConstant"):
				self.outxml(tmp, 2)
				break
			elif( tmp.type == "keyword" and (tmp.val == "true" or tmp.val == "false"
			 or tmp.val == "null" or tmp.val == "this")):
				self.outxml(tmp, 2)
				break
			# 函数调用  var.b()
			# 变量 var
			# 数组 var[i]
			# 表达式 a*(a+b)
			elif(tmp.type == "identifier"):
				nextTmp = self.tokenizer.advance(1)

				if(None != nextTmp and nextTmp.type == "symbol" and nextTmp.val == "("):
					# 函数
					self.outxml(tmp, 2)
					size = self.compileExpressionList()
				elif(None != nextTmp and nextTmp.type == "symbol" and nextTmp.val == "["):
					## 数组
					self.outxml(tmp, 2)
					tmp4 = self.tokenizer.next()
					self.outxml(tmp4, 2)
					self.compileExpression()
					tmp4 = self.tokenizer.next()
					self.outxml(tmp4, 2)
					break
				elif(None != nextTmp and nextTmp.type == "symbol" and nextTmp.val == "."):
					self.outxml(tmp, 2)
				else:
					self.outxml(tmp, 2)
					break
					
			elif(tmp.type == "symbol" and tmp.val == "("):
				# 表达式
				self.outxml(tmp,2)
				self.compileExpression()
				tmp = self.tokenizer.next()
				self.outxml(tmp,2)
				break
			elif(tmp.type == "symbol" and (tmp.val == ".")):
				# 变量
				self.outxml(tmp,2)
			elif(self.isunaryOp(tmp)):
				self.outxml(tmp,2)
				self.compileTerm()
			else:
				self.tokenizer.index(-1)
				break



		self.indent -= 1
		self.outxml("</term>")
		return
	def compileExpressionList(self):
		tmp = self.tokenizer.next()
		self.outxml(tmp, 2)

		self.outxml("<expressionList>")
		self.indent += 1

		ne = self.tokenizer.advance(1)
		if(ne.type != "symbol" or ne.val != ")"):
	
			self.compileExpression()

			for i in range(MAX):
				tmp = self.tokenizer.advance(1)
				if(tmp.type == "symbol" and tmp.val == ","):
					tmp = self.tokenizer.next()
					self.outxml(tmp, 2)
					tmp = self.compileExpression()
				else:
					break
			
		self.indent -= 1
		self.outxml("</expressionList>")

		self.outxml(self.tokenizer.next(), 2)
		return 
	def formatSymbol(self, t):
		res1 = {
			"&" :"&amp;",
			">" :"&gt;",
			"<" :"&lt;"
		}
		if(res1.get(t) != None):
			return res1.get(t)
		return t

	def outxml(self, line, type = 1):
		if(type == 1):
			self.xmlfile.write(self.getIndent() +  line  + "\n");
		elif(type == 2):
			self.outxml("<{0}> {1} </{2}>".format(line.type, self.formatSymbol(line.val), line.type))
		else:
			print("invalid type :" + type)


	def outline(self, line):
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


   
if __name__ == "__main__":
		
	if(len(sys.argv) == 1) :
		print("not found source file to compiler!");
		sys.exit();

	srouceFileOrDir  =sys.argv[1];
	start(srouceFileOrDir)