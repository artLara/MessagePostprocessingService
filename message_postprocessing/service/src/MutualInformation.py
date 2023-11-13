class MutualInformation:
    def __init__(self, prob, prob_join, N):
        self.prob = prob
        self.prob_join = prob_join
        self.N = N

    def similitud(self, word1, word2):
        # w1_1 = self.prob[words[0]]
        # w2_1 = self.prob[words[1]]
        w1_1 = self.prob[word1]/self.N
        w2_1 = self.prob[word2]/self.N
        w1_0 = 1 - w1_1
        w2_0 = 1 - w2_1
        jp = {}
        tmp = sorted([word1, word2])
        words = (tmp[0], tmp[1])
        try:
            jp[(1,1)] = self.prob_join[words]/self.N
        except:
            #This ocurs when any sentence has that two words
            # jp[(1,1)] = sys.float_info.min * sys.float_info.epsilon
            jp[(1,1)] = 0.000001

        jp[(0,1)] = w2_1 - jp[(1,1)]
        jp[(1,0)] = w1_1 - jp[(1,1)]
        jp[(0,0)] = w1_0 - jp[(0,1)]
        i = jp[(0,0)] * np.log2(jp[(0,0)] / (w1_0 * w2_0))
        i += jp[(0,1)] * np.log2(jp[(0,1)] / (w1_0 * w2_1))
        i += jp[(1,0)] * np.log2(jp[(1,0)] / (w1_1 * w2_0))
        i += jp[(1,1)] * np.log2(jp[(1,1)] / (w1_1 * w2_1))
        if np.isnan(i):
            i = 0

        return i
