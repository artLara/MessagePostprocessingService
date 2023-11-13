import sys
sys.path.insert(0, '../../src')
# sys.path.insert(0, '../src')

from SpellingCorrectionTrajectory import SpellingCorrectionTrajectory
from spellchecker import SpellChecker
import pickle

class VocabularyTablesGenerator():
    def __init__(self):
        self.__spell = SpellChecker(language='es')
        self.__vocabByLen = self.loadVocabulary()
        self.__st = SpellingCorrectionTrajectory(pathFiles='../../bin/spellingCorrectionTrajectory/')

    def loadVocabulary(self):
        vocabByLen = []
        for i in range(100):
            vocabByLen.append([])

        for word in self.__spell:
            vocabByLen[len(word)].append(word)

        return vocabByLen
    def generate(self, lenWord, path='../../bin/spellingCorrectionTrajectory/tableWords/'):
        tables = {}
        for validWord in self.__vocabByLen[lenWord]: #Iterate words with the same longitud
            # if 'dile' == validWord:
            #     tmp = self.__st.makeTableTrajectories(validWord, verbose=True)
            # else:
            #     tmp = self.__st.makeTableTrajectories(validWord)

            tmp = self.__st.makeTableTrajectories(validWord)
            tables[validWord] = tmp

        # self.__st.printTable(tables['dile'])
        # self.__st.printTable(tables['at'])


        with open(path+'tables'+str(lenWord)+'.pkl', 'wb') as handle:
            pickle.dump(tables, handle, protocol=pickle.HIGHEST_PROTOCOL)

generator = VocabularyTablesGenerator()
for long_word in range(20,23):
    generator.generate(long_word)
