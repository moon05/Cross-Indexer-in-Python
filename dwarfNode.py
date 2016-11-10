import re
import sys

class DWNode:
<<<<<<< HEAD
	def __init__(self, Name, Global, FileName, StartRow, EndRow):
		self._name = Name
		self._FileName = FileName
		self._StartRow = StartRow
		self._EndRow = EndRow
		if (Global is None):
			self._Global = False
		else:
			self._Global = Global

	@property
	def Name(self):
		return self._name
	@Name.setter
	def Name(self, val):
		self._name = val

	@property
	def Global(self):
		return self._Global
	@Global.setter
	def Global(self, val):
		self._Global = val
=======
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
>>>>>>> 8f2539f68c76770f7a9b65095d5d095b38f70571

	@property
	def FileName(self):
		return self._FileName
	@FileName.setter
	def FileName(self, val):
		self._FileName = val

	@property
<<<<<<< HEAD
	def StartRow(self):
		return self._StartRow
	@StartRow.setter
	def StartRow(self, val):
		self._StartRow = val

	@property
	def EndRow(self):
		return self._EndRow
	@EndRow.setter
	def EndRow(self, val):
		self._EndRow = val

=======
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
>>>>>>> 8f2539f68c76770f7a9b65095d5d095b38f70571

