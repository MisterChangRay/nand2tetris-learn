
import sys
import re
import os
from pathlib import Path








def filename(file):
	return Path(file).stem

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
		if(False == srouceFileOrDir.endswith(".jack")) :
			print("invalid file -> " + srouceFileOrDir)
			return
	
	outputname = outputname + ".vm"
	outputfile = open(outputname, "w")

	write = CodeWriter(None, outputfile, Parser(None))
	write.writeInit()
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
