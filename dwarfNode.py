import re
import sys

class DWNode:
	def __init__(self, DW_AT_NAME, FileName, LineBounds, OffsetBounds):
		self._DW_AT_NAME = DW_AT_NAME
		self._FileName = FileName
		self._LineBounds = LineBounds
		self._OffsetBounds = OffsetBounds

	@property
	def DW_AT_NAME(self):
		return self._DW_AT_NAME
	@DW_AT_NAME.setter
	def DW_AT_NAME(self, val):
		print "setter of DW_AT_NAME called"
		self._DW_AT_NAME = val

	@property
	def FileName(self):
		return self._FileName
	@FileName.setter
	def FileName(self, val):
		self._FileName = val

	@property
	def LineBounds(self):
		return self._LineBounds
	
	@LineBounds.setter
	def LineBounds(self, val):
		self._LineBounds = val

	@property
	def OffsetBounds(self):
		return self._OffsetBounds
	@OffsetBounds.setter
	def OffsetBounds(self, val):
		self._OffsetBounds = val

	def isinBounds(self, lineNumber, offset, fileName):
		return lineNumber - self.LineBounds[0] >= 0 \
				and self.LineBounds[1] - lineNumber >= 0 \
				and offset - self.OffsetBounds[0] >= 0 \
				and self.OffsetBounds[1] - offset >= 0 \
				and self.FileName == fileName \

	def distanceFromStart(self, lineNumber, offset):
		return (lineNumber - self.LineBounds[0]) + (offset - self.OffsetBounds[0])


#Sample Node
# first = DWNode("main", "picoc.c", (1,15), (100,200))
# print first.DW_AT_NAME
# print first.FileName
# print first.LineBounds
# print first.OffsetBounds
# print "checking setters"
# first.DW_AT_NAME = "parse"
# print first.DW_AT_NAME
# print first.isinBounds(12, 150, "picoc.c")

