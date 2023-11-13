import sys
sys.path.insert(0, '../src')
from WordsSelector import WordsSelector

class GraphTest():
	def __init__(self, pathOfObjectDirectory='../bin/similarWords/'):
		self.__wordsSelector = WordsSelector()

	def runTest(self):
		cleanWordsSet = [[('pue', 1.05), ('ke', 0.8), ('pe', 0.7803836094158675), ('ue', 0.7578901482127289), ('pu', 0.7330427201394943)],
						[('casualidad', 1.3), ('calidad', 0.932081175939118), ('casada', 0.8999999999999999), ('salida', 0.8999999999999999), ('cualidad', 0.8409285193036106)],
						[('nonatos', 0.7375), ('notamos', 0.7375), ('enanos', 0.675), ('eramos', 0.5817375377100992), ('oramos', 0.3970657951443758)],
						[('em', 0.9666666666666666), ('en', 0.9666666666666666), ('e', 0.33743462414281844), ('m', 0.3340493969082167), ('n', 0.3337011537562982)],
						[('elam', 1.3), ('ela', 1.05), ('lam', 0.8282909930715935), ('am', 0.8), ('el', 0.8)],
						[('mercado', 0.41666666666666663), ('pecado', 0.26791923724060573), ('recado', 0.13679192372406057), ('serrado', 0.11761388421511809), ('remera', 0.11428304355954384)]]
		
		# cleanWordsSet = [[('de', 1.3), ('e', 0.5018599809906249), ('d', 0.5001511938377455), ('-', -1), ('-', -1)],
		# 				[('nada', 1.1), ('tada', 0.800027490356977), ('ada', 0.6000691790301945), ('nad', 0.6000543765302839), ('tad', 0.6000190317855993)],
		# 				[('hasta', 1.3), ('has', 0.8999999999999999), ('asta', 0.8004063738008932), ('hata', 0.800029329303994), ('hast', 0.8000257446112836)],
		# 				[('luego', 0.925), ('lego', 0.5003833695437487), ('lelo', 0.5001208769504246), ('ludo', 0.5000953979853842), ('leo', 0.38225202449140827)]]
		self.__wordsSelector.getPhrase(cleanWordsSet, selector='contextGraph')


test = GraphTest()
test.runTest()