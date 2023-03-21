
import sys
import re




class Parser:
  
  def  hasMoreCommands(self):
    while True:
      self.line = self.sourcefile.readline()
      if(not self.line) :
        return False
      
      
      if(len(self.line) > 0):
        if( re.match(r".*//.*", self.line)):
          self.line = self.line[0 : self.line.index("//")]

        self.line = self.line.strip()
        if(len(self.line) > 0) :
          return True

  def advance(self):
    return self.line



  def commandType(self):
    lineTrim = self.line.strip()

    if(self.line.startswith("@")) :
      return "A_CMD"

    if(self.line.startswith("(") & self.line.endswith(")")) :
      return "L_CMD"

    return "C_CMD"


  def symble(self):
    if(self.line.startswith("(")):
      return self.line[1:len(self.line) - 1]
    else:
      return self.line[1:]

  def dest(self):
    res = self.line.split("=")
    return res[0]
    

  def comp(self):
    res = self.line.split("=")
    return res[1]


  def jump(self):
    res = self.line.split(";")
    return res[0]

  def __init__(self, sourcefile):
    self.sourcefile = open(sourcefile,'r')
    self.readIndex = 0
    self.parserIndex = 0
    self.line = ""
    


class Code:
  def dest(str):
    if(str == "M"):
      return "001" 
    elif(str == "D"):
      return "010" 
    elif(str == "MD"):
      return "011" 
    elif(str == "A"):
      return "100" 
    elif(str == "AM"):
      return "101" 
    elif(str == "AD"):
      return "110" 
    elif(str == "AMD"):
      return "111" 
    else :
      return "000" 


  def comp(str):
    if(str == "0"):
      return "101010" 
    elif(str == "1"):
      return "111111" 
    elif(str == "-1"):
      return "111010" 
    elif(str == "D"):
      return "001100" 
    elif(str == "A" or str == "M"):
      return "110000" 
    elif(str == "!D"):
      return "001101" 
    elif(str == "!A" or str == "!M"):
      return "110001" 
    elif(str == "-D"):
      return "001111" 
    elif(str == "-A" or str == "-M"):
      return "110011" 
    elif(str == "D+1"):
      return "011111" 
    elif(str == "A+1" or str == "M+1"):
      return "110111" 
    elif(str == "D-1"):
      return "001110" 
    elif(str == "A-1" or str == "M-1"):
      return "110010" 
    elif(str == "D+A" or str == "D+M"):
      return "000010" 
    elif(str == "D-A" or str == "D-M"):
      return "010011" 
    elif(str == "A-D" or str == "M-D"):
      return "000111" 
    elif(str == "D&A" or str == "D&M"):
      return "000000" 
    elif(str == "D|A" or str == "D|M"):
      return "010101" 



  def jump(str):
    if(str == "JGT"):
      return "001" 
    elif(str == "JEQ"):
      return "010" 
    elif(str == "JGE"):
      return "011" 
    elif(str == "JLT"):
      return "100" 
    elif(str == "JNE"):
      return "101" 
    elif(str == "JLE"):
      return "110" 
    elif(str == "JMP"):
      return "111" 
    else :
      return "000" 

  def __init__(self):
    return
   


class SymbolTable:
  def addEntry(self, symbol , addr):
    self.map[symbol] = addr
    return

  def contains(self, symbol):
    return self.map.__contains__(symbol)

  def GetAddress(self, symbol):
    return self.map[symbol]

  def __init__(self):
    self.map = {
      "SP":0, "LCL":1, "ARG":2, "THIS":3, "THAT":4,
      "R0":0, "R1":1, "R2":2, "R3":3, "R4":4,"R5":5, "R6":6, "R7":7, "R8":8, 
      "R9":9,"R10":10, "R11":11, "R12":12, "R13":13, "R14":14, "R15":15,
      "SCREEN": 16384, "KBD":24576

    }

stringb = ""
def writeline(str) :
  global stringb;
  stringb = stringb + str + "\r";

def preloadM(str):
  res = re.match(r".*M(\[(\d+)\]).*", str)

  if(res) :
    # 宏指令M[123]
    writeline("{:0>16d}".format(int(bin(int(res[2]))[2:])))
    str = str.replace(res[1], "")
    return str
  return str




if(len(sys.argv) == 1) :
  print("not found source file to compiler!");
  sys.exit();


sourceFileName  =sys.argv[1];
parser = Parser(sourceFileName);
table = SymbolTable();

storePc = 0
while parser.hasMoreCommands():
  line = parser.advance();

  if(parser.commandType() == 'L_CMD' and False == table.contains(parser.symble())) :
    table.addEntry(parser.symble(), storePc)
  else :
    storePc = storePc + 1





storePc = 15
parser = Parser(sourceFileName);
while parser.hasMoreCommands():
  line = parser.advance();


  if(parser.commandType() == 'A_CMD'):
    line = line[1:]
    if(re.match(r"^[0-9]+$", line)):
      writeline("{:0>16d}".format(int(bin(int(line))[2:])))
    else:
      if(table.contains(line)):
        writeline("{:0>16d}".format(int(bin(int(table.GetAddress(line)))[2:])))
      else :
        storePc = storePc + 1
        print(line, storePc)

        table.addEntry(line, storePc)
        writeline("{:0>16d}".format(int(bin(int(table.GetAddress(line)))[2:])))


  if(parser.commandType() == 'C_CMD'):
    prefix = "111"
    prefix0 = prefix + "0"


    if(re.match(r".+;.+", line)) :
      # 比较跳转指令
      line0 = line.split(";")[0]
      line1 = line.split(";")[1]
      if(line0 == "0"):
        comp = Code.comp("0")        
      else :
        line0 = preloadM(line0)
        if(re.match(".*M.*", line0)):
          prefix0 = prefix + "1"
        comp = Code.comp(line0)
     
      dest = Code.dest("none");
      jmp = Code.jump(line1);
      writeline(prefix0 + comp + dest + jmp)
    else:
      line0 =line.split("=")[0];
      line1 =line.split("=")[1];
      line = preloadM(line);
      if(re.match(".*M.*", line1)):
        prefix0 = prefix + "1"
      # 简单的操作指令
      comp = Code.comp(line1)
      dest = Code.dest(line0);
      jmp = Code.jump("none");
      writeline(prefix0 + comp + dest + jmp)
      
file = open(sourceFileName[0:len(sourceFileName) - 3] + "hack", "w")
file.write(stringb)
file.close()

    






