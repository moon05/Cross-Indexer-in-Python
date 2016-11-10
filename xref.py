import sys
import re
import os
import fnmatch
import glob
from dwarfParser import *
from dwarfNode import *
import subprocess


# for finding out valid variable names
regex4 = r'\w+\d*_*'

def create_path_list(input_filename_array, input_directory):
	result = []
	for dirName, subdirList, fileList in os.walk(input_directory):
		for fname in fileList:
			if fname in input_filename_array:
				result.append(os.path.join(dirName,fname))

	return result

def htmlFormat(directory,filename, content):
	f = open(directory+'/'+filename+'.html','w')
	f.write('<html>\n')
	f.write('<body>\n')
	f.write('<pre>\n')

	for i in content:
		f.write('<a>' + i + '</a>')

	f.write('</pre>\n')
	f.write('</body>\n')
	f.write('</html>\n')
	f.close()


def convertToHTML(fileList):
	directory = './htmlFiles'
	if not os.path.exists(directory):
		os.makedirs(directory)

	hashForIndex = dict()
	for sourceFile in fileList:
		if '.c' in sourceFile:
			stringSplit = sourceFile.split('.c')
			with open(sourceFile) as g:
				content = g.readlines()
			htmlFormat(directory,stringSplit[0],content)
		if '.h' in sourceFile:
			stringSplit = sourceFile.split('.h')
			with open(sourceFile) as g:
				content = g.readlines()
			htmlFormat(directory,stringSplit[0],content)

	print "Success"
	return	


def main():
	if len(sys.argv) < 2:
		print "usage: python xref.py <program>"
	
	else:
		program = sys.argv[1]
		output = subprocess.check_output("dwarfdump program", shell=True)
		with open("dwarfText.txt", "w") as f:
			f.write(output)

		with open("./dwarfText.txt") as k:	
			parser = Parser("./dwarfText.txt")
			parser.parseGlobal(k)

		varList, funcList = parser._variables, parser._functions
		HList, CList = parser._LocSym, parser._ComUnit

		HFilesList = create_path_list(HList, './')
		CFilesList = create_path_list(CList, './')



if __name__ == '__main__':
	main()
