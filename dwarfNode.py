import re
import sys

class DWNode:
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

	@property
	def FileName(self):
		return self._FileName
	@FileName.setter
	def FileName(self, val):
		self._FileName = val

	@property
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


