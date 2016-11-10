from dwarfNode import *
import re
import sys
import json

#returns the next line
#gets pointer back to the previous line
def peek_line(f):
	pos = f.tell()
	line = f.readline()
	f.seek(pos)

	if (len(line) > 0):
		return True, line
	else:
		return False, ''

def searchHashKey(hashTable, key):
	for a in hashTable.keys():
		if key in a:
			return hashTable[a]
	
	return None

#prepares a dictionary for all the debug lines
def parseLineMapping(dwarfFile):
	bigHash = dict()
	with open(dwarfFile) as f:
		content = f.readlines()
	a = int(len(content))
	wh = a-1
	i = 0
	while (i <= wh):
		if '<pc>' in content[i]:
			littleHash = dict()
			fileName = ''
			i += 1
			while (i<=wh):
				# Add hex and row, col to little hash
				if 'NS ET' in content[i]:
					splitted = content[i].split('NS ET')[0]
					hexa, row, col = current.strip().replace('[','').replace(',','').replace(']','').split()
					row, col = int(row), int(col)
					littleHash[int(hexa,16)] = (row, col)
					break
				elif 'uri' in content[i]:
					splitted = content[i].split("uri: ")
					b = splitted[-1:][0]
					a = b[1:len(b)-2]
					fileName = a
					splitted =  splitted[0]
					hexa, row, col, blah = splitted.replace('[','').replace(',','').replace(']','').split()
					row, col = int(row), int(col)
					littleHash[int(hexa,16)] = (row, col)
				else:
					current = content[i]
					if 'NS' in current:
						current = current.split('NS')[0]
						hexa, row, col = current.strip().replace('[','').replace(',','').replace(']','').split()
						row, col = int(row), int(col)
						littleHash[int(hexa,16)] = (row, col)
					elif 'DI' in current:
						current = current.split('DI')[0]
						hexa, row, col = current.strip().replace('[','').replace(',','').replace(']','').split()
						row, col = int(row), int(col)
						littleHash[int(hexa,16)] = (row, col)
				i += 1
			bigHash[fileName] = littleHash
		i += 1

	return bigHash

class Parser:
	def __init__(self,DwarfFile):
		self.dumpFile = DwarfFile
		self.ROW_COl_MAP = parseLineMapping(self.dumpFile)
		self._variables = list()
		self._functions = list()
		self._LocSym = list()
		self._ComUnit = list()

	#returns a list of .h files
	def captureLocalSymbols(self):
		LocalSymbols = dict()
		with open(self.dumpFile) as f:
			for line in f:
				m = re.findall(r"\w+\.h", line)
				if not m:
					pass
				else:
					for i in m:
						LocalSymbols[i] = True
		self._LocSym = LocalSymbols.keys()
		return None

	#returns a list of .c files
	def captureCompileUnits(self):
		CompileUnits = dict()
		with open(self.dumpFile) as f:
			for line in f:
				m = re.findall(r"\w+\.c", line)
				if not m:
					pass
				else:
					for i in m:
						if i in CompileUnits.keys():
							pass
						else:
							CompileUnits[i] = True
		self._ComUnit = CompileUnits.keys()
		return None

	#lowPC in HEX
	#highPC in decimal
	#add up both of them
	#returns in decimal
	def endLineNumber(self, lowPC, highPC):
		low = int(lowPC, 16)
		high = highPC
		lineEnd = low + high
		return lineEnd

	def isSubProgram(self, line):
		regex = r'DW_TAG_subprogram'
		a = re.findall(regex, line)
		if a:
			return True
		else:
			return False

	def isLexicalScope(self, line):
		regex = r'DW_TAG_lexical_block'
		a = re.findall(regex, line)
		if a:
			return True
		else:
			return False

	def isVariable(self, line):
		regex = r'DW_TAG_variable'
		a = re.findall(regex, line)
		if a:
			return True
		else:
			return False

	def isFormalParameter(self, line):
		regex = r'DW_TAG_formal_parameter'
		a = re.findall(regex, line)
		if a:
			return True
		else:
			return False

	#find the position where DW is located at in the line
	def countIndentation(self, line):
		regex = r"DW"
		m = re.search(regex, line)

		if (m == None):
			return -1

		else:
			return m.start()

	#Parse Variable Info from DWARF
	def parseVariable(self, fileObject, indentation, endRow):
		hasLine, line = peek_line(fileObject)
		varNode = DWNode(None, None, None, None, None)

		while hasLine and (self.countIndentation(line) == indentation):
			fileObject.readline()

			if (re.findall('DW_AT_name', line)):
				a, b, value = line.partition('DW_AT_name')
				value = value.strip()
				varNode.name = value

			elif (re.findall('DW_AT_decl_file', line)):
				value = re.compile(r'\s+').split(line)[3]
				varNode.FileName = value

			elif (re.findall('DW_AT_decl_line', line)):
				lineHex = re.compile(r'\s+').split(line)[2]
				varNode.StartRow = int(lineHex,16)

			hasLine, line = peek_line(fileObject)

		varNode.EndRow = endRow
		return varNode

	def parseLexicalBlock(self, fileObject, indentation):
		hasLine, line =  peek_line(fileObject)
		lowPC = 0
		highPC = 0

		while hasLine and (self.countIndentation(line) == indentation):
			if (re.findall('DW_AT', line)):
				fileObject.readline()

			if (re.findall('DW_AT_low_pc', line)):
				#giving hex value
				lowPC = re.compile(r'\s+').split(line)[2]

			elif (re.findall('DW_AT_high_pc', line)):
				temp = re.compile(r'\s+').split(line)[2]
				reg = re.compile(r'>(.*)$')
				highPC = int(reg.search(temp).group(1))

			elif (re.findall('DW_TAG', line)):
				break

			hasLine, line = peek_line(fileObject)

		return lowPC, highPC

	def skipUnknownScope(self, fileObject, indentation):
		hasLine, line = peek_line(fileObject)
		
		while hasLine and (self.countIndentation(line) > indentation):
			fileObject.readline()
			hasLine, line = peek_line(fileObject)

	def parseScope(self, fileName, fileObject, indentation, endRow):
		hasLine, line = peek_line(fileObject)

		while hasLine and (self.countIndentation(line) == indentation):
			fileObject.readline()

			if self.isLexicalScope(line):
				a, b = self.parseLexicalBlock(fileObject, indentation + 2)
				
				if (a == 0):
					self.skipUnknownScope(fileObject, indentation)
					continue

				tempNUM = int(a,16)
				ending, b = searchHashKey(self.ROW_COl_MAP, fileName)[tempNUM]
				scopeEndRow = ending

				self.parseScope(fileName, fileObject, indentation + 2, scopeEndRow)

			if self.isVariable(line) or self.isFormalParameter(line):
				variableNode = self.parseVariable(fileObject, indentation + 2, endRow)
				self._variables.append(variableNode)

			hasLine, line = peek_line(fileObject)

	def parseFunction(self, fileObject, indentation):
		hasLine, line = peek_line(fileObject)
		indentationREGEX = r'<\s[0-9]+><0x[0-9a-fA-F]+>\s*'
		funcNode = DWNode(None, None, None, None, None)
		highPC = 0
		lowPC = 0

		while hasLine and (self.countIndentation(line) == indentation):
			if (re.findall('DW_AT', line)):
				fileObject.readline()

			if (re.findall('DW_AT_name', line)):
				a, b, value = line.partition('DW_AT_name')
				value = value.strip()
				funcNode.name = value

			elif (re.findall('DW_AT_decl_file', line)):
				value = re.compile(r'\s+').split(line)[3]
				funcNode.FileName = value

			elif (re.findall('DW_AT_decl_line', line)):
				lineHex = re.compile(r'\s+').split(line)[2]

				funcNode.StartRow = int(lineHex, 16)
			elif (re.findall('DW_AT_low_pc', line)):
				#giving hex value
				lowPC = re.compile(r'\s+').split(line)[2]

			elif (re.findall('DW_AT_high_pc', line)):
				temp = re.compile(r'\s+').split(line)[2]
				reg = re.compile(r'>(.*)$')
				highPC = int(reg.search(temp).group(1))

			elif (re.findall('DW_TAG', line)):
				break

			hasLine, line = peek_line(fileObject)

		temp_2 = int(lowPC,16)

		ending, b = searchHashKey(self.ROW_COl_MAP, funcNode.FileName)[temp_2]

		funcNode.EndRow = ending
		self.parseScope(funcNode.FileName, fileObject, indentation, funcNode.EndRow)

		return funcNode

	def parseGlobal(self, fileObject):
		line = fileObject.readline()
		funcNode = DWNode(None, None, None, None, None)

		self.captureLocalSymbols()
		self.captureCompileUnits()

		while len(line) != 0:
			if re.findall('DW_TAG_subprogram', line) and (self.countIndentation(line) == 20):
				fNode = self.parseFunction(fileObject, 22)
				fNode.Global = True
				self._functions.append(fNode)
			
			if re.findall('DW_TAG_variable', line) and (self.countIndentation(line) == 20):
				node = self.parseVariable(fileObject, 22, 0)
				node.Global = True
				self._variables.append(node)

			line = fileObject.readline()


#for 'hexstring space DW_TAG_*'
regex = r'<\s[0-9]+><0x[0-9a-fA-F]+>\s*\w+'
#for checking first line indentation with hex string
regex2 = r'<\s[0-9]+><0x[0-9a-fA-F]+>\s*' 
# for checking 2nd line indentation increase, re.findall[0], re.search.group()
regex3 = r'\s*' 
# for finding out valid variable names
regex4 = r'\w+\d*_*'



