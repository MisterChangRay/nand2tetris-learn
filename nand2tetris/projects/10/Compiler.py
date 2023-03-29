
import sys
import re
import os
from JackTokenizer import JackTokenizer

from pathlib import Path







def filename(file):
	return Path(file).stem

def parseFile(file):
	token = JackTokenizer(file)
	token.start()
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
