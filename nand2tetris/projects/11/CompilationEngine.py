
import sys
import re
import os
from JackTokenizer import JackTokenizer
from JackTokenizer import Token
import traceback
from pathlib import Path

class SymbolTable:
	def add(self, name, dataType, type):
		if(self.hasSymbol(name)):
			raise ValueError(f"compilation type error! has more definetion " + name)
		self.tables[name] = Symbol(name, dataType, type, self.countType(type))

	def countType(self, type):
		count = 0
		for k in self.tables:
			if(k.type == type):
				count += 1
		return count

	def hasSymbol(self, name):
		res = self.tables.get(name)
		if(res == None):
			return False
		return True

	def __init__(self, parent = None):
		self.tables = dict()
		self.next = None
		self.parent = None
		if(parent != None):
			self.parent  = parent
			parent.next = self
		pass
class Symbol:
	def __init__(self, name, dataType, type, index):
		self.name = name
		self.dataType = dataType
		self.type = type
		self.index = index
		pass
	

def CompilationEngine(filepath, symbolTable):
	def tag_indent(tagName, expand_none = False):
		def wapper(fn):
			def helper( tokens, nedent, *args, **kwargs):
				res = []
				takeTokens, tokens = fn( tokens, nedent + 1, *args, **kwargs)
				if(takeTokens == None and expand_none == True):
					takeTokens = []
				if(takeTokens == None):
					return None, tokens
				else:
					res.append(doIndent(nedent, "<{0}>".format(tagName)) )
					res += [] if (None == takeTokens) else takeTokens
					res.append(doIndent(nedent,"</{0}>".format(tagName) ))
				return res, tokens
			return helper
		return wapper
	
	def delay_token_application(f):
		"""Decorate f to make it a "delayed" function waiting for tokens"""
		def helper(*args, **kwargs):
			return lambda tokens : f( tokens, *args, **kwargs)
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
		
		return [doIndent(n_indent, tmp)], tokens[1:]
	@delay_token_application
	def takeKeyword(  tokens, n_indent, val, err=True):
		# "class|constructor|function|method|field|static|var|int|char|boolean|void|true|false|null|this|let|do|if|else|while|return"
		return take("keyword", tokens, n_indent, val, err)
	@delay_token_application
	def takeIdentifier( tokens, n_indent):
		return take("identifier", tokens, n_indent)
	
	@delay_token_application
	def takeSymbol( tokens, n_indent, val, err = True):
		return take("symbol", tokens, n_indent, val, err)
	
	@delay_token_application
	def takeInt(self):
		return take("integerConstant")
	
	# int, char, boolean, identifer , void
	@delay_token_application
	def takeType(tokens, indent, includeVoid=False, err = True):
		token = tokens[0]
		tmp = token.tag

		if(tmp.find( "identifier") > 0):
			return [doIndent( indent, tmp )], tokens[1:]
		elif(tmp .find( "keyword") > 0):
			if(tmp == tokenFormat("keyword", "int") or 
      			tmp == tokenFormat("keyword", "char") or 
				tmp == tokenFormat("keyword", "boolean")):
				return [doIndent( indent, tmp)], tokens[1:]
			if(tmp == tokenFormat("keyword", "void") ):
				return [doIndent( indent, tmp)], tokens[1:]
		elif(err == True):
			raise ValueError(f"compilation type error! except: type or identifier ")
			
		return None, tokens

	@delay_token_application
	def applyTakers(tokens,  *tasks, breakNone=True):
		taked = []
		for task in tasks:
			res, tokens = task(tokens)
			if(res == None):
				if(breakNone) :
					break
				else:
					continue
			else:
				taked += res
				
		return taked if(len(taked) > 0) else None, tokens
	
	@delay_token_application
	def takeUtilNone(tokens, *tasks):
		i = 0
		taked = []
		ended = False
		while True:
			for task in tasks:
				res, tokens = task(tokens)
				if(res == None):
					ended = True
					break
				else:
					taked += res
					i+=1
			if(ended == True):
				break
		return taked, tokens
	
	@delay_token_application
	@tag_indent("classVarDec")
	def compileClassVarDec(tokens, n_indent):
		return applyTakers(
			takeKeyword(n_indent, "static|field", err=False),
			takeType(n_indent),
			takeIdentifier(n_indent),
			takeUtilNone(
				takeSymbol( n_indent, ",", False),
				takeIdentifier( n_indent)
			),
			takeSymbol( n_indent, ";")
		)(tokens)
		
	@delay_token_application
	@tag_indent("subroutineDec")
	def compileSubroutineDec(tokens, n_indent):
		return applyTakers(
			takeKeyword(n_indent, "constructor|function|method", err=False),
			takeType(n_indent, True),
			takeIdentifier(n_indent),
			takeSymbol(n_indent, "("),
			takeParameterList(n_indent),
			takeSymbol(n_indent, ")"),
			takeSubroutineBody(n_indent)
		)(tokens)

	@delay_token_application
	@tag_indent("parameterList", expand_none=True)
	def takeParameterList(tokens, n_indent):
		return applyTakers(
			takeType(n_indent, False, False),
			takeIdentifier(n_indent),
			takeUtilNone(
				takeSymbol(n_indent, ",", err=False),
				takeType(n_indent),
				takeIdentifier(n_indent)
			)
		)(tokens)
		pass

	@delay_token_application
	@tag_indent("subroutineBody")
	def takeSubroutineBody(tokens, n_indent):
		return applyTakers(
	
			takeSymbol(n_indent, "{"),
			takeUtilNone(
				takeVarDec(n_indent),
			),
			takeStatements(n_indent),
			takeSymbol(n_indent, "}")
		)(tokens)


	@delay_token_application
	@tag_indent("varDec")
	def takeVarDec(tokens, n_indent):
		return applyTakers(
			takeKeyword(n_indent, "var", False),
			takeType(n_indent, False),
			takeIdentifier(n_indent),
			takeUtilNone(
				takeSymbol(n_indent, ",", False),
				takeIdentifier(n_indent)
			),
			takeSymbol(n_indent, ";")
		)(tokens)

	@delay_token_application
	@tag_indent("statements")
	def takeStatements(tokens, n_indent):
		res = []
		while(True):
			token = tokens[0]
			tmp = token.tag
			if(tmp == tokenFormat("keyword", "let")):
				tmp, tokens = takeStatementLet( n_indent)(tokens)
				res += tmp
			elif(tmp == tokenFormat("keyword", "if")):
				tmp, tokens =  takeStatementIf( n_indent)(tokens)
				res += tmp
			elif(tmp == tokenFormat("keyword", "while")):
				tmp, tokens =  takeStatementWhile( n_indent)(tokens)
				res += tmp
			elif(tmp == tokenFormat("keyword", "do")):
				tmp, tokens =  takeStatementDo( n_indent)(tokens)
				res += tmp
			elif(tmp == tokenFormat("keyword", "return")):
				tmp, tokens =  takeStatementReturn( n_indent)(tokens)
				res += tmp
			else:
				break
		return res, tokens			


	@delay_token_application
	@tag_indent("letStatement")
	def takeStatementLet(tokens, n_indent):
		res = applyTakers(
		     	takeKeyword(n_indent, "let"),
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
			 )(tokens, )
		return res
	
	@delay_token_application
	@tag_indent("expression")
	def takeExpression(tokens, n_indent):
		res = applyTakers(
			takeTerm(n_indent),
			takeUtilNone(
				takeOp(n_indent, err = False),
				takeTerm(n_indent)
			)
		)(tokens)
		return res
		pass
	@delay_token_application
	@tag_indent("ifStatement")
	def takeStatementIf(tokens, n_indent):
		return applyTakers(
			takeKeyword(n_indent, "if"),
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
		)(tokens)
		pass

	@delay_token_application
	@tag_indent("term")
	def takeTerm(tokens, n_indent):
		token = tokens[0]
		tmp = token.tag
		if(tmp.find("<integerConstant>") != -1 or tmp.find("<stringConstant>")  != -1 or tmp.find("<keyword>" )  != -1):
			return [doIndent(n_indent, tmp)], tokens[1:]
		elif(tmp.find("<identifier>") != -1):
			token1 = tokens[1]
			tmp1 = token1.tag
			if(tmp1.find("[") != -1):
				# variable a[b]
				return applyTakers(
					takeIdentifier(n_indent),
					takeSymbol(n_indent, "["),
					takeExpression(n_indent),
					takeSymbol(n_indent, "]")
				)(tokens)
				pass
			elif(tmp1.find("(") != -1):
				# method a()
				return takeSubroutineCall( n_indent)(tokens)
			elif(tmp1.find(".") != -1):
				# method a.b()
				return takeSubroutineCall( n_indent)(tokens)
			else:
				# var name
				return [doIndent(n_indent, tmp)], tokens[1:]
		elif(tmp.find("-") != -1 or tmp.find("~") != -1):
			return applyTakers(
				takeUnaryOp(n_indent, False),
				takeTerm(n_indent)
			)(tokens)
			pass
		elif(tmp.find("(") != -1):
			return applyTakers(
				takeSymbol( n_indent, "("),
				takeExpression(n_indent),
				takeSymbol( n_indent, ")"),
			)(tokens)
			pass
		else:
			return None, tokens
			
	@delay_token_application
	def takeUnaryOp(tokens, n_indent, err):
		return takeSymbol(n_indent, val="~|-", err=False)(tokens)
	
	@delay_token_application
	def takeSubroutineCall(tokens, n_indent):
		token = tokens[1]
		tmp = token.tag

		if(tmp.find(tokenFormat("symbol", ".")) != -1):
			# a.b()
			return applyTakers(
				takeIdentifier(n_indent),
				takeSymbol(n_indent, "."),
				takeIdentifier(n_indent),
				takeSymbol(n_indent, "("),
				takeExpressionList(n_indent),
				takeSymbol(n_indent, ")"),
			)(tokens)
		else:
			# a()
			return applyTakers(
				takeIdentifier(n_indent),
				takeSymbol(n_indent, "("),
				takeExpressionList(n_indent),
				takeSymbol(n_indent, ")"),
			)(tokens)
		pass

	@delay_token_application
	@tag_indent("expressionList", expand_none=True)
	def takeExpressionList(tokens, n_indent):
		return applyTakers(
			takeExpression(n_indent),
			takeUtilNone(
				takeSymbol(n_indent, ",", False),
				takeExpression(n_indent)
			)
		)(tokens)
		pass
	@delay_token_application
	def takeOp(tokens, n_indent, err=True):
		return takeSymbol(n_indent, "+|-|*|/|&|OR|<|>|=", err=err)(tokens)
	
	@delay_token_application
	@tag_indent("whileStatement")
	def takeStatementWhile(tokens, n_indent):
		return applyTakers(
			takeKeyword(n_indent, "while"),
			takeSymbol(n_indent, "("),
			takeExpression(n_indent),
			takeSymbol(n_indent, ")"),
			takeSymbol(n_indent, "{"),
			takeStatements(n_indent),
			takeSymbol(n_indent, "}"),
		)(tokens)
		pass
	@delay_token_application
	@tag_indent("doStatement")
	def takeStatementDo(tokens, n_indent):
		return applyTakers(
			takeKeyword(n_indent, "do"),
			takeSubroutineCall(n_indent),
			takeSymbol(n_indent, ";")
		)(tokens)
		pass
	@delay_token_application
	@tag_indent("returnStatement")
	def takeStatementReturn(tokens, n_indent):
		return applyTakers(
			takeKeyword(n_indent, "return"),
			applyTakers(
	       		takeExpression(n_indent)
			),
			takeSymbol(n_indent, ";"),
			breakNone=False
		)(tokens)
		pass


	@tag_indent("class")
	def compileClass( tokens, n_indent):
		res = applyTakers(
			takeKeyword( n_indent, "class"),
			takeIdentifier( n_indent),
			takeSymbol( n_indent, "{"),
			takeUtilNone(
				compileClassVarDec(n_indent),
			),
			takeUtilNone(
				compileSubroutineDec( n_indent)
			),
			takeSymbol( n_indent, "}"),
		)(tokens)
		return res
		
	

	print("=====   compiling:" + filepath)
	# start compile
	tokens = tokenizer(filepath)
	res = compileClass(tokens, 0)
	# xmlout(res)

	return res

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
	res = res.replace(
	'<symbol> < </symbol>', '<symbol> &lt; </symbol>').replace(
	'<symbol> > </symbol>', '<symbol> &gt; </symbol>').replace(
	'<symbol> & </symbol>', '<symbol> &amp; </symbol>')
	return res

def xmlout( tokens, file):
	file = open(file, "w")
	# print result
	for i in tokens[0]:
		file.write(xmlformat(i) + "\n")
	file.close()
	pass
def parseFile(file):
	outputfile = file[:len(file)-5]
	res = CompilationEngine(file, SymbolTable())
	xmlout( res, outputfile + "3.xml")
	outputfile = outputfile + ".vm"

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

