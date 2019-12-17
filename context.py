import os
from threading import RLock
from datetime import datetime

import pyswip
import ctypes
from pyswip.prolog import PrologError

from application_settings import BASE_DIR

DEFAULT_RULES = [
	'''get_user_competitions(UserId, CompetitionId) :- 
		competition(CompetitionId), 
		user_competition(UserId, CompetitionId).''',
	'% section.facts'
]

USER_COMPETITION_FACT = 'user_competition({}, {}).'

COMPETITION_FACT = 'competition({}, {}).'

COMPETITION_FACT2 = 'competition({}).'

TIMESTAMP_FORMAT = '%d-%b-%Y (%H:%M:%S.%f)'

class PrologMT(pyswip.Prolog):
	"""Multi-threaded (one-to-one) pyswip.Prolog ad-hoc reimpl"""
	_swipl = pyswip.core._lib

	PL_thread_self = _swipl.PL_thread_self
	PL_thread_self.restype = ctypes.c_int

	PL_thread_attach_engine = _swipl.PL_thread_attach_engine
	PL_thread_attach_engine.argtypes = [ctypes.c_void_p]
	PL_thread_attach_engine.restype = ctypes.c_int

	@classmethod
	def _init_prolog_thread(cls):
		pengine_id = cls.PL_thread_self()
		if pengine_id == -1:
			pengine_id = cls.PL_thread_attach_engine(None)
			# Attach pengine to thread pengine_id
		if pengine_id == -1:
			raise pyswip.prolog.PrologError("Unable to attach new Prolog engine to the thread")

	class _QueryWrapper(pyswip.Prolog._QueryWrapper):
		def __call__(self, *args, **kwargs):
			PrologMT._init_prolog_thread()
			return super().__call__(*args, **kwargs)


class PrologKb:
	def __init__(self, file_path='{}/db.pro'.format(BASE_DIR)):
		assert file_path is not None
		self.__file_path = file_path.replace('\\', '/')		
		self.__kb_file = open(self.__file_path, 'a+')
		self.__guard = RLock()
		self.__kb = PrologMT()
		self.__prepare_file()		
		self.__kb.consult(self.__file_path)

	def __file_is_empty(self):
		return os.stat(self.__file_path).st_size == 0

	def __clear_file(self):
		self.__kb_file.close()
		self.__kb_file = open(self.__file_path, 'w').close()
		self.__kb_file = open(self.__file_path, 'a+')

	def __del__(self):
		self.__kb_file.close()

	def __prepare_file(self):
		if not self.__file_is_empty():
			return
		text_to_file = '\n'.join(DEFAULT_RULES)+'\n'
		self.__write(text_to_file)

	def __call(self, query):
		try:
			li = list(self.__kb.query(query))
			return li
		except PrologError:
			return None	
	
	# Writes data to self._kb_file.
	def __write(self, data):
		if len(data) > 0:
			self.__guard.acquire()
		
			self.__kb_file.write(data)
			self.__kb_file.flush()
			os.fsync(self.__kb_file.fileno())
			
			self.__kb.consult(self.__file_path)
			
			self.__guard.release()

	def __exists_u_c(self, userId, competitionId):
		userComps = self.__call(USER_COMPETITION_FACT.format(userId, competitionId))
		return len(userComps) != 0 if userComps else False

	def __exists_c(self, competitionId):
		cond = self.__call(COMPETITION_FACT2.format(competitionId))
		return len(cond) != 0 if cond else False

	def __add_competition(self, competitionId):
		compStr = '\n' + COMPETITION_FACT2.format(competitionId)
		self.__write(compStr)

	def add_user_competition(self, userId, competitionId):
		if self.__exists_u_c(userId, competitionId):
			return False
		
		if not self.__exists_c(competitionId):
			self.__add_competition(competitionId)
		
		compStr = '\n' + USER_COMPETITION_FACT.format(userId, competitionId)
		self.__write(compStr)
		return True

	def get_competitions(self):
		competitions = self.__call(COMPETITION_FACT2.format('Id'))
		if not competitions:
			return []
		return list(map(lambda x: x['Id'], competitions))
	
	def get_user_competitions(self, userId):
		userComps = self.__call('get_user_competitions({}, CompetitionId)'.format(userId))
		if not userComps:
			return []
		return list(map(lambda x: x['CompetitionId'], userComps))			
	

# Simple driver program.
# TODO: will be removed in future.
def main():

	kb = PrologKb()
	compets = kb.get_competitions()
	kb.add_user_competition(22, 1)
	kb.add_user_competition(22, 1)
	kb.add_user_competition(23, 2)
	kb.add_user_competition(23, 1)
	kb.add_user_competition(22,2)
	uComps = kb.get_user_competitions(22)
	uComps = kb.get_user_competitions(23)




	#comps = kb.get_competitions()

	# kb.add_exchange(366889066, 'EUR', True)
	# li = [('dollar', True), ('ether', False)]
	# kb.add_exchanges(74, li)

	# print(kb.get_crypto_currencies(74))	
	# print(kb.get_fiat_currencies(74))
	

if __name__ == '__main__':
	main()