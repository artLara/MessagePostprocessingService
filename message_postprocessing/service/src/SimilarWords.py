import pickle
import os
from .MutualInformation import MutualInformation
class SimilarWords:
    def __init__(self, pathOfObjectDirectory='../../bin/similarWords/mutualInformation/'):
        self.vocabulary = set()
        self.prob = {}
        self.prob_join = {}
        self.N = 1 # Total of sentences

        if not os.path.isfile(pathOfObjectDirectory+'probability.pkl') or \
        not os.path.isfile(pathOfObjectDirectory+'probability_join.pkl')  or \
        not os.path.isfile(pathOfObjectDirectory+'N.pkl') :
            # self.initializeProbs(pathOfObjectDirectory)
            print('Error files not found!')

        else:
            with open(pathOfObjectDirectory+'probability.pkl', 'rb') as inp:
                self.prob = pickle.load(inp)

            with open(pathOfObjectDirectory+'probability_join.pkl', 'rb') as inp:
                self.prob_join = pickle.load(inp)

            with open(pathOfObjectDirectory+'N.pkl', 'rb') as inp:
                self.N = pickle.load(inp)

        # if not os.path.isfile(pathOfObjectDirectory+'mutualInformation.pkl'):
        self.mutualInformation = MutualInformation(self.prob, self.prob_join, self.N)
        # else:
        #     with open(pathOfObjectDirectory+'mutualInformation.pkl', 'rb') as inp:
        #         self.mutualInformation = pickle.load(inp)

    # def initializeProbs(self, pathOfObjectDirectory, processAllTexts=True, maxTexts=10, verbose=True):
    #     """Preprocess texts and returns a list of lists which contains a sentence"""
    #     file_names = [] #List of file names in the specific path
    #     path = '/content/rawWikis/'
    #     #Get all file names in the directory
    #     for (dirpath, dirnames, filenames) in walk(path):
    #         file_names.extend(filenames)
    #         break
    #
    #     # file_names = ['e960401_mod.htm']#Forzar a este solo archivo para experimentar
    #     analized = 0
    #     for index, file_name in enumerate(sorted(file_names)):
    #         try:
    #             #Read the document
    #             with open(path+file_name, encoding='utf-8') as f:
    #                 text = f.read() #Raw data in a huge string
    #             text = self.tp.process(text) #Preprocessing and split in sentences
    #             self.calculateProbabilities(text) #Calculate proabibilities
    #         except:
    #             print('Problem with {}'.format(file_name))
    #             continue
    #
    #         if verbose:
    #             analized += 1
    #             if analized%10 == 0:
    #                 print('{} de {}'.format(analized,len(file_names)))
    #         if not processAllTexts and index>=maxTexts:
    #             break
    #
    #     del file_names
    #
    #     with open(pathOfObjectDirectory+'probability.pkl', 'wb') as outp:
    #         pickle.dump(self.prob, outp, pickle.HIGHEST_PROTOCOL)
    #
    #     with open(pathOfObjectDirectory+'probability_join.pkl', 'wb') as outp:
    #         pickle.dump(self.prob_join, outp, pickle.HIGHEST_PROTOCOL)
    #
    #     with open(pathOfObjectDirectory+'N.pkl', 'wb') as outp:
    #         pickle.dump(self.N, outp, pickle.HIGHEST_PROTOCOL)
    #
    #     self.vocabulary = sorted(self.vocabulary)
    #     with open(pathOfObjectDirectory+'vocabulary.pkl', 'wb') as outp:
    #         pickle.dump(self.vocabulary, outp, pickle.HIGHEST_PROTOCOL)
    #
    #
    # def calculateProbabilities(self, sentences):
    #     # self.prob = {}
    #     # prob_join = {}
    #     self.N += len(sentences)#Total of sentences
    #     for sentence in sentences: #For each sentence
    #         sentence_set = list(set(sentence)) #Delete repetetive words
    #         for i,word in enumerate(sentence_set):
    #             self.vocabulary.add(word)#Add word to vocabulary set
    #             #Single probability
    #             try:
    #                 self.prob[word] += 1
    #             except:
    #                 self.prob[word] = 1
    #
    #             #Join probability
    #             #Make all necesary combinations of words
    #             for j in range(i+1, len(sentence_set)-1):
    #                 #Sorting words is useful for save in the same space
    #                 #p(a,b) and p(b,a) because they are equals in this case
    #                 words = sorted([sentence_set[i], sentence_set[j]])
    #                 try:
    #                     self.prob_join[(words[0], words[1])] += 1
    #                 except:
    #                     self.prob_join[(words[0], words[1])] = 1
