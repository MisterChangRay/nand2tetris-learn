
import sys
import re
import os
from pathlib import Path

def filename(file):
	return Path(file).stem

class Parser:
	def hasMoreCommands(self):
		while True:
			self.linetxt = self.sourcefile.readline()
			if(not self.linetxt) :
			  return False

			# 忽略 注释行
			if(len(self.linetxt) > 0):
			  if( re.match(r".*//.*", self.linetxt)):
			    self.linetxt = self.linetxt[0 : self.linetxt.index("//")]

			  self.linetxt = self.linetxt.strip()
			  if(len(self.linetxt) > 0) :
			    return True

		return
	def advance(self):
		return self.linetxt
	def commandType(self):
		if(self.linetxt.startswith("add") or self.linetxt.startswith("sub") or
			self.linetxt.startswith("neg") or self.linetxt.startswith("and") or
			self.linetxt.startswith("or") or self.linetxt.startswith("not") or
			self.linetxt.startswith("eq") or self.linetxt.startswith("gt") or
			self.linetxt.startswith("lt")):
			return "C_ARITHMETIC"
		if(self.linetxt.startswith("push")):
			return "C_PUSH"
		if(self.linetxt.startswith("pop")):
			return "C_POP"
		if(self.linetxt.startswith("goto") or self.linetxt.startswith("if-goto")  ):
			return "C_GOTO"
		if(self.linetxt.startswith("if")):
			return "C_IF"
		if(self.linetxt.startswith("function")):
			return "C_FUNCTION"
		if(self.linetxt.startswith("return")):
			return "C_RETURN"
		if(self.linetxt.startswith("call")):
			return "C_CALL"
		if(self.linetxt.startswith("label")):
			return "C_LABEL"
		
		return
	def arg0(self):
		res = re.findall("(\\S+)", self.linetxt)
		if(len(res) >= 1):
			return str(res[0]).lower()
	def arg1(self):
		res = re.findall("(\\S+)", self.linetxt)
		if(len(res) >= 2):
			return str(res[1]).lower()
	def arg2(self):
		res = re.findall("(\\S+)", self.linetxt)
		if(len(res) >= 3):
			return str(res[2]).lower()

	def __init__(self, filename):
		self.linetxt = ""
		self.sourcefile = open(filename,'r')
		return

class CodeWriter:
	def setFileName(self):

		return
	def writeArthmetic(self):
		if(self.parser.commandType() != "C_ARITHMETIC"):
			return

		if(self.parser.arg0().startswith("add")) :
			self.add()
			return

		if(self.parser.arg0().startswith("sub")) :
			self.sub()
			return
		if(self.parser.arg0().startswith("neg")) :
			self.neg()
			return
		if(self.parser.arg0().startswith("eq")) :
			self.eq()
			return
		if(self.parser.arg0().startswith("gt")) :
			self.gt()
			return
		if(self.parser.arg0().startswith("lt")) :
			self.lt()
			return

	def eq(self):
		self.outline("R14=0")

		self.stackdec()
		self.outline("R13=D")
		self.stackinc()
		self.outline("D=R13-D")
		self.outline("@{0}}".format(self.filename))
		self.outline("D;JNE")
		self.outline("@65535")
		self.outline("D=A")
		self.outline("(end0)")
		self.stackinc()

		return
	def gt(self):
		self.stackdec()
		self.outline("R13=D")
		self.stackinc()
		self.outline("D=R13-D")
		self.stackinc()
		return
	def lt(self):
		self.stackdec()
		self.outline("D=-D")
		self.stackinc()
		return
	def neg(self):
		self.stackdec()
		self.outline("D=-D")
		self.stackinc()
		return
	def add(self):
		self.stackdec()
		self.outline("@R13")
		self.outline("M=D")
		self.stackdec()
		self.outline("@R13")
		self.outline("D=D+M")
		self.stackinc()
		return
	def sub(self):
		self.stackdec()
		self.outline("@R13")
		self.outline("M=D")
		self.stackdec()
		self.outline("@R13")
		self.outline("D=D-M")
		self.stackinc()
		return

	def stackinc(self):  ## 堆栈压入D数据
		self.outline("@SP")
		self.outline("A=M")
		self.outline("M=D")

		self.outline("@SP")
		self.outline("M=M+1")
		return
	def  stackdec(self): ## 堆栈弹出到D
		self.outline("@SP")
		self.outline("M=M-1")

		self.outline("A=M")
		self.outline("D=M")
		return

	def writePushPop(self):
		if(self.parser.commandType() != "C_PUSH" and self.parser.commandType() != "C_POP"):
			return

		if(self.parser.commandType() == "C_PUSH"):
			self.dopush()
			return
		if(self.parser.commandType() == "C_POP"):
			self.dopop()
			return
	def dopop(self):
		if(self.parser.arg1() == "static"):
			self.stackdec()
			self.outline("@{0}.{1}", self.filename , self.parser.arg2())
			self.outline("M=D")
			return
		if(self.parser.arg1() == "constant"):
			self.stackdec()
			return
		if(self.parser.arg1() == "this" or self.parser.arg1() == "that"):
			self.stackdec()
			self.outline("@R{0}".format(self.baseAddr[self.parser.arg1()]))
			self.outline("M=D")
			return
		if(self.parser.arg1() == "pointer" or self.parser.arg1() == "static" or self.parser.arg1() == "temp"):
			self.stackdec()
			self.outline("@R{0}".format(self.baseAddr[self.parser.arg1()] + int(self.parser.arg2())))
			self.outline("M=D")
			return
		if(self.parser.arg1() == "local" or self.parser.arg1() == "argument" ):
			self.stackdec()
			self.outline("@R13")
			self.outline("M=D")
			self.outline("@{0}".format("LCL" if self.parser.arg1() == "local" else "ARG"))
			self.outline("D=A")
			self.outline("@{0}".format(self.parser.arg2()))
			self.outline("A=D+A")
			self.outline("D=A")
			self.outline("@R13")
			self.outline("M=D")
			return


	def dopush(self):

		if(self.parser.arg1() == "static"):
			self.outline("@{0}.{1}", self.filename , self.parser.arg2())
			self.outline("D=M")
			self.stackinc()
			return
		if(self.parser.arg1() == "constant"):
			self.outline("@{0}".format( self.parser.arg2()))
			self.outline("D=A")
			self.stackinc()
		if(self.parser.arg1() == "this" or self.parser.arg1() == "that"):
			self.outline("@R{0}".format(self.baseAddr[self.parser.arg1()]))
			self.outline("D=M")
			self.stackinc()
		if(self.parser.arg1() == "pointer" or self.parser.arg1() == "static" or self.parser.arg1() == "temp"):
			self.outline("@R{0}".format(self.baseAddr[self.parser.arg1()] + int(self.parser.arg2())))
			self.outline("D=M")
			self.stackinc()
		if(self.parser.arg1() == "local" or self.parser.arg1() == "argument" ):
			self.outline("@{0}".format("LCL" if self.parser.arg1() == "local" else "ARG"))
			self.outline("D=A")
			self.outline("@{0}".format(self.parser.arg2()))
			self.outline("A=D+A")
			self.outline("D=M")
			self.stackinc()
			return

	def outline(self, str):
		self.output.write(str + "\n");


	def __init__(self, filename, output, parser):
		self.filename = filename
		self.baseAddr = {
			"register":0,
			"static":16,
			"stack":256,
			"heap":2048,
			"memory":16384,


			"local":3048,
			"argument":2048,
			"constant":2,
			"this":3,
			"that":4,
			"pointer":3,
			"temp":5,
		}
		self.output = output
		self.parser = parser

		# 初始化堆栈指针
		self.outline("@256")
		self.outline("D=A")
		self.outline("@SP")
		self.outline("M=D")

		# 初始化local指针
		self.outline("@3048")
		self.outline("D=A")
		self.outline("@LCL")
		self.outline("M=D")

		# 初始化arguments指针
		self.outline("@2048")
		self.outline("D=A")
		self.outline("@ARG")
		self.outline("M=D")

		return





def parseFile(file, output):
	filename1 = filename(file)

	parser = Parser(file)
	codeWriter = CodeWriter(filename1, output, parser)

	while parser.hasMoreCommands():
		if(parser.commandType() == "C_ARITHMETIC"):
			codeWriter.writeArthmetic()
			continue
		if(parser.commandType() == "C_PUSH" or parser.commandType() == "C_POP"):
			codeWriter.writePushPop()
			continue

	return



def scanfiles(dir, output):
	for filepath,dirnames,filenames in os.walk(dir):
		for filename in filenames:
			if(filename.endswith(".vm")):
				parseFile(os.path.join(filepath, filename), output)
	return


def start(srouceFileOrDir):
	# file.write(stringb)

	srouceFileOrDir = os.path.realpath(srouceFileOrDir)
	if(srouceFileOrDir.endswith("\\")):
		srouceFileOrDir = srouceFileOrDir[0: len(srouceFileOrDir)  - 1]

	outputname = srouceFileOrDir[ srouceFileOrDir.index("\\"):]
	if(os.path.isfile(srouceFileOrDir)):
		outputname = srouceFileOrDir[ srouceFileOrDir.rfind("\\") + 1: len(srouceFileOrDir) - 3]
		if(False == srouceFileOrDir.endswith(".vm")) :
			print("invalid file -> " + srouceFileOrDir)
			return
	
	outputname = outputname + ".asm"
	outputfile = open(outputname, "w")


	if(os.path.isfile(srouceFileOrDir)):
			parseFile(srouceFileOrDir, outputfile)
	else:
		scanfiles(srouceFileOrDir, outputfile)
				

	outputfile.close()
	return


if(len(sys.argv) == 1) :
  print("not found source file to compiler!");
  sys.exit();


srouceFileOrDir  =sys.argv[1];
start(srouceFileOrDir)
