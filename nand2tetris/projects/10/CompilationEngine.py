
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
	def compileDo(self):
		# todo 还没搞完
		self.outxml("<doStatement>")
		self.indent += 1
		tmp1 = self.tokenizer.next()
		self.outxml(tmp1, 2)

		for x in range(1000):
			tmp2 = self.tokenizer.next()
			self.outxml(tmp2, 2)
			if(tmp2.type == "symbol" and tmp2.val == "("):
				self.compileExpressionList()
			if(tmp2.type == "symbol" and tmp2.val == ")"):
				break
		tmp2 = self.tokenizer.next()
		if(tmp2.type != "identifier"):
			self.error(tmp2)
		tmp3 = self.tokenizer.next()
		if(tmp3.type != "symbol" and tmp3.val != ";"):
			self.error(tmp3)

		self.outxml(tmp1)
		self.outxml(tmp2)
		self.outxml(tmp3)

		self.outxml("</doStatement>")
		self.tokenizer.next()

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
		
		eq = False
		for i in range(MAX):
			tmp = self.tokenizer.next()

			if(i == 0):
				self.outxml(tmp, 2)
			elif(i == 1 and tmp.type == "identifier"):
				self.outxml(tmp, 2)
			elif(i == 2 and tmp.type == "symbol" and tmp.val == "["):
				self.compileExpression()
			elif(i >= 2 and tmp.type == "symbol" and tmp.val == "="):
				eq = True
				self.outxml(tmp, 2)
				self.compileExpression()
		
				break;
			else:
				self.error(tmp)
				break
		tmp = self.tokenizer.next()
		self.outxml(tmp, 2)
		self.indent -= 1
		self.outxml("<letStatement>")
		return
	def compileWhile(self):
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
		return
	def compileReturn(self):
		return
	def compileIf(self):
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
			elif(i == 1 and tmp.type == "keyword" and (tmp.val == "true" or tmp.val == "false"
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
					for i in range(MAX):
						tmp4 = self.tokenizer.next()
						self.outxml(tmp4, 2)
						if(tmp4.type == "symbol" and tmp4.val == "]"):
							break
				else:
					self.outxml(tmp, 2)
			elif(tmp.type == "symbol" and tmp.val == "("):
				# 表达式
				self.compileExpression()
			elif(tmp.type == "symbol" and (tmp.val == ".")):
				# 变量
				self.outxml(tmp,2)
			elif(self.isunaryOp(tmp)):
				self.outxml(tmp,2)
			else:
				self.tokenizer.index(-1)
				break



		self.indent -= 1
		self.outxml("</term>")
		return
	def compileExpressionList(self):
		self.outxml(self.tokenizer.next(), 2)
		endTag = False

		ne = self.tokenizer.advance(1)
		if(ne.type != "symbol" and ne.val != ")"):
			self.outxml("<expressionList>")
			self.indent += 1
			endTag = True
			self.compileExpression()

			for i in range(MAX):
				tmp = self.tokenizer.advance(1)
				if(tmp.type == "symbol" and tmp.val == ","):
					tmp = self.tokenizer.next()
					self.outxml(tmp, 2)
					tmp = self.compileExpression()
				else:
					break
			
		if(endTag):
			self.indent -= 1
			self.outxml("</expressionList>")

		self.outxml(self.tokenizer.next(), 2)
		return 
	def outxml(self, line, type = 1):
		if(type == 1):
			self.xmlfile.write(self.getIndent() +  line  + "\n");
		elif(type == 2):
			self.outxml("<{0}> {1} </{2}>".format(line.type, line.val, line.type))
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