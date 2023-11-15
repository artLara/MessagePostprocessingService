from .SimilarWords import SimilarWords
from .Utils import Utils
import pickle
import os
class WordsSelector():
    def __init__(self, pathOfObjectDirectory='../bin/similarWords/'):
        if Utils.checkRamSize():
            self.__offset = 100000
            self.__sw = SimilarWords()
            self.__V = None
            self.__INF = 9999
            self.__graph = []
            self.__maxFrec = None
            self.__dictFrec = None

            if not os.path.isfile(pathOfObjectDirectory+'graphContext/dictFec.pkl') or \
            not os.path.isfile(pathOfObjectDirectory+'graphContext/maxFrec.pkl'):
                print('Error: graph context files not found!')

            else:
                with open(pathOfObjectDirectory+'graphContext/dictFec.pkl', 'rb') as inp:
                    self.__maxFrec = pickle.load(inp)

                with open(pathOfObjectDirectory+'graphContext/maxFrec.pkl', 'rb') as inp:
                    self.__dictFrec = pickle.load(inp)

    def getPhrase(self, wordsSet, selector='max'):
        if not Utils.checkRamSize():
            return self.maxSelect(wordsSet)
            
        if selector == 'max':
            return self.maxSelect(wordsSet)

        if selector == 'contextGraph':
            return self.contextGraph(wordsSet)

        print(selector, 'does not an option, try with max or contextGraph')

    def maxSelect(self, wordsSet):
        res = []
        for word in wordsSet:
            res.append(word[0][1])

        return res

    def __getProb(self, w1, w2):
        try:
            return self.__dictFrec[(w1,w2)]*self.__offsetoffset/self.__maxFrec[1]
        except:
            return 1*self.__offsetoffset/self.__maxFrec[1]

    def __getMI(self, w1, w2):
        # return 1
        try:
            # return self.__dictFrec[(w1,w2)]*self.__offsetoffset/maxFrec[1]
            return self.__sw.mutualInformation.similitud(w1,w2)
        except:
            return 1/self.__sw.mutualInformation.N

    def __initialise(self, dis, Next):
        for i in range(self.__V):
            for j in range(self.__V):
                dis[i][j] = self.__graph[i][j]

                # No edge between node
                # i and j
                if (self.__graph[i][j] == self.__INF):
                    Next[i][j] = -1
                else:
                    Next[i][j] = j

        return dis, Next

    def __constructPath(self, u, v, dis, Next):
        # global dis, Next

        # If there's no path between
        # node u and v, simply return
        # an empty array
        if (Next[u][v] == -1):
            return {}

        # Storing the path in a vector
        path = [u]
        values = []
        while (u != v):
            oldu = u
            u = Next[u][v]
            path.append(u)
            values.append(dis[oldu][u])

        return path, values

    def __floydWarshall(self, V, dis, Next):
        # Standard Floyd Warshall Algorithm
        # with little modification Now if we find
        # that dis[i][j] > dis[i][k] + dis[k][j]
        # then we modify next[i][j] = next[i][k]

        maxOptWords = 5
        # global dist, Next
        for k in range(V):
            for i in range(V):
                # for j in range(V):
                for j in range((i//maxOptWords+1) * maxOptWords, V, 1):
                    # We cannot travel through
                    # edge that doesn't exist
                    if (dis[i][k] == self.__INF or dis[k][j] == self.__INF):
                        continue
                    if (dis[i][j] > dis[i][k] + dis[k][j]):
                        dis[i][j] = dis[i][k] + dis[k][j]
                        Next[i][j] = Next[i][k]
        return dis, Next

    def printPath(self, path):
        n = len(path)
        if n==0:
            print('Not path')
            return
        for i in range(n - 1):
            print(path[i], end=" -> ")
        print(path[n - 1])

    def printGraph(self, graph):
        for row in graph:
            for column in row:
                print('{:.2f} '.format(column), end='')
            print('')

    def printSolution(self, dist):
        print("Following matrix shows the shortest distances between every pair of vertices")
        for i in range(self.__V):
            for j in range(self.__V):
                if(dist[i][j] == self.__INF):
                    print("%9s\t" % ("INF"), end=" ")
                else:
                    print("%.9f\t" % (dist[i][j]), end=' ')
                if j == self.__V-1:
                    print()

    def contextGraph(self, words):
        # print('Len(words)', len(words))
        self.__graph = []
        tam = len(words) * len(words[0])
        self.__V = tam
        for i in range(tam):
            tmp = []
            for j in range(tam):
                if i==j:
                    tmp.append(0)
                else:
                    tmp.append(self.__INF)
            self.__graph.append(tmp)

        # self.printGraph(self.__graph)
        """
        Fill all the node conexions with MI values
        """
        sizeOptWords = len(words[0])
        sw = 0
        for stride in range(sizeOptWords,tam,sizeOptWords):
            for i in range(sizeOptWords):
                for j in range(sizeOptWords): #len(words)=6
                    #Metric with probality
                    # self.__graph[i+stride-tam][j+stride] = (words[sw][i][1] + words[sw+1][j][1]) * -getProb(words[sw][i][0],words[sw+1][j][0])

                    # #Just MI
                    # if sw+1 >= len(words):
                    #     continue

                    self.__graph[i+stride-sizeOptWords][j+stride] = -self.__getMI(words[sw][i][0],words[sw+1][j][0])
                    # print('prob:(',words[sw][i][0],',',words[sw+1][j][0],')')
                    # self.__graph[i+stride-tam][j+stride] = -getProb(words[sw][i][0],words[sw+1][j][0])
            sw += 1
        # self.printGraph(self.__graph)
        # print('-----------------------------------')

        MAXM,self.__INF = 1000,self.__INF
        dis = [[-1 for i in range(MAXM)] for i in range(MAXM)]
        Next = [[-1 for i in range(MAXM)] for i in range(MAXM)]

        # Function to initialise the
        # distance and Next array
        dis, Next = self.__initialise(dis, Next)

        # Calling Floyd Warshall Algorithm,
        # this will update the shortest
        # distance as well as Next array
        dis, Next = self.__floydWarshall(self.__V, dis, Next)
        path = []
        shortes = self.__INF
        start = -1
        end = -1
        for i in range(sizeOptWords):
            for j in range(sizeOptWords):
                if shortes > dis[i][j + tam - sizeOptWords]:
                    shortes = dis[i][j + tam - sizeOptWords]
                    start = i
                    end = j + tam - sizeOptWords

        # print('-------------')
        # self.printSolution(self.__graph)
        # self.printSolution(dis)
        path, values = self.__constructPath(start, end, dis, Next)
        # self.printPath(path)
        # self.printGraph(self.__graph)

        # print('path=',path)
        res = []
        for i,j in enumerate(path):
            # print(words[i][j-(tam*i)][0], end='->')
            res.append(words[i][j-(sizeOptWords*i)][1])
        # print('')
        # print('value:', dis[start][end])
        # print(res)
        return res
