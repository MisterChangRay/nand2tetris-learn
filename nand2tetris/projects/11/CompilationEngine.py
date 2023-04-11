
import sys
import re
import os
from JackTokenizer import JackTokenizer
from JackTokenizer import Token
import traceback
from pathlib import Path




def CompilationEngine(filepath):
	def tag_indent(tagName, outIfNone = True):
		def wapper(fn):
			def helper( tokens, nedent, *args, **kwargs):
				res = []
				takeTokens, tokens = fn( tokens, nedent + 1, *args, **kwargs)
				if(None == takeTokens and outIfNone == False):
					res.append(tokenFormat(tagName, ""))
				else:
					res.append(doIndent(nedent, "<{0}>".format(tagName)) )
					res += takeTokens
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
		return (" " * 3) * i + token
	
	def take(type, tokens, n_indent, val = None):
		tmp = tokens[0]
		if(None != val):
			strs = val.split("|")
			err = True
			for key in strs:
				if(tokenFormat(type, val)  == tmp):
					err = False
					break
			if(err):
				print("compilation val error! except: {0}".format(tmp))
				return None, tokens
		
		return [doIndent(n_indent, tmp)], tokens[1:]
	@delay_token_application
	def takeKeyword(  tokens, n_indent, val):
		# "class|constructor|function|method|field|static|var|int|char|boolean|void|true|false|null|this|let|do|if|else|while|return"
		return take("keyword", tokens, n_indent, val)
	@delay_token_application
	def takeIdentifier( tokens, n_indent):
		return take("identifier", tokens, n_indent)
	@delay_token_application
	def takeSymbol( tokens, n_indent, val):
		return take("symbol", tokens, n_indent, val)
	@delay_token_application
	def takeInt(self):
		return take("integerConstant")
	
	# int, char, boolean, identifer
	@delay_token_application
	def takeType( val=None):
		tmp = tokenizer.next()
		err = False
		if(tmp.type == "identifier"):
			return tmp
		elif(tmp.type == "keyword"):
			if(val == None):
				if( tmp.val == "int" or tmp.val != "char" or tmp.val != "boolean"):
					return tmp
			elif(val == tmp.val):
				return tmp
		else:
			print("compilation type error! except:{0}, actual:{1}; line({2}): {3}".format(val, tmp.val, tmp.lineno, tmp.linetxt))
			
		return None

	def applyTakers(tokens, *tasks):
		taked = []
		for task in tasks:
			res, tokens = task(tokens)
			if(res == None):
				break
			else:
				taked += res
				
		return taked if(len(taked) > 0) else None, tokens
	def takeUtilNone( *tasks):
		i = 0
		taked = []
		for task in tasks:
			res = task()
			if(res == None):
				break
			else:
				taked.append(res)
				i+=1
		return taked
	
	@tag_indent("classVarDec")
	@delay_token_application
	def compileClassVarDec(tokens, n_indent):
		return applyTakers(
			tokens,
			takeKeyword("static|field"),
			takeType(),
			takeIdentifier(tokens, n_indent),
			takeUtilNone(
				takeSymbol(tokens, n_indent, ","),
				takeIdentifier(tokens, n_indent)
			),
			takeSymbol(tokens, n_indent, ";")
		)
		
		
	def compileSubroutineDec(tokens, n_indent):
		pass

	def xmlout( *tokens):
		print(len(tokens))

		pass

	@tag_indent("class")
	def compileClass( tokens, n_indent):
		res = applyTakers(
			tokens, 
			takeKeyword( n_indent, "class"),
			takeIdentifier( n_indent),
			takeSymbol( n_indent, "{"),
			compileClassVarDec(n_indent),
			# compileSubroutineDec( n_indent)
		)
		return res
		
	


	# start compile
	tokens = tokenizer(filepath)
	res = compileClass(tokens, 0)

	# print result
	for i in res[0]:
		print(i)
		pass
	return

def tokenFormat(tag, val):
	res = "<{0}> {1} </{2}>".format(tag, val, tag)
	res.replace(
        '<symbol> < </symbol>', '<symbol> &lt; </symbol>').replace(
        '<symbol> > </symbol>', '<symbol> &gt; </symbol>').replace(
        '<symbol> & </symbol>', '<symbol> &amp; </symbol>')
	return res

def tokenizer(file):
	res = []
	tokenizer = JackTokenizer(file)
	while(tokenizer.hasMoreCommands()) :
		tmp = tokenizer.advance()
		res.append(tokenFormat(tmp.type, tmp.val))
	return res



def filename(file):
	return Path(file).stem

def parseFile(file):
	outputfile = file[:len(file)-5]
	outputfile = outputfile + ".vm"
	CompilationEngine(file)
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