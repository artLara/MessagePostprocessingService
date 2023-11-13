import sys
sys.path.insert(0, '../src')
sys.path.append('../')
sys.path.append('../../')
sys.path.append('../../../')
import pandas as pd
from src.PhraseCleaner import PhraseCleaner

class PhraseCleanerTest():
    def __init__(self):
        self.__phraseCleaner = PhraseCleaner()

    def metric(self):
        pass

    def runTest(self):
        print('=================Testing PhraseCleaner=======================')
        # df = pd.read_csv('noisePhrases/dataset.csv')
        # for index in df.index:
        #     target = df['target'][index]
        #     noisePhrase = open("noisePhrases/"+df['file_name'][index], "r")
        #     cleanPhrase = self.__phraseCleaner.cleanSentence(noisePhrase.read(),selector='max')
        #     print(cleanPhrase)
        cleanPhrase = self.__phraseCleaner.cleanSentence('holav comoe estuas',selector='max')
        print(cleanPhrase)



test = PhraseCleanerTest()
test.runTest()
