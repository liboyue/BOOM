from pymetamap import MetaMap
import os
import diskcache as dc

class Singleton:
	def __init__(self,cls):
		self._cls = cls
	def Instance(self):
		try:
			return self._instance
		except AttributeError:
			self._instance = self._cls()
			return self._instance

@Singleton
class SingletonMetaMap:
	def __init__(self):
		self.mm = MetaMap.get_instance('/home/khyathi/installations/public_mm/bin/metamap')
		self.start_command = "/Users/khyathi/installations/public_mm/bin/skrmedpostctl start"
		self.stop_command = "/Users/khyathi/installations/public_mm/bin/skrmedpostctl stop"
	
	def startMetaMap(self):
		os.system(self.start_command)

	def stopMetaMap(self):
		os.system(self.stop_command)

@Singleton
class SingletonUMLSCache:
	def __init__(self):
		self.cache = dc.Cache('umlsCache')

@Singleton
class SingletonSNOMEDCTCache:
	def __init__(self):
		self.cache = dc.Cache('snomedctCache')


'''
x = SingletonMetaMap.Instance()
print x.mm
'''
