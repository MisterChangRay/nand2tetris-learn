
import sys
import re
import os
from pathlib import Path

class Parser:
	def hasMoreCommands():
		return
	def advance():
		return
	def commandType():
		return
	def arg1():
		return
	def arg2():
		return
	def __init__(self):
		return

class CodeWriter:
	def setFileName():
		return
	def writeArthmetic():
		return
	def writePushPop():
		return

	def __init__(self):
		return


def parseFile(file, output):
	return

def scanfiles(dir, output):
	return


def start(srouceFileOrDir):
	# file.write(stringb)

	srouceFileOrDir = os.path.realpath(srouceFileOrDir)
	if(srouceFileOrDir.endswith("\\")):
		srouceFileOrDir = srouceFileOrDir[0: len(srouceFileOrDir)  - 1]

	outputname = srouceFileOrDir[ srouceFileOrDir.index("\\"):]
	if(os.path.isfile(srouceFileOrDir)):
		outputname = srouceFileOrDir[ srouceFileOrDir.rfind("\\") + 1: len(srouceFileOrDir) - 3]
	
	outputname = outputname + ".asm"
	outputfile = open(outputname, "w")


	if(srouceFileOrDir.endswith("vm")):
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