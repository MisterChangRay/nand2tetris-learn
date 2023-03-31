
import sys
import re
import os
from JackTokenizer import JackTokenizer

from pathlib import Path



class CompilationEngine:

	def error(self, line):
		print("error occen with line {0}: {1}".format(self.line, line))
		return

	def compileClass(self):
		self.outxml("<class>")
		while(self.tokenizer. hasMoreCommands()):
			tmp = self.tokenizer.advance()
			
			if(tmp.type == "keyword"):
				if(tmp.val == "method" or tmp.val == "function"):
					self.compileSubroutine()
				elif(tmp.val == "field" or tmp.val == "static"):
					self.compileClassVarDec()
				else:
					self.error()
			elif(tmp.type == "symbol"):
				self.outxml("<symbol>{0}</symbol>".format(tmp.val))
			elif(tmp.type == "identifier"):
				self.outxml("<symbol>{0}</symbol>".format(tmp.val))
			else:
				self.error()
		self.outxml("</class>")

		return
	def compileClassVarDec(self):
		return
	def compileSubroutine(self):
		return
	def compileParameterList(self):
		return
	def compileVarDec(self):
		return
	def compileStatements(self):
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
	def outxml(self, line):
		self.xmlfile.write(line  + "\n");

	def outline(line):
		self.outputfile.write(line  + "\n");
	def __init__(self, inputfile, outputfile):
		self.inputfile =  open(inputfile, "r");
		self.outputfile = open(outputfile, "w");

		xmlfilepath = self.inputfile.name[:len(self.inputfile.name)-5]
		xmlfilepath = xmlfilepath + "2.xml"
		self.xmlfile = open(xmlfilepath, "w")


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
