
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
		self.vmfile.write("return \n")
		pass
	def writeLabel(self, label):
		self.vmfile.write("label {0}\n".format(label))
		pass
	def writeGoto(self, type, label):
		if(type == 1):
			self.vmfile.write("goto-if {0} \n".format(label))
		else :
			self.vmfile.write("goto {0} \n".format(label))
		pass
	def writeArithmetic(self,val):
		dic = {
			"-" :"sub",
			"+" :"add",
			"*":"call Math.multiply 2",
   			"/":"call Math.divide 2",
      
      		"<" :"lt",
			">" :"gt",
   			"=" :"eq",
			"~" :"not",
			"&" :"and",
			"|" :"or",
   			"!" :"neg",
		}
		
		self.vmfile.write(dic.get(val) +  "\n")
		
		pass
	def writeCall(self, *args):
		self.outline("call", args)
		
		pass
	def writeFunction(self, name, localNum, type):
		# type : constructor|function|method
  		# localNum : 局部变量表个数
		self.vmfile.write("function {0} {1} \n".format(name, localNum))
		pass
	def flsh(self):
		pass
	def outline(self, keywrod, args):
		tmp = keywrod + " "
		for i in range(len(args)):
			tmp += str(args[i]) + " "

		self.vmfile.write(tmp + "\n")
		return
	def __init__(self, outfile):
		self.vmfile = open(outfile, "w")
		pass

class SymbolTree:
	# type : arguments, var, static, field, constructor|function|method
	def add(self, name, dataType, type):
		# constructor|function|method
		kname = self.key(name, type)		
		if(None != self.tables.get(kname)):
			raise ValueError(f"compilation type error：identifier has already defined! -> " + name)
		
		self.tables[kname] = Symbol(name, dataType, type, self.countType( self.distict(type)))
	def distict(self, type):
		type = type.replace("constructor", "fn") \
				.replace("function", "fn") \
				.replace("method", "fn") \
				.replace("field", "field") \
				.replace("static", "field") \
				.replace("arguments", "var") 
		return type
	def getSymbol(self, name):
		this = self
		while(True):
			kname = self.key(name, "field")
			if(this.tables.get(kname) != None):
				return this.tables.get(kname)
			kname = self.key(name, "var")
			if(this.tables.get(kname) != None):
				return this.tables.get(kname)
			if(this.parent != None):
				this = this.parent
			else :
				break
		raise ValueError(f"compilation type error：identifier has not defined! -> " + name)
	def key(self, name, type):
		return name + "_" + self.distict(type)

	def countType(self, type):
		count = 0
		for k in self.tables:
			tmp = self.tables[k]
			if(self.distict(tmp.type) == type):
				count += 1
		return count
	

	def remove(self):
		self.parent.next.remove(self)
		return
	def addChild(self, name, child):
		self.next[name] = child
		child.parent = self
		pass

	def __init__(self):
		self.tables = {			}
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
	

def CompilationEngine(tokens, symbolTree:SymbolTree, assemberEngine:AssemberEngine):
	clzName = None
	fnLocalVarCount = 0
	globalLabelIndex = 0
 
	def tag_indent(tagName, expand_none = False):
		def wapper(fn):
			def helper( readIndex, symbolTree, nedent, *args, **kwargs):
				res = []
				takeTokens, readIndex, symbolTree = fn( readIndex, symbolTree, nedent + 1, *args, **kwargs)

				
				if(takeTokens == None and expand_none == True):
					takeTokens = []
				if(takeTokens == None):
					return None, readIndex, symbolTree
				else:
					# before = Token(None, tagName, None, None)
					# before.tag = doIndent(nedent, "<{0}>".format(tagName)) 
					# res.append(before)
					res += takeTokens

					# after = Token(None, tagName, None, None)
					# after.tag = doIndent(nedent, "</{0}>".format(tagName)) 
					# res.append(after)
				return res, readIndex, symbolTree
			return helper
		return wapper
	
	def delay_token_application(f):
		"""Decorate f to make it a "delayed" function waiting for tokens"""
		def helper(*args, **kwargs):
			def f1(readIndex, symbolTree):
				res = f( readIndex, symbolTree, *args, **kwargs)
				# if(len(res) <= 2) :
				# 	print(333)
				return res
			return f1
		return helper

	
	def doIndent( i, token):
		return (" " * 2) * i + token
	
	def take(type, readIndex, n_indent, val = None, err = True):
		token = tokens[readIndex]
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
				return None, readIndex
		token.tag = doIndent(n_indent, tmp)
		return [token], readIndex + 1
	@delay_token_application
	def takeKeyword(  readIndex, symbolTree, n_indent, val, err):
		# "class|constructor|function|method|field|static|var|int|char|boolean|void|true|false|null|this|let|do|if|else|while|return"
		res =  take("keyword", readIndex, n_indent, val, err) 
		nonlocal clzName


		if(None !=  res[0]):
			if(val == "class"):
				clzName = tokens[readIndex + 1].val
	
		return res[0], res[1], symbolTree
		
	@delay_token_application
	def takeIdentifier( readIndex, symbolTree:SymbolTree, n_indent, symbolType=None):
		# type : static, method, function, name, class, 
		# symbolType: fn, var,  field, param
		res = take("identifier", readIndex, n_indent)

		if(None != symbolType) :
			if(symbolType == "class"):
				clzName = tokens[readIndex].val
			#registe to symbolTalbe
			if(symbolType == "arguments"):
				type = tokens[readIndex - 1].val
				name = tokens[readIndex].val
				symbolTree.add(name, type, "arguments")

				nextIndex = readIndex + 1
				while True:
					next = tokens[nextIndex]
					if(next.type == "symbol" and next.val == ","):
						type = tokens[nextIndex + 1].val
						name = tokens[nextIndex + 2].val
						symbolTree.add(name, type, "arguments")
						nextIndex += 3
					else :
						break
				pass
			if(symbolType == "var" or symbolType == "field"):
				nonlocal fnLocalVarCount
    
				type = tokens[readIndex - 2].val
				dataType = tokens[readIndex - 1].val
				name = tokens[readIndex].val
				symbolTree.add(name, dataType, type)
				fnLocalVarCount += 1

				nextIndex = readIndex + 1
				while True:
					next = tokens[nextIndex ]
					if(next.type == "symbol" and next.val == ","):
						fnLocalVarCount += 1
						name = tokens[nextIndex + 1].val
						symbolTree.add(name, dataType, type)
						nextIndex += 2
					else :
						break

				pass
			if(symbolType == "fn"):
				newSymbolTree = SymbolTree()
				
				fnName = tokens[readIndex].val
				fnReturnType = tokens[readIndex - 1].val
				# fnType: constructor|method|function
				fnType = tokens[readIndex - 2].val

				newSymbolTree.parent = symbolTree
				symbolTree.add(fnName,  fnReturnType, fnType)
				symbolTree.addChild(fnName, newSymbolTree )

				symbolTree = newSymbolTree
				
				pass
			pass
		return res[0], res[1], symbolTree
	
	@delay_token_application
	def takeSymbol( readIndex, symbolTree, n_indent, val, err = True):
		res =  take("symbol", readIndex, n_indent, val, err)
		return res[0], res[1], symbolTree
	
	
	
	# int, char, boolean, identifer , void
	@delay_token_application
	def takeType(readIndex, symbolTree, indent, includeVoid=False, err = True):
		token = tokens[readIndex]
		tmp = token.tag

		if(tmp.find( "identifier") > 0):
			token.tag = doIndent( indent, tmp )
			return [token], readIndex+1, symbolTree
		elif(tmp .find( "keyword") > 0):
			if(tmp == tokenFormat("keyword", "int") or 
      			tmp == tokenFormat("keyword", "char") or 
				tmp == tokenFormat("keyword", "boolean")):
				
				token.tag = doIndent( indent, tmp )
				return [token], readIndex + 1, symbolTree
			if(tmp == tokenFormat("keyword", "void") ):

				token.tag = doIndent( indent, tmp )
				return [token], readIndex + 1, symbolTree
		elif(err == True):
			raise ValueError(f"compilation type error! except: type or identifier ")
			
		return None, readIndex, symbolTree

	@delay_token_application
	def applyTakers(readIndex, symbolTree,  *tasks,  breakNone=True):
		taked = []
		
		i = 0
		while( i < len(tasks)):
			task = tasks[i]
			res, readIndex, symbolTree = task(readIndex, symbolTree)
			i += 1
			if(res == "WRITE_CODE"):
				continue
			if(res == None):
				if(breakNone) :
					# j = i
					# while( j < len(tasks)):
					# 	task = tasks[j]
					# 	try:
					# 		# task(readIndex, symbolTree)
					# 		pass
					# 	except ValueError:
					# 		pass
					# 	finally:
					# 		j += 1
					# print("break")
					break
				else:
					continue
			else:
				taked += res
			
				
		return taked if(len(taked) > 0) else None, readIndex, symbolTree
	
	@delay_token_application
	def takeUtilNone(readIndex, symbolTree, *tasks):
		i = 0
		taked = []
		ended = False
		while True:
			for task in tasks:
				res,readIndex, symbolTree  = task(readIndex, symbolTree)
				
				if(res == None):
					ended = True
					break
				else:
					taked += res
					i+=1
			if(ended == True):
				break
		return taked, readIndex, symbolTree
	
	@delay_token_application
	@tag_indent("classVarDec")
	def compileClassVarDec(readIndex, symbolTree, n_indent):
		res = applyTakers(
			takeKeyword(n_indent, "static|field", err=False),
			takeType(n_indent),
			takeIdentifier(n_indent, "field"),
			takeUtilNone(
				takeSymbol( n_indent, ",", False),
				takeIdentifier( n_indent)
			),
			takeSymbol( n_indent, ";")
		)(readIndex,symbolTree)


		return res[0], res[1], symbolTree

	
	@delay_token_application
	@tag_indent("subroutineDec")
	def compileSubroutineDec(readIndex, thisSymbolTree:SymbolTree, n_indent):
		nonlocal fnLocalVarCount
		fnLocalVarCount = 0
		res = applyTakers(
			takeKeyword(n_indent, "constructor|function|method", err=False),
			takeType(n_indent, True),
			takeIdentifier(n_indent, "fn"),
			takeSymbol(n_indent, "("),
			takeParameterList(n_indent),
			takeSymbol(n_indent, ")"),
			takeSubroutineBody(n_indent, readIndex)
		)(readIndex, thisSymbolTree)
		
		return res[0], res[1], thisSymbolTree
		
	@delay_token_application
	@tag_indent("parameterList", expand_none=True)
	def takeParameterList(readIndex, thisSymbol:SymbolTree, n_indent):
		res = applyTakers(
			takeType(n_indent, False, False),
			takeIdentifier(n_indent, "arguments"),
			takeUtilNone(
				takeSymbol(n_indent, ",", err=False),
				takeType(n_indent),
				takeIdentifier(n_indent)
			)
		)(readIndex,thisSymbol)
  
	
	
		return res[0], res[1], thisSymbol
	
 
	@delay_token_application
	def writeFunction(readIndex, thisSymbol:SymbolTree, n_indent, fnStartReadIndex):
		# write label of function
		nonlocal fnLocalVarCount
		nonlocal clzName
		fnName = "{0}.{1}".format(clzName, tokens[fnStartReadIndex + 2].val)
		assemberEngine.writeFunction(fnName, fnLocalVarCount,tokens[readIndex - 4].val )
		
		return "WRITE_CODE", readIndex, thisSymbol

	@delay_token_application
	@tag_indent("subroutineBody")
	def takeSubroutineBody(readIndex, thisSymbol:SymbolTree, n_indent, fnStartReadIndex):
		res = applyTakers(
			takeSymbol(n_indent, "{"),
			takeUtilNone(
				takeVarDec(n_indent),
			),
			writeFunction(n_indent, fnStartReadIndex),
			takeStatements(n_indent),
			takeSymbol(n_indent, "}")
		)(readIndex,thisSymbol)
		return res[0], res[1], thisSymbol


	@delay_token_application
	@tag_indent("varDec")
	def takeVarDec(readIndex, thisSymbol:SymbolTree, n_indent):
		res = applyTakers(
			takeKeyword(n_indent, "var", err=False),
			takeType(n_indent, False),
			takeIdentifier(n_indent, "var"),
			takeUtilNone(
				takeSymbol(n_indent, ",", err=False),
				takeIdentifier(n_indent)
			),
			takeSymbol(n_indent, ";")
		)(readIndex,thisSymbol)

		
		
		return res[0], res[1], thisSymbol
	@delay_token_application
	@tag_indent("statements")
	def takeStatements(readIndex, thisSymbol:SymbolTree, n_indent):
		res = []
		while(True):
			token = tokens[readIndex]
			tmp = token.tag
			if(tmp == tokenFormat("keyword", "let")):
				tmp, readIndex, thisSymbol1 = takeStatementLet( n_indent)(readIndex, thisSymbol)
				res += tmp
			elif(tmp == tokenFormat("keyword", "if")):
				startIndex = readIndex
				writeStatementIf(n_indent, 1, startIndex)(readIndex, thisSymbol)
				tmp, readIndex, thisSymbol1 =  takeStatementIf( n_indent)(readIndex, thisSymbol)
				writeStatementIf(n_indent, 3, startIndex)(readIndex, thisSymbol)
				res += tmp
			elif(tmp == tokenFormat("keyword", "while")):
				startIndex = readIndex
				tmp, readIndex, thisSymbol1 =  takeStatementWhile( n_indent)(readIndex, thisSymbol)
				writeWhileCode(n_indent, 2, startIndex)(readIndex, thisSymbol)
				res += tmp
			elif(tmp == tokenFormat("keyword", "do")):
				tmp, readIndex, thisSymbol1 =  takeStatementDo( n_indent)(readIndex, thisSymbol)
				res += tmp
			elif(tmp == tokenFormat("keyword", "return")):
				tmp, readIndex, thisSymbol1 =  takeStatementReturn( n_indent)(readIndex, thisSymbol)
				res += tmp
			else:
				break
		return res, readIndex, thisSymbol			


	@delay_token_application
	@tag_indent("letStatement")
	def takeStatementLet(readIndex,  thisSymbol:SymbolTree, n_indent):
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
			 )(readIndex,thisSymbol )

		if(res != None and len(res) > 0):

			# vm code 
			name = res[0][1].val
			assemberEngine.writePop("temp", 0)
			if(res[0][2].type == "symbol" and res[0][2].val == "["):
				assemberEngine.writePop("temp", 1)
			symbol = thisSymbol.getSymbol(name)
			if(symbol.type == "var"):
				# 局部变量表
				assemberEngine.writePush("local", symbol.index)
			if(symbol.type == "field"):
				# 类成员属性
				pass
			if(symbol.type == "static"):
				# 全局成员属性
				assemberEngine.writePush("static", symbol.index)
				pass
			if(symbol.type == "arguments"):
				# 参数变量表
				assemberEngine.writePush("argument", symbol.index)
		return res[0], res[1], thisSymbol
	
	@delay_token_application
	@tag_indent("expression")
	def takeExpression(readIndex, thisSymbol:SymbolTree, n_indent):
		res = applyTakers(
			takeTerm(n_indent),
			takeUtilNone(
				takeOp(n_indent, err = False),
				takeTerm(n_indent, addOp=True)
			)
		)(readIndex,symbolTree)


		return res[0], res[1], thisSymbol
		pass
	
	@delay_token_application
	def writeStatementIf(readIndex, thisSymbol:SymbolTree , n_indent, type, index):
		tagelse = "if_{0}_else".format(index)
		tagend = "if_{0}_end".format(index)
		
		# type : 标签位置
		if(type == 1):
			# if start
			# 取反, 大于0则跳到else
			assemberEngine.writeArithmetic("!")
			# if > 0 
			assemberEngine.writeGoto(1, tagelse)
			pass
		if(type == 2):
			assemberEngine.writeGoto(2, tagend)
			assemberEngine.writeLabel(tagelse)
			pass
		if(type == 3):
			assemberEngine.writeLabel(tagend)
			pass
		if(type == 4):
			assemberEngine.writeGoto(2, tagend)
			pass

		return "WRITE_CODE", readIndex, thisSymbol

	@delay_token_application
	@tag_indent("ifStatement")
	def takeStatementIf(readIndex, thisSymbol:SymbolTree , n_indent):
		res = applyTakers(
			takeKeyword(n_indent, "if", err=True),
			takeSymbol(n_indent, "("),
			takeExpression(n_indent),
			takeSymbol(n_indent, ")"),
			takeSymbol(n_indent, "{"),
			takeStatements(n_indent),
   
   			writeStatementIf(n_indent, 2, readIndex),
      
			takeSymbol(n_indent, "}"),
			applyTakers(
				takeKeyword(n_indent, "else", err=False),
				takeSymbol(n_indent, "{"),
				takeStatements(n_indent),
				takeSymbol(n_indent, "}"),
			),
		)(readIndex,thisSymbol)
		
		writeStatementIf(n_indent, 4, readIndex)(readIndex,thisSymbol)
		return res[0], res[1], thisSymbol

	def writeAddOp(readIndex, addOp):
		if(False == addOp):
			return
		token = tokens[readIndex -1 ]
		assemberEngine.writeArithmetic(token.val)
	
     

	@delay_token_application
	@tag_indent("term")
	def takeTerm(readIndex, thisSymbol:SymbolTree, n_indent, addOp=False):
		token = tokens[readIndex]
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
			
			writeAddOp(readIndex, addOp)
			return [token], readIndex+1, thisSymbol
		elif(tmp.find("<identifier>") != -1):
			token1 = tokens[readIndex + 1]
			tmp1 = token1.tag
			if(tmp1.find("[") != -1):
				# variable a[b]
				res = applyTakers(
					takeIdentifier(n_indent),
					takeSymbol(n_indent, "["),
					takeExpression(n_indent),
					takeSymbol(n_indent, "]")
				)(readIndex,symbolTree)
    
				writeAddOp(readIndex, addOp)
				return res[0], res[1], thisSymbol
				pass
			elif(tmp1.find("(") != -1):
				# method a()
				res = takeSubroutineCall( n_indent)(readIndex, thisSymbol)
				writeAddOp(readIndex, addOp)
				return res[0], res[1], thisSymbol
			elif(tmp1.find(".") != -1):
				# method a.b()
				res= takeSubroutineCall( n_indent)(readIndex, thisSymbol)
				writeAddOp(readIndex, addOp)
				return res[0], res[1], thisSymbol
			else:
				# var name
				token.tag = doIndent(n_indent, tmp)
				writeAddOp(readIndex, addOp)
				return [token], readIndex + 1, thisSymbol
		elif(tmp.find("-") != -1 or tmp.find("~") != -1):
			res = applyTakers(
				takeUnaryOp(n_indent, False),
				takeTerm(n_indent, thisSymbol)
			)(readIndex,symbolTree)
			writeAddOp(readIndex, addOp)
			return res[0], res[1], thisSymbol
			pass
		elif(tmp.find("(") != -1):
			res =  applyTakers(
				takeSymbol( n_indent, "("),
				takeExpression(n_indent),
				takeSymbol( n_indent, ")"),
			)(readIndex,symbolTree)
			writeAddOp(readIndex, addOp)
			return res[0], res[1], thisSymbol
			pass
		else:
			return None, readIndex, thisSymbol
			
	@delay_token_application
	def takeUnaryOp(readIndex, thisSymbol, n_indent, err):
		res =  takeSymbol(n_indent, val="~|-", err=False)(readIndex, thisSymbol)
		return res[0], res[1], thisSymbol
	
	@delay_token_application
	def takeSubroutineCall(readIndex, thisSymbol:SymbolTree, n_indent):
		token = tokens[readIndex + 1]
		tmp = token.tag

		if(tmp.find(tokenFormat("symbol", ".")) != -1):
			fnName = tokens[readIndex].val + tokens[readIndex+1].val  + tokens[readIndex+2].val
			# for static function a.b()
			res = applyTakers(
				takeIdentifier(n_indent),
				takeSymbol(n_indent, "."),
				takeIdentifier(n_indent),
				takeSymbol(n_indent, "("),
				takeExpressionList(n_indent, fnName),
				takeSymbol(n_indent, ")"),
			)(readIndex,symbolTree)
			
		
		else:
			fnName = tokens[readIndex].val
			# for instance method a()
			res = applyTakers(
				takeIdentifier(n_indent),
				takeSymbol(n_indent, "("),
				takeExpressionList(n_indent, fnName),
				takeSymbol(n_indent, ")"),
			)(readIndex,symbolTree)

			# write call
			# 处理this
			assemberEngine.writeCall( )

		return res[0], res[1], thisSymbol
		pass

	@delay_token_application
	@tag_indent("expressionList", expand_none=True)
	def takeExpressionList(readIndex, thisSymbol:SymbolTree, n_indent, fnName):
		# 只有 call 才会调用到这里
		# 实际这个函数是解析参数个数的
		res = applyTakers(
			takeExpression(n_indent),
			takeUtilNone(
				takeSymbol(n_indent, ",", False),
				takeExpression(n_indent)
			)
		)(readIndex,symbolTree)
  
		# 解析调用参数个数
		paramLen = 0
		if(res[0] != None and len(res[0] )> 0):
			paramLen = 1
			for item in res [0]:
				if(item.type == "symbol" and item.val == ","):
					paramLen += 1
			pass
  		# write call 
		assemberEngine.writeCall(fnName, paramLen )
		return res[0], res[1], thisSymbol
	
	@delay_token_application
	def takeOp(readIndex, thisSymbol:SymbolTree, n_indent, err=True):
		res = takeSymbol(n_indent, "+|-|*|/|&|OR|<|>|=", err=err)(readIndex, thisSymbol)
		return res[0], res[1], thisSymbol

	@delay_token_application
	def writeWhileCode(readIndex, thisSymbol:SymbolTree, n_indent, type, index):
		starttag = "while.satrt{0}".format(index)
		endtag = "while.end{0}".format(index)

		if(1 == type):
			assemberEngine.writeLabel(starttag)
			# if start
			# 取反, 大于0则跳到else
			assemberEngine.writeArithmetic("!")
			# if > 0 
			assemberEngine.writeGoto(1, endtag)

		if(2 == type):
			assemberEngine.writeLabel(endtag)
		if(3 == type):
			assemberEngine.writeGoto(2, starttag)
   
   
		return "WRITE_CODE", readIndex, thisSymbol

	@delay_token_application
	@tag_indent("whileStatement")
	def takeStatementWhile(readIndex, thisSymbol:SymbolTree, n_indent):
		res = applyTakers(
			takeKeyword(n_indent, "while", err=True),
			takeSymbol(n_indent, "("),
   			writeWhileCode(n_indent, 1, readIndex), # write start label
			takeExpression(n_indent),
			takeSymbol(n_indent, ")"),
			takeSymbol(n_indent, "{"),
			takeStatements(n_indent),
			writeWhileCode(n_indent, 3, readIndex), # write end label
			takeSymbol(n_indent, "}"),
		)(readIndex,thisSymbol)
  
		return res[0], res[1], thisSymbol
		pass
	@delay_token_application
	@tag_indent("doStatement")
	def takeStatementDo(readIndex, thisSymbol:SymbolTree, n_indent):
		res = applyTakers(
			takeKeyword(n_indent, "do", err=True),
			takeSubroutineCall(n_indent),
			takeSymbol(n_indent, ";")
		)(readIndex,thisSymbol)

  
		return res[0], res[1], thisSymbol
	
	@delay_token_application
	@tag_indent("returnStatement")
	def takeStatementReturn(readIndex, thisSymbol:SymbolTree, n_indent):
		res = applyTakers(
			takeKeyword(n_indent, "return", err=True),
			applyTakers(
	       		takeExpression(n_indent)
			),
			takeSymbol(n_indent, ";"),
			breakNone=False
		)(readIndex,thisSymbol)
  
		assemberEngine.writeReturn()
		return res[0], res[1], thisSymbol


	@tag_indent("class")
	def compileClass( readIndex, symbolTree, n_indent):
		res = applyTakers(
			takeKeyword( n_indent, "class", err=True),
			takeIdentifier( n_indent, "class"),
			takeSymbol( n_indent, "{"),
			takeUtilNone(
				compileClassVarDec(n_indent),
			),
			takeUtilNone(
				compileSubroutineDec(n_indent)
			),
			takeSymbol( n_indent, "}"),
		)(readIndex, symbolTree)
		return res[0], res[1], symbolTree
		
	

	res = compileClass(0, symbolTree, 0)
	# xmlout(res)

	return  res

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


def xmlout( res, file):
	file = open(file, "w")
	# print result
	for i in res[0]:
		file.write(xmlformat(i) + "\n")
	file.close()
	pass
def parseFile(file):
	outputfile = file[:len(file)-5]
	symbolTree = SymbolTree()
	vmoutputfile = outputfile + ".vm"
	print("=====   compiling:" + file)

	asserberEngine = AssemberEngine(vmoutputfile)
	# start compile
	tokens = tokenizer(file)

	res = CompilationEngine(tokens, symbolTree, asserberEngine)
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

