
class SymbolTable:
	def add(self, name, dataType, type):
		if(self.hasSymbol(name)):
			raise ValueError(f"compilation type error! has more definetion " + name)
		self.tables[name] = Symbol(name, dataType, type, self.countType(type) + 1)

	def countType(self, type):
		count = 0
		for k in self.tables:
			if(self.tables[k].type == type):
				count += 1
		return count

	def hasSymbol(self, name,):
		res = self.tables.get(name)
		if(res == None):
			return False
		return True

	def __init__(self,  parent):
		self.tables = dict()
		self.next = None
		if(parent != None):
		    self.parent  = parent
        
class Symbol:
	def __init__(self, name, dataType, type, index):
		self.name = name
		self.dataType = dataType
		self.type = type
		self.index = index
		pass


p = SymbolTable(None)
p.add("A", "int", "static")
p.add("b", "int", "static")

print(222)
