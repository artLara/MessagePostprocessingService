import numpy as np
import pickle as pkl
import bisect
import heapq
from fractions import Fraction
from spellchecker import SpellChecker
import time
from Utils import Utils




class SpellingCorrectionTrajectory():
    def __init__(self,coordenatesOrd=None, sizeTable=20, pathFiles='../bin/spellingCorrectionTrajectory/'):
        self.__spell = SpellChecker(language='es')
        self.__vocabByLen = self.__loadVocabulary()
        self.__sizeTable = sizeTable
        self.__confidenceIoU = 0.5
        if coordenatesOrd == None:
            #Load from file
            with open(pathFiles + 'coordenatesOrd.pkl', 'rb') as handle:
                coordenatesOrd = pkl.load(handle)

        self.__coordenatesOrd = coordenatesOrd
        self.__MAX_LEN_WORD = 22
        self.__MIN_LEN_WORD = 1

    def __loadVocabulary(self):
        vocabByLen = []
        for i in range(100):
            vocabByLen.append([])

        self.__maxFrecuency = 0
        for word in self.__spell:
            vocabByLen[len(word)].append(word)
            if self.__spell[word] > self.__maxFrecuency:
               self.__maxFrecuency = self.__spell[word]

        return vocabByLen

    def loadTables(self, number, path='../bin/spellingCorrectionTrajectory/tableWords/'):
        with open(path + 'tables'+str(number)+'.pkl', 'rb') as handle:
            table = pkl.load(handle)
        return table

    def findCorrectWord(self, word2clean, distance=2, maxOptWords=5, pathTablesFiles='../bin/spellingCorrectionTrajectory/tableWords/'):
        # Make table of noise words
        noiseTable= self.makeTableTrajectories(word2clean)
        # Compare with tables in range and return the best words in range of macOptWords
        ##Make a list, compare with the worst element and put in list in case of get a better IoU
        startInterval = max(self.__MIN_LEN_WORD, min(self.__MAX_LEN_WORD, len(word2clean)-distance))
        endInterval = min(self.__MAX_LEN_WORD, len(word2clean)+distance) + 1
        validWords = [(0, '-') for _ in range(maxOptWords)]
        minIoU = 0
        heapq.heapify(validWords)
        for index in range(startInterval, endInterval):#iterate vocabulary by len from the longest to smallest
            tables = self.loadTables(index, pathTablesFiles)
            for validWord in self.__vocabByLen[index]:
                wordTable = tables[validWord]
                iou = self.calculateIoU(noiseTable, wordTable)
                if minIoU < iou:
                    metric = Utils.metricEditDistanceModify(validWord, word2clean, self.__spell[validWord]/self.__maxFrecuency, 0.3)
                    # heapq.heappush(validWords, (iou, validWord))
                    heapq.heappush(validWords, (metric, validWord))
                    minIoU = heapq.heappop(validWords)[0]

        return sorted(list(validWords), key= lambda x: x[0] , reverse=True)[:maxOptWords]

    def calculateIoU(self, table1, table2):
        intersection = np.logical_and(table1, table2).sum()
        union = np.logical_or(table1, table2).sum()
        return intersection/union

    def compareWords(self, word1, word2):
        table1 = self.makeTableTrajectories(word1)
        table2 = self.makeTableTrajectories(word2)
        iou = self.calculateIoU(table1, table2)
        print('IoU=',iou)
        return iou

    def __linealFunction(self, m, p, x):
        return int(m*x - m*p[0] + p[1])

    def __calculateM(self, p1, p2):
        try:
            m = Fraction(p1[1]-p2[1]) / Fraction(p1[0]-p2[0])
        except:
            # print('Problems with :')
            # print('C1:', c1)
            # print('C2:', c2)
            m = Fraction(0)

        return m

    def calculateTrajectory(self, c1, c2):
        p1 = None
        p2 = None
        reverse = False
        if c1[0] < c2[0]:
            p1 = c1
            p2 = c2
        elif c1[0] > c2[0]:
            p1 = c2
            p2 = c1
        else:
            reverse = True
            if c1[1] < c2[1]:
                p1 = c1
                p2 = c2
            else:
                p1 = c2
                p2 = c1

        m = self.__calculateM(p1, p2)

        trajectory = []
        for x in range(p1[0], max(p2[0], p2[1])+1):
            y = self.__linealFunction(m, p1, x)
            if reverse:
                trajectory.append((y, x))
            else:
                trajectory.append((x, y))
            # if x == p2[0] or y == p2[1]:
            if (x, y) == p2:
                break

        return trajectory

    def drawTrayectory(self, table, coordenates, start, end, verbose=False):
        trajectory = self.calculateTrajectory(coordenates[start], coordenates[end])
        if verbose:
            print('Trajectory:',start,'->', end)
            print(trajectory)
        for i,j in trajectory:
            try:
                table[i][j] = start
            except:
                print('Problems with :')
                print('Trajectory:',start,'->', end)
                print(trajectory)
                print('start:', start)
                print('end:', end)
                break

    def makeTableTrajectories(self, word, verbose=False, pathTablesFiles='../bin/spellingCorrectionTrajectory/tableWords/'):
        table = [[0 for _ in range(self.__sizeTable)] for _ in range(self.__sizeTable)]
        tokens = self.tokenizer(word.lower().rstrip())
        # print(tokens)
        if len(tokens) ==  1:
            p = self.__coordenatesOrd[tokens[0]]
            table[p[0]][p[1]] = tokens[0]

        index = 0
        while(index < len(tokens)-1):
            self.drawTrayectory(table, self.__coordenatesOrd, tokens[index], tokens[index+1], verbose)
            index += 1

        return np.asarray(table)

    def replaceAccents(self, c):
        if c == 'á':
            c = 'a'

        if c == 'é':
            c = 'e'

        if c == 'í':
            c = 'i'

        if c == 'ó':
            c = 'o'

        if c == 'ú':
            c = 'u'

        if c == 'ü':
            c = 'u'

        return c

    def tokenizer(self, word):
        tokens = []
        index = 0
        while index < len(word):
            if index < len(word)-1 and word[index] == word[index+1]:
                tmp = ord(self.replaceAccents(word[index])) + ord(self.replaceAccents(word[index]))
                tokens.append(tmp)
                index += 2
                continue
            tmp = ord(self.replaceAccents(word[index]))
            tokens.append(self.replaceAccents(tmp))
            index += 1

        return tokens

    def printTable(self, table):
        for i in range(len(table)):
            for j in range(len(table)):
                print('{}\t'.format(table[i][j]), end=' ')
            print('')

# st = SpellingCorrectionTrajectory()
# # # # st.printTable(st.makeTableTrajectories('perro'))
# # # # st.printTable(st.makeTableTrajectories('cerro'))
# start = time.time()
# pw = st.findCorrectWord('hue')
# end = time.time()
# print(pw)
# print(end - start)
# st.compareWords('hue', 'que')
# st.compareWords('que', 'hue')
