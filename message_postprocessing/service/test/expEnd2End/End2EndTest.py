import sys

sys.path.insert(0, '../../src')
sys.path.insert(0, '../bin/spellingCorrectionTrajectory/')
sys.path.append('../')
sys.path.append('../../')
sys.path.append('../../../')
import pandas as pd
from src.PhraseCleaner import PhraseCleaner
from SpellingCorrectionTrajectory import SpellingCorrectionTrajectory
class End2EndTest():
    def __init__(self):
        self.__phraseCleaner = PhraseCleaner()
        self.__st = SpellingCorrectionTrajectory(pathFiles='../../bin/spellingCorrectionTrajectory/')

    def metric(self):
        pass

    def runGetSetsTest(self):
        print('=================Testing PhraseCleaner=======================')
        confidenses=[0.0,0.5,0.6,0.7,0.8]
        # confidenses=[0.8]

        for confidence in confidenses:
            df = pd.read_csv('confidence{}.csv'.format(confidence))
            alg1_list = []
            sys_list = []
            tra_list = []
            union_list = []
            for index in df.index:
                target = df['target'][index]
                noiseMessage = df['noiseMessage'][index]
                set_alg1, set_sym, set_tra, set_union = self.__phraseCleaner.getWordsSet(noiseMessage, maxOptWords=5)
                alg1_list.append(set_alg1)
                sys_list.append(set_sym)
                tra_list.append(set_tra)
                union_list.append(set_union)
                # print('Alg 1:', set_alg1)
                # print('Alg sym:', set_sym)
                # print('Alg tra:', set_tra)
                # print('Alg union:', set_union)
                # break


            df_alg1 = pd.DataFrame(alg1_list)
            df_sys = pd.DataFrame(sys_list)
            df_tra = pd.DataFrame(tra_list)
            df_union = pd.DataFrame(union_list)

            pd.concat([df,df_alg1,df_sys,df_tra,df_union], ignore_index=True, axis=1).rename(columns={0: "target", 1: "jsonfile", 2:"noiseMessage", 3:"alg1", 4:"sys", 5:"tra", 6:"union"}).to_csv('confidence{}.csv'.format(confidence),index=False)

            # break

    def __getListFromString(self, m):
        wordSets = m.split('-')
        validWordsSet = []
        for validWords in wordSets:
            if len(validWords) < 1:
                continue

            words = validWords.split()
            cleanWords = []
            for word in words:
                if word == '' or word ==' ':
                    continue

                cleanWords.append((-1, word))
            validWordsSet.append(cleanWords)

        return validWordsSet
    
    def runMakePhraseTest(self, selector='max'):
        confidenses=[0.0,0.5,0.6,0.7,0.8]
        confidenses=[0.0]
        for confidence in confidenses:
            df = pd.read_csv('confidence{}.csv'.format(confidence))
            messages = []
            sys_list = []
            tra_list = []
            union_list = []
            for index in df.index:
                sets_string = df['alg1'][index]
                validWords = self.__getListFromString(sets_string)
                print(validWords)
                message = self.__phraseCleaner.builtMessage(validWords, selector='contextGraph')
                print(message)
                break
            break

test = End2EndTest()
test.runMakePhraseTest()
