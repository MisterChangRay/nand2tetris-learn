
import sys
import re
import os
from JackTokenizer import JackTokenizer
from JackTokenizer import Token
import traceback
from pathlib import Path


class AssemberEngine:
	def writePop(self, *args):
		self.outline("pop", args)
		pass
	def writePush(self, *args):
		self.outline("push", args)
		pass
	def writeReturn(self):
		pass
	def writeLabel(self, label):
		self.outline("({0})".format(label))
		pass
	def writeGoto(self):
		pass
	def writeArithmetic(self):
		pass
	def writeCall(self, *args):
		self.outline("call", args)
		
		pass
	def writeFunction(self):
		pass
	def flsh(self):
		pass
	def outline(self, keywrod, *args):
		tmp = keywrod + " "
		for i in args:
			tmp += str(i) + " "

		self.vmfile.write(tmp + "\n")
		return
	def __init__(self, outfile):
		self.vmfile = open(outfile, "w")
		pass

class SymbolTree:
	# type : arguments, var, static, field, constructor|function|method
	def add(self, name, dataType, type):
		# constructor|function|method
		table = self.getDict(name, type)
		
		if(None != table.get(name)):
			raise ValueError(f"compilation type error：identifier has already defined! -> " + name)
		
		table[name] = Symbol(name, dataType, type, self.countType(table, type))

	def countType(self,table, type):
		count = 0
		for k in table:
			if(table[k].type == type):
				count += 1
		return count
	
	def getDict(self, name, type):
		if(type == "constructor" or type == "function" or type == "method"):
			return self.tables.get("fn")
		return self.tables["var"]

	def getSymbol(self, name, type):
		table = self.tables["fn"]
		if(type == "var"):
			table = self.tables["var"]
		return table.get(name)
	

	def remove(self):
		self.parent.next.remove(self)
		return
	def addChild(self, name, child):
		self.next[name] = child
		child.parent = self
		pass

	def __init__(self):
		self.tables = {
			"fn": dict(),
			"var" : dict()
		}
		self.parent = None
		self.next = dict()
		pass
class Symbol:
	def __init__(self, name, dataType, type, index):
		self.name = name
		self.dataType = dataType
		self.type = type
		self.index = index
		pass
	

def CompilationEngine(filepath, symbolTree:SymbolTree, assemberEngine:AssemberEngine):
	def tag_indent(tagName, expand_none = False):
		def wapper(fn):
			def helper( tokens, symbolTree, nedent, *args, **kwargs):
				res = []
				takeTokens, tokens, symbolTree = fn( tokens, symbolTree, nedent + 1, *args, **kwargs)
				if(takeTokens == None and expand_none == True):
					takeTokens = []
				if(takeTokens == None):
					return None, tokens, symbolTree
				else:
					t = Token(None, tagName, None, None)
					t.tag = doIndent(nedent, "<{0}>".format(tagName)) 
					res.append(t)
					res += [] if (None == takeTokens) else takeTokens

					t = Token(None, tagName, None, None)
					t.tag = doIndent(nedent, "</{0}>".format(tagName)) 
					res.append(t)
				return res, tokens, symbolTree
			return helper
		return wapper
	
	def delay_token_application(f):
		"""Decorate f to make it a "delayed" function waiting for tokens"""
		def helper(*args, **kwargs):
			def f1(tokens, symbolTree):
				res = f( tokens, symbolTree, *args, **kwargs)
				# if(len(res) <= 2) :
				# 	print(333)
				return res
			return f1
		return helper

	
	def doIndent( i, token):
		return (" " * 2) * i + token
	
	def take(type, tokens, n_indent, val = None, err = True):
		token = tokens[0]
		tmp = token.tag
		if(None != val):
			strs = val.split("|")
			hasErr = True
			for key in strs:
				if(key == "OR"):
					key = "|"
				if(tokenFormat(type, key)  == tmp):
					hasErr = False
					break
			if(hasErr):
				if(err):
					raise ValueError(f"compilation val error! except:" + tmp)
				return None, tokens
		token.tag = doIndent(n_indent, tmp)
		return [token], tokens[1:]
	@delay_token_application
	def takeKeyword(  tokens, symbolTree, n_indent, val, err):
		# "class|constructor|function|method|field|static|var|int|char|boolean|void|true|false|null|this|let|do|if|else|while|return"
		res =  take("keyword", tokens, n_indent, val, err) 
		return res[0], res[1], symbolTree
		
	@delay_token_application
	def takeIdentifier( tokens, symbolTree, n_indent):
		res = take("identifier", tokens, n_indent)
		return res[0], res[1], symbolTree
	
	@delay_token_application
	def takeSymbol( tokens, symbolTree, n_indent, val, err = True):
		res =  take("symbol", tokens, n_indent, val, err)
		return res[0], res[1], symbolTree
	
	
	
	# int, char, boolean, identifer , void
	@delay_token_application
	def takeType(tokens, symbolTree, indent, includeVoid=False, err = True):
		token = tokens[0]
		tmp = token.tag

		if(tmp.find( "identifier") > 0):
			token.tag = doIndent( indent, tmp )
			return [token], tokens[1:], symbolTree
		elif(tmp .find( "keyword") > 0):
			if(tmp == tokenFormat("keyword", "int") or 
      			tmp == tokenFormat("keyword", "char") or 
				tmp == tokenFormat("keyword", "boolean")):
				
				token.tag = doIndent( indent, tmp )
				return [token], tokens[1:], symbolTree
			if(tmp == tokenFormat("keyword", "void") ):

				token.tag = doIndent( indent, tmp )
				return [token], tokens[1:], symbolTree
		elif(err == True):
			raise ValueError(f"compilation type error! except: type or identifier ")
			
		return None, tokens, symbolTree

	@delay_token_application
	def applyTakers(tokens, symbolTree,  *tasks,  breakNone=True):
		taked = []
		for task in tasks:
			res, tokens, symbolTree = task(tokens, symbolTree)
			if(res == None):
				if(breakNone) :
					break
				else:
					continue
			else:
				taked += res
				
		return taked if(len(taked) > 0) else None, tokens, symbolTree
	
	@delay_token_application
	def takeUtilNone(tokens, symbolTree, *tasks):
		i = 0
		taked = []
		ended = False
		while True:
			for task in tasks:
				res,tokens, symbolTree  = task(tokens, symbolTree)
				
				if(res == None):
					ended = True
					break
				else:
					taked += res
					i+=1
			if(ended == True):
				break
		return taked, tokens, symbolTree
	
	@delay_token_application
	@tag_indent("classVarDec")
	def compileClassVarDec(tokens, symbolTree, n_indent):
		res = applyTakers(
			takeKeyword(n_indent, "static|field", err=False),
			takeType(n_indent),
			takeIdentifier(n_indent),
			takeUtilNone(
				takeSymbol( n_indent, ",", False),
				takeIdentifier( n_indent)
			),
			takeSymbol( n_indent, ";")
		)(tokens,symbolTree)

		readTokens = res[0]
		if(None == readTokens or len(readTokens) == 0):
			return res[0], res[1], symbolTree

		# if(compileStep == 0):
		# 	# generator symbol table
		# 	type = readTokens[0].val
		# 	dataType = readTokens[1].val
		# 	symbolTree.add(readTokens[2].val, dataType, type)
			
		# 	i = 2
		# 	j = len(readTokens) - 2
		# 	while i < j:
		# 		symbolTree.add(readTokens[i + 2].val, dataType, type)
		# 		i += 2
		return res[0], res[1], symbolTree

	
	@delay_token_application
	@tag_indent("subroutineDec")
	def compileSubroutineDec(tokens, symbolTree, n_indent, tokenOfClass):
		# if(compileStep == 0):
		# 	tmp = SymbolTree()
		# 	tmp = symbolTree.getNext()

		res = applyTakers(
			takeKeyword(n_indent, "constructor|function|method", err=False),
			takeType(n_indent, True),
			takeIdentifier(n_indent),
			takeSymbol(n_indent, "("),
			takeParameterList(n_indent),
			takeSymbol(n_indent, ")"),
			takeSubroutineBody(n_indent)
		)(tokens,symbolTree)

		# if(res[0] != None and len(res[0]) > 0):
		# 	fnType = res[0][0].val
		# 	fnReturnType = res[0][1].val
		# 	fnName = res[0][2].val

		# 	if(compileStep == 0):
		# 		# 1.生成符号表
		# 		symbolTree.add(fnName, fnReturnType, fnType)
		# 		symbolTree.addChild(fnName, tmp)
		# 	if(compileStep == 1):
		# 		# 2. 生成vm代码
		# 		assemberEngine.writeLabel("{0}.{1}".format(tokenOfClass.val, fnName))

		return res[0], res[1], symbolTree
		
	@delay_token_application
	@tag_indent("parameterList", expand_none=True)
	def takeParameterList(tokens, thisSymbol:SymbolTree, n_indent):
		res = applyTakers(
			takeType(n_indent, False, False),
			takeIdentifier(n_indent),
			takeUtilNone(
				takeSymbol(n_indent, ",", err=False),
				takeType(n_indent),
				takeIdentifier(n_indent)
			)
		)(tokens,symbolTree)
	
	
		readTokens = res[0]
		if(None == readTokens or len(readTokens) == 0):
			return res[0], res[1], thisSymbol

		# if(compileStep == 0):
		# 	# generator var symbol table
		# 	type = readTokens[0].val
		# 	name = readTokens[1].val
		# 	thisSymbol.add(name, type, "arguments")
			
		# 	i = 2
		# 	j = len(readTokens) - 2
		# 	while i < j:
		# 		type = readTokens[i + 1].val
		# 		name = readTokens[i + 2].val
		# 		thisSymbol.add(name, type, "arguments")
		# 		i += 3
	
		# 	pass
		return res[0], res[1], thisSymbol
	

	@delay_token_application
	@tag_indent("subroutineBody")
	def takeSubroutineBody(tokens, thisSymbol:SymbolTree, n_indent):
		res = applyTakers(
			takeSymbol(n_indent, "{"),
			takeUtilNone(
				takeVarDec(n_indent),
			),
			takeStatements(n_indent),
			takeSymbol(n_indent, "}")
		)(tokens,symbolTree)

		return res[0], res[1], thisSymbol


	@delay_token_application
	@tag_indent("varDec")
	def takeVarDec(tokens, thisSymbol:SymbolTree, n_indent):
		res = applyTakers(
			takeKeyword(n_indent, "var", err=False),
			takeType(n_indent, False),
			takeIdentifier(n_indent),
			takeUtilNone(
				takeSymbol(n_indent, ",", err=False),
				takeIdentifier(n_indent)
			),
			takeSymbol(n_indent, ";")
		)(tokens,symbolTree)
		
		readTokens = res[0]
		if(None == readTokens or len(readTokens) == 0):
			return res[0], res[1], thisSymbol
		
		# if(compileStep == 0):
		# 	# generator symbol table
		# 	type = readTokens[0].val
		# 	dataType = readTokens[1].val
		# 	thisSymbol.add(readTokens[2].val, dataType, type)
			
		# 	i = 2
		# 	j = len(readTokens) - 2
		# 	while i < j:
		# 		thisSymbol.add(readTokens[i + 2].val, dataType, type)
		# 		i += 2
		return res[0], res[1], thisSymbol
	@delay_token_application
	@tag_indent("statements")
	def takeStatements(tokens, thisSymbol:SymbolTree, n_indent):
		res = []
		while(True):
			token = tokens[0]
			tmp = token.tag
			if(tmp == tokenFormat("keyword", "let")):
				tmp, tokens, thisSymbol1 = takeStatementLet( n_indent)(tokens, thisSymbol)
				res += tmp
			elif(tmp == tokenFormat("keyword", "if")):
				tmp, tokens, thisSymbol1 =  takeStatementIf( n_indent)(tokens, thisSymbol)
				res += tmp
			elif(tmp == tokenFormat("keyword", "while")):
				tmp, tokens, thisSymbol1 =  takeStatementWhile( n_indent)(tokens, thisSymbol)
				res += tmp
			elif(tmp == tokenFormat("keyword", "do")):
				tmp, tokens, thisSymbol1 =  takeStatementDo( n_indent)(tokens, thisSymbol)
				res += tmp
			elif(tmp == tokenFormat("keyword", "return")):
				tmp, tokens, thisSymbol1 =  takeStatementReturn( n_indent)(tokens, thisSymbol)
				res += tmp
			else:
				break
		return res, tokens, thisSymbol			


	@delay_token_application
	@tag_indent("letStatement")
	def takeStatementLet(tokens,  thisSymbol:SymbolTree, n_indent):
		res = applyTakers(
		     	takeKeyword(n_indent, "let", err=True),
			    takeIdentifier(n_indent),
			    applyTakers(
		   			takeSymbol(n_indent, "[", False),
					takeExpression(n_indent),
					takeSymbol(n_indent, "]")
		   		),
				takeSymbol(n_indent, "="),
				takeExpression(n_indent),
				takeSymbol(n_indent, ";"),

				breakNone=False
			 )(tokens,symbolTree )
		
		# if(len(res) > 0):
		# 	if(compileStep == 1):
		# 		# generator vm code
		# 		varname = tokens[1].val
		# 		vardec = thisSymbol.getSymbol(varname, "var")

		# 		addr = vardec.index
		# 		if(tokens[2].type == "symbol" and tokens[2].val == "["):
		# 			assemberEngine.writePop("temp", 0)
		# 			assemberEngine.writePush("constant", addr)
		# 			assemberEngine.writeCall("add")
		# 			assemberEngine.writePop("that")
		# 			assemberEngine.writePush("temp", 0)
					
		# 		assemberEngine.writePush("temp", 0)
		# 		assemberEngine.writePop("that")
		# 		pass
		return res[0], res[1], thisSymbol
	
	@delay_token_application
	@tag_indent("expression")
	def takeExpression(tokens, thisSymbol:SymbolTree, n_indent):
		res = applyTakers(
			takeTerm(n_indent),
			takeUtilNone(
				takeOp(n_indent, err = False),
				takeTerm(n_indent)
			)
		)(tokens,symbolTree)

		if(len(res) > 1):
			
			pass

		return res[0], res[1], thisSymbol
		pass
	@delay_token_application
	@tag_indent("ifStatement")
	def takeStatementIf(tokens, thisSymbol:SymbolTree , n_indent):
		res = applyTakers(
			takeKeyword(n_indent, "if", err=True),
			takeSymbol(n_indent, "("),
			takeExpression(n_indent),
			takeSymbol(n_indent, ")"),
			takeSymbol(n_indent, "{"),
			takeStatements(n_indent),
			takeSymbol(n_indent, "}"),
			applyTakers(
				takeKeyword(n_indent, "else", err=False),
				takeSymbol(n_indent, "{"),
				takeStatements(n_indent),
				takeSymbol(n_indent, "}"),
			)
		)(tokens,symbolTree)
		return res[1], res[1], thisSymbol

	@delay_token_application
	@tag_indent("term")
	def takeTerm(tokens, thisSymbol:SymbolTree, n_indent):
		token = tokens[0]
		tmp = token.tag
		if(tmp.find("<integerConstant>") != -1 or tmp.find("<stringConstant>")  != -1 or tmp.find("<keyword>" )  != -1):
			token.tag = doIndent(n_indent, tmp)

			if(tmp.find("<integerConstant>") != -1):
				assemberEngine.writePush("constant", token.val)
			if(tmp.find("<stringConstant>") != -1):
				for i in range(len(token.val)):
					c = token.val[i]
					assemberEngine.writePush("constant", ord(c))
					assemberEngine.writeCall("String.appendChar", 2)
			 
			return [token], tokens[1:], thisSymbol
		elif(tmp.find("<identifier>") != -1):
			token1 = tokens[1]
			tmp1 = token1.tag
			if(tmp1.find("[") != -1):
				# variable a[b]
				res = applyTakers(
					takeIdentifier(n_indent),
					takeSymbol(n_indent, "["),
					takeExpression(n_indent),
					takeSymbol(n_indent, "]")
				)(tokens,symbolTree)
				return res[0], res[1], thisSymbol
				pass
			elif(tmp1.find("(") != -1):
				# method a()
				res = takeSubroutineCall( n_indent)(tokens, thisSymbol)
				return res[0], res[1], thisSymbol
			elif(tmp1.find(".") != -1):
				# method a.b()
				res= takeSubroutineCall( n_indent)(tokens, thisSymbol)
				return res[0], res[1], thisSymbol
			else:
				# var name
				token.tag = doIndent(n_indent, tmp)
				return [token], tokens[1:], thisSymbol
		elif(tmp.find("-") != -1 or tmp.find("~") != -1):
			res = applyTakers(
				takeUnaryOp(n_indent, False),
				takeTerm(n_indent, thisSymbol)
			)(tokens,symbolTree)
			return res[0], res[1], thisSymbol
			pass
		elif(tmp.find("(") != -1):
			res =  applyTakers(
				takeSymbol( n_indent, "("),
				takeExpression(n_indent),
				takeSymbol( n_indent, ")"),
			)(tokens,symbolTree)
			return res[0], res[1], thisSymbol
			pass
		else:
			return None, tokens, thisSymbol
			
	@delay_token_application
	def takeUnaryOp(tokens, thisSymbol, n_indent, err):
		res =  takeSymbol(n_indent, val="~|-", err=False)(tokens, thisSymbol)
		return res[0], res[1], thisSymbol
	
	@delay_token_application
	def takeSubroutineCall(tokens, thisSymbol:SymbolTree, n_indent):
		token = tokens[1]
		tmp = token.tag

		if(tmp.find(tokenFormat("symbol", ".")) != -1):
			# for static function a.b()
			res = applyTakers(
				takeIdentifier(n_indent),
				takeSymbol(n_indent, "."),
				takeIdentifier(n_indent),
				takeSymbol(n_indent, "("),
				takeExpressionList(n_indent),
				takeSymbol(n_indent, ")"),
			)(tokens,symbolTree)
		else:
			# for instance method a()
			res = applyTakers(
				takeIdentifier(n_indent),
				takeSymbol(n_indent, "("),
				takeExpressionList(n_indent),
				takeSymbol(n_indent, ")"),
			)(tokens,symbolTree)

		return res[0], res[1], thisSymbol
		pass

	@delay_token_application
	@tag_indent("expressionList", expand_none=True)
	def takeExpressionList(tokens, thisSymbol:SymbolTree, n_indent):
		res = applyTakers(
			takeExpression(n_indent),
			takeUtilNone(
				takeSymbol(n_indent, ",", False),
				takeExpression(n_indent)
			)
		)(tokens,symbolTree)
		return res[0], res[1], thisSymbol
	
	@delay_token_application
	def takeOp(tokens, thisSymbol:SymbolTree, n_indent, err=True):
		res = takeSymbol(n_indent, "+|-|*|/|&|OR|<|>|=", err=err)(tokens, thisSymbol)
		return res[0], res[1], thisSymbol
	
	@delay_token_application
	@tag_indent("whileStatement")
	def takeStatementWhile(tokens, thisSymbol:SymbolTree, n_indent):
		res = applyTakers(
			takeKeyword(n_indent, "while", err=True),
			takeSymbol(n_indent, "("),
			takeExpression(n_indent),
			takeSymbol(n_indent, ")"),
			takeSymbol(n_indent, "{"),
			takeStatements(n_indent),
			takeSymbol(n_indent, "}"),
		)(tokens,symbolTree)
		return res[0], res[1], thisSymbol
		pass
	@delay_token_application
	@tag_indent("doStatement")
	def takeStatementDo(tokens, thisSymbol:SymbolTree, n_indent):
		res = applyTakers(
			takeKeyword(n_indent, "do", err=True),
			takeSubroutineCall(n_indent),
			takeSymbol(n_indent, ";")
		)(tokens,symbolTree)
		return res[0], res[1], thisSymbol
	
	@delay_token_application
	@tag_indent("returnStatement")
	def takeStatementReturn(tokens, thisSymbol:SymbolTree, n_indent):
		res = applyTakers(
			takeKeyword(n_indent, "return", err=True),
			applyTakers(
	       		takeExpression(n_indent)
			),
			takeSymbol(n_indent, ";"),
			breakNone=False
		)(tokens,symbolTree)
		return res[0], res[1], thisSymbol


	@tag_indent("class")
	def compileClass( tokens, symbolTree, n_indent):
		res = applyTakers(
			takeKeyword( n_indent, "class", err=True),
			takeIdentifier( n_indent),
			takeSymbol( n_indent, "{"),
			takeUtilNone(
				compileClassVarDec(n_indent),
			),
			takeUtilNone(
				compileSubroutineDec(n_indent, tokens[1])
			),
			takeSymbol( n_indent, "}"),
		)(tokens, symbolTree)
		return res[0], res[1], symbolTree
		
	

	print("=====   compiling:" + filepath)
	# start compile
	tokens = tokenizer(filepath)
	res = compileClass(tokens, symbolTree, 0)
	# xmlout(res)

	return res[0], res[1], symbolTree

def tokenFormat(tag, val):
	res = "<{0}> {1} </{2}>".format(tag, val, tag)
	return res

def tokenizer(file):
	res = []
	tokenizer = JackTokenizer(file)
	while(tokenizer.hasMoreCommands()) :
		tmp = tokenizer.advance()
		tmp.tag = tokenFormat(tmp.type, tmp.val)
		res.append(tmp)
	return res



def filename(file):
	return Path(file).stem
def xmlformat(res):
	return res.tag.replace(
	'<symbol> < </symbol>', '<symbol> &lt; </symbol>').replace(
	'<symbol> > </symbol>', '<symbol> &gt; </symbol>').replace(
	'<symbol> & </symbol>', '<symbol> &amp; </symbol>')


def xmlout( tokens, file):
	file = open(file, "w")
	# print result
	for i in tokens[0]:
		file.write(xmlformat(i) + "\n")
	file.close()
	pass
def parseFile(file):
	outputfile = file[:len(file)-5]
	symbolTree = SymbolTree()
	vmoutputfile = outputfile + "2.vm"
	asserberEngine = AssemberEngine(vmoutputfile)
	res = CompilationEngine(file,symbolTree , asserberEngine)
	xmlout( res, outputfile + "3.xml")
	

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
		print("not found source file to compiler!")
		sys.exit()

	srouceFileOrDir  =sys.argv[1]
	start(srouceFileOrDir)

