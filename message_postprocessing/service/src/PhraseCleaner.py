from spellchecker import SpellChecker
from .WordsSelector import WordsSelector
from .SpellingCorrectionTrajectory import SpellingCorrectionTrajectory
from symspellpy import SymSpell, Verbosity

class PhraseCleaner():
    def __init__(self, maxOptWords=5, pathSymEspDict='../bin/dictionaries/es-100l.txt'):
        self.__maxOptWords = maxOptWords
        self.__maxFrecuency = None
        self.__spell = SpellChecker(language='es')
        self.__vocabByLen = self.loadVocabulary()
        self.__wordsSelector = WordsSelector()
        self.__symSpell = SymSpell()
        pathSymEspDict = '/home/lara/Desktop/dactilologiaLSM_microservices/MessagePostprocessingService/message_postprocessing/service/bin/dictionaries/es-100l.txt'
        self.__symSpell.load_dictionary(pathSymEspDict, 0, 1)
        tajectoryTablesPath = '/home/lara/Desktop/dactilologiaLSM_microservices/MessagePostprocessingService/message_postprocessing/service/bin/spellingCorrectionTrajectory/'
        self.__st = SpellingCorrectionTrajectory(pathFiles=tajectoryTablesPath)

    def loadVocabulary(self):
        vocabByLen = []
        for i in range(100):
            vocabByLen.append([])

        self.__maxFrecuency = 0
        for word in self.__spell:
            vocabByLen[len(word)].append(word)
            if self.__spell[word] > self.__maxFrecuency:
               self.__maxFrecuency = self.__spell[word]

        return vocabByLen

    def findCorrectWord(self, word2clean, maxOptWords=None):
        if maxOptWords == None:
            maxOptWords = self.__maxOptWords

        validwords = []#Array of clean words
        maxNumWords = 0
        word2clean = word2clean.strip()
        for index in range(min(len(word2clean),len(self.__vocabByLen)), 0, -1):#iterate vocabulary by len from the longest to smallest
            for validWord in self.__vocabByLen[index]: #Iterate words with the same longitud
                indexValidWord = 0
                indexWord2Clean = 0
                while(len(validWord)-indexValidWord<=len(word2clean)-indexWord2Clean): #Check every letter by positition
                    if validWord[indexValidWord] == word2clean[indexWord2Clean]:
                        indexValidWord += 1
                        if indexValidWord == len(validWord):
                            if self.__spell[validWord] > maxNumWords:
                                maxNumWords=self.__spell[validWord]
                            metric = len(validWord)/len(word2clean) #+ self.__spell[validWord]/maxNumWords
                            # metric += self.__spell[validWord]/maxNumWords*0.3 #MOdificado aquiiiiiii
                            metric += self.__spell[validWord]/self.__maxFrecuency*0.3 #MOdificado aquiiiiiii

                            validwords.append((metric, validWord.strip()))
                            break
                    indexWord2Clean += 1

            if len(validwords) >= maxOptWords: #Modificar para un largo definido y mateices rectangulares
                break

        # return validwords
        # if len(validwords) < maxOptWords: #For return square matrices
        #     for _ in range(len(validwords),maxOptWords):
        #         validwords.append(('-', -1))

        return sorted(validwords, key= lambda x: x[0] , reverse=True)[:maxOptWords]
        # return max(validwords, key= lambda x: x[1] + self.__spell[x[0]]/maxNumWords*0.3)[0]

    def symSpell(self, word2clean, maxOptWords=None):
        if maxOptWords == None:
            maxOptWords = self.__maxOptWords

        validwords = []
        suggestions = self.__symSpell.lookup(word2clean, Verbosity.CLOSEST, max_edit_distance=2, include_unknown=False)

        for suggestion in suggestions:
            validWord = suggestion.term
            metric = len(validWord)/len(word2clean) #+ self.__spell[validWord]/maxNumWords
            metric += self.__spell[validWord]/self.__maxFrecuency*0.3 #MOdificado aquiiiiiii
            validwords.append((metric, validWord.strip()))

        return sorted(validwords, key= lambda x: x[0] , reverse=True)[:maxOptWords]


    def cleanSentence(self, phrase, selector='contextGraph', maxOptWords=None):
        if maxOptWords == None:
            maxOptWords = self.__maxOptWords

        words = []
        for word in phrase.split(' '):
            if word == ' ' or word == '':
                continue

            tmp = self.cleanRepetitiveLetters(word).strip()

            if tmp == ' ' or tmp == '':
                continue

            words.append(tmp)

        cleanWordsSet = []
        # print(words)
        # print('Word sets:')
        for word in words:
            set1 = set(self.findCorrectWord(word))
            # set2 = set(self.symSpell(word))
            set2 = set()
            validwords = list(set1.union(set2))
            for _ in range(len(validwords), self.__maxOptWords): #For square matrix
                validwords.append((-1, '-'))

            validwords = sorted(validwords, key= lambda x: x[0] , reverse=True)[:self.__maxOptWords]
            # print(tmp)
            cleanWordsSet.append(validwords)

        words = self.__wordsSelector.getPhrase(cleanWordsSet, selector)
        return ' '.join(words)
    
    def getWordsSet(self, phrase, maxOptWords=None):
        if maxOptWords == None:
            maxOptWords = self.__maxOptWords

        words = []
        for word in phrase.split(' '):
            if word == ' ' or word == '':
                continue

            tmp = self.cleanRepetitiveLetters(word).strip()

            if tmp == ' ' or tmp == '':
                continue

            words.append(tmp)

        cleanWordsSet = []
        # print(words)
        # print('Word sets:')
        union_set = set()
        set_alg1 = []
        set_algSys = []
        set_algTra = []

        wordsSetString1 = ''
        for word in words:
            tmp = self.findCorrectWord(word, maxOptWords=maxOptWords)
            set_alg1.append(tmp)
            for i in tmp:
                wordsSetString1 += i[1] + ' '
            wordsSetString1 += '-'

        wordsSetStringSys = ''
        for word in words:
            tmp = self.symSpell(word, maxOptWords=maxOptWords)
            set_algSys.append(tmp)
            for i in tmp:
                wordsSetStringSys += i[1] + ' '
            wordsSetStringSys += '-'

        wordsSetStringTra = ''
        tmpPath = '/home/lara/Desktop/dactilologiaLSM_microservices/MessagePostprocessingService/message_postprocessing/service/bin/spellingCorrectionTrajectory/tableWords/'
        for word in words:
            tmp = self.__st.findCorrectWord(word, pathTablesFiles=tmpPath, distance=4)
            set_algTra.append(tmp)
            for i in tmp:
                wordsSetStringTra += i[1] + ' '
            wordsSetStringTra += '-'

        unionString = ''
        for setIndex in range(len(set_alg1)):
            union_set = set()
            # print(set_alg1[setIndex])
            # print(set_algSys[setIndex])
            # print(set_algTra[setIndex])
            
            union_set = union_set.union(set_alg1[setIndex], set_algSys[setIndex], set_algTra[setIndex])
            # print(union_set)
            union_list = sorted(list(union_set), key= lambda x: x[0] , reverse=True)[:maxOptWords]
            for i in union_list:
                unionString += i[1] + ' '

            unionString += '-'

        return wordsSetString1, wordsSetStringSys, wordsSetStringTra, unionString

    def cleanRepetitiveLetters(self, word):
        curryLetter = word[0]
        cleanWord = curryLetter
        index = 0
        letter = word[index]

        while index < len(word)-1:
            index += 1
            letter = word[index]
            if index == 0:
                continue
            if curryLetter == letter:
                continue
            if letter == '/':
                index += 1
                cleanWord += word[index]
                cleanWord += word[index]
                curryLetter = word[index]
                index += 2
                continue

            curryLetter = letter
            cleanWord += curryLetter

        return cleanWord.lower()
