from dwarfNode import *
import re
import sys
import json

class Parser:
	def __init__(self,DwarfFile):
		self.dumpFile = DwarfFile

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

		return LocalSymbols.keys()

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
		
		return CompileUnits.keys()

	def processSubProgram(self, linkedList):
		return 0

	def captureSubPrograms(self):
		f = open(self.dumpFile)
		a = f.readlines()
		fileLength = len(a)
		count = 0
		bigLink = list()
		
		#getting all the subprogram sections
		for i in range(0, fileLength):
			m = re.findall(r"DW_TAG_subprogram", a[i])
			if not m:
				pass
			else:
				count += 1
				smLink = list()
				for j in range(1,10):
					smLink.append(a[i+j].rstrip().lstrip().strip("\n"))
				bigLink.append(smLink)
				i += 11

		return bigLink



picoc = Parser("dwarfPicoc.txt")


#sample capturing .h files and .c files on dwarfPicoc
#WORKS
# print picoc.captureLocalSymbols()
# print picoc.captureCompileUnits()

a = picoc.captureSubPrograms()
h = dict()
for i in a[0]:
	k = i.split()
	h[k[0]] = k[-1:]

print json.dumps(h, indent=2) 

def processSubProgram(listOfSubPrg):
	SubProgams = listOfSubPrg
	for a in SubProgams:
		return 0
	return 0

