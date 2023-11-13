import sys
sys.path.insert(0, '../../src')
sys.path.insert(0, '../bin/spellingCorrectionTrajectory/')

from PhraseCleaner import PhraseCleaner
from SpellingCorrectionTrajectory import SpellingCorrectionTrajectory

import numpy as np
import pandas as pd
class SpellingCorrectionTrajectoryTest():
	"""
	This file run the test for evaluate each algorithm which find the correct posible set of words.
	"""
	def __init__(self):
		self.__st = SpellingCorrectionTrajectory(pathFiles='../../bin/spellingCorrectionTrajectory/')
		self.__phraseCleaner = PhraseCleaner()
		self.__MAX_CARDINALITY_SET = 7
		self.__MAX_DISTANCE = 5


	def writeInFile(self, path, file_name, text):
		textFile = open(path + file_name + ".txt", "a")  # append mode
		textFile.write(text)
		textFile.close()

	def initDicts(self):
		generalCountsFind = {} 
		generalCountsTra = {} 
		generalCountsSym = {} 
		generalCountsUnion = {} 

		for deleteLettersRate in np.arange(0.0,1.1,0.1):
			deleteLettersRate = round(deleteLettersRate,1)
			for randomLettersRate in np.arange(0.0,1.1,0.1):
				randomLettersRate = round(randomLettersRate,1)
				for maxRandoms in range(1,8):
					generalCountsSym['{}_{}_{}'.format(deleteLettersRate, randomLettersRate, maxRandoms)] = 0
					for cardinality in range(1,self.__MAX_CARDINALITY_SET+1):
						generalCountsTra['{}_{}_{}_{}'.format(deleteLettersRate, randomLettersRate, maxRandoms, cardinality)] = 0
						generalCountsUnion['{}_{}_{}_{}'.format(deleteLettersRate, randomLettersRate, maxRandoms, cardinality)] = 0

		return generalCountsFind, generalCountsTra, generalCountsSym, generalCountsUnion
	
	def loadTargets(self, path):
		textFile = open(path + "cleanWords.txt","r")
		cleanWords = []
		for word in textFile.readlines():
			cleanWords.append(word)
		textFile.close()

		return cleanWords

	def getResults(self, wordsSet, target, count, deleteLettersRate,randomLettersRate, maxRandoms,useCardinality=True):
		#Trajectory
		result = False
		cardinality = 0
		for indexList, possibleWord in enumerate(wordsSet): #Iterate elements of the set found
			if target == possibleWord[1]:
				result = True
				cardinality = indexList+1
				if useCardinality:
					for i in range(indexList+1, self.__MAX_CARDINALITY_SET+1):
						count['{}_{}_{}_{}'.format(deleteLettersRate,randomLettersRate, maxRandoms,i)] += 1
				else:
					count['{}_{}_{}'.format(deleteLettersRate, randomLettersRate, maxRandoms)] += 1

				break
		return result, cardinality

	def runTest(self, startLoop1, endLoop1, startLoop2, endLoop2, path2save='noiseTextWordsResult/', path='noiseTextWords/'):
		#Load targets
		cleanWords = self.loadTargets(path)
		generalCountsFind, generalCountsTra, generalCountsSym, generalCountsUnion = self.initDicts()

		for deleteLettersRate in np.arange(startLoop1, endLoop1, 0.1):
			deleteLettersRate = round(deleteLettersRate,1)
			for randomLettersRate in np.arange(startLoop2, endLoop2, 0.1): #Iterate every letter rates
				randomLettersRate = round(randomLettersRate, 1)
				for maxRandoms in range(1, 8): #Iterate every letter randoms
					textFile = open(path + "noiseWords{}_{}_{}.txt".format(deleteLettersRate, randomLettersRate, maxRandoms),"r")
					print('Testing FindCorrectWordsSet {}_{}_{}'.format(deleteLettersRate, randomLettersRate, maxRandoms))
					count = 0

					dfTraAlg = pd.DataFrame(columns=['Noise word', 'Result', 'Cardinality'])
					dfSymAlg = pd.DataFrame(columns=['Noise word', 'Result', 'Cardinality'])
					dfUnion = pd.DataFrame(columns=['Noise word', 'Result', 'Cardinality'])

					for indexWord, word in enumerate(textFile.readlines()): #Iterate every noise word in the file loaded
						target = cleanWords[indexWord].strip()
						wordsSet1 = self.__st.findCorrectWord(word, self.__MAX_CARDINALITY_SET, pathTablesFiles='../../bin/spellingCorrectionTrajectory/tableWords/')
						result, cardinality = self.getResults(wordsSet1, target, generalCountsTra, deleteLettersRate,randomLettersRate, maxRandoms)
						dfTraAlg.loc[len(dfTraAlg), dfTraAlg.columns] = word, result, cardinality

						#SymSpell algorithm
						wordsSet2 = self.__phraseCleaner.symSpell(word)
						result, cardinality = self.getResults(wordsSet2, target, generalCountsSym, deleteLettersRate,randomLettersRate, maxRandoms, useCardinality=False)
						dfSymAlg.loc[len(dfSymAlg), dfSymAlg.columns] = word, result, cardinality


						count += 1
						if count % 4000 == 0:
							print('Progreso: {} de {}===={:.2f}%'.format(count, len(cleanWords), count/len(cleanWords)*100))
							print('Accuracy temporal:')
							for cardinality in range(1,self.__MAX_CARDINALITY_SET+1):
								tmpCount = generalCountsTra['{}_{}_{}_{}'.format(deleteLettersRate, randomLettersRate, maxRandoms,cardinality)]
								print('Accuracy {}_{}_{}_{}={:.2f}%'.format(deleteLettersRate, randomLettersRate, maxRandoms,cardinality,tmpCount/count*100))

							print('Progreso: {} de {}===={:.2f}%, Accuracy temporal;'.format(count, len(cleanWords), count/len(cleanWords)*100))
							break
					textFile.close()

					#Write in files
					dfTraAlg.to_csv(path2save+'restultTraAlg{}_{}.csv'.format(deleteLettersRate, randomLettersRate, maxRandoms), index=False)
					dfSymAlg.to_csv(path2save+'restultSymAlg{}_{}.csv'.format(deleteLettersRate, randomLettersRate, maxRandoms), index=False)
					dfUnion.to_csv(path2save+'restultUnion{}_{}.csv'.format(deleteLettersRate, randomLettersRate, maxRandoms), index=False)

					break
					tmpCount = generalCountsSym['{}_{}_{}'.format(deleteLettersRate, randomLettersRate, maxRandoms)]
					tmp = 'Accuracy {}_{}_{}={}\n'.format(deleteLettersRate, randomLettersRate, maxRandoms,tmpCount)
					self.writeInFile(path2save, "accuracySym{}_{}_{}".format(deleteLettersRate, randomLettersRate, maxRandoms), tmp)
					for cardinality in range(1,self.__MAX_CARDINALITY_SET+1):
						tmpCount = generalCountsTra['{}_{}_{}_{}'.format(deleteLettersRate, randomLettersRate, maxRandoms,cardinality)]
						tmp = 'Accuracy {}_{}_{}_{}={}\n'.format(deleteLettersRate, randomLettersRate, maxRandoms,cardinality,tmpCount)
						self.writeInFile(path2save, "accuracyFindAlg{}_{}_{}_{}".format(deleteLettersRate, randomLettersRate, maxRandoms,cardinality), tmp)
						print('Count {}_{}_{}_{}={}'.format(deleteLettersRate, randomLettersRate, maxRandoms,cardinality,tmpCount))
						print('Accuracy {}_{}_{}_{}={:.2f}%'.format(deleteLettersRate, randomLettersRate, maxRandoms,cardinality,tmpCount/len(cleanWords)*100))


						tmpCount = generalCountsUnion['{}_{}_{}_{}'.format(deleteLettersRate, randomLettersRate, maxRandoms,cardinality)]
						tmp = 'Accuracy {}_{}_{}_{}={}\n'.format(deleteLettersRate, randomLettersRate, maxRandoms,cardinality,tmpCount)
						self.writeInFile(path2save, "accuracyUnion{}_{}_{}_{}".format(deleteLettersRate, randomLettersRate, maxRandoms,cardinality), tmp)

						# print('Accuracy {}_{}_{}={}'.format(randomLettersRate, maxRandoms,cardinality,tmpCount/len(count)))

						break
					break
				break
			break

path2save = sys.argv[1]
path = sys.argv[2]
startLoop1 = float(sys.argv[3])
endLoop1 = float(sys.argv[4])
startLoop2 = float(sys.argv[5])
endLoop2 = float(sys.argv[6])

test = SpellingCorrectionTrajectoryTest()
test.runTest(startLoop1=startLoop1, endLoop1=endLoop1, startLoop2=startLoop2, endLoop2=endLoop2, path2save=path2save, path=path)
