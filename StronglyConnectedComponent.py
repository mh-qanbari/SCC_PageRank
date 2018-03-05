import numpy as np
# from IndexMap import IndexMap


class SCC:
    def __init__(self, A):
        """ Strongly Connected Component.
        :param A: Adjacency matrix of the graph.
        :type A: np.ndarray
        """
        self.__A = A
        self.__states = []
        self.__removedIndexes = set([])

    # def run(self, A):
    #     """ Removes the non-leaving nodes from graph specified by adjacency matrix A.
    #     :param A: Adjacency matrix of the graph.
    #     :type A: numpy.ndarray
    #     :return: A matrix with no non-leaving nodes.
    #     :rtype: numpy.ndarray
    #     """
    #     __A = self.removeOneLevelDeadEnds(A)

    def removeDeadEnds(self):
        """ Recursively, removes the nodes with no non-leaving edge from the graph.
        :return: An adjacency matrix of the graph with no nodes contains non-leaving edges.
        :rtype: np.ndarray
        """
        __A = np.copy(self.__A)

        # [OLD] : Old version
        # while True:
        #     __removed_indexes = SCC.removeOneLevelDeadEnds(__A)
        #     if __removed_indexes.size == 0:
        #         break
        #     else:
        #         self.__states.append(__removed_indexes)
        # [NEW] : New version ...................................
        i = 0
        while True:
            __s = np.sum(self.__A, 0)
            __indexes = np.where(__s == 0)[0]
            __state = set(list(__indexes)) - self.__removedIndexes
            if len(__state) == 0:
                break
            self.__states.append(__state)
            self.__removedIndexes = self.__removedIndexes.union(set(__indexes))
            __A = np.delete(__A, list(__state), 1)
            i += 1
        print "iteration =", i
        # .......................................................
        __A = np.delete(__A, list(self.__removedIndexes), 0)
        return __A

    @staticmethod
    def removeOneLevelDeadEnds(A):
        """ Removes the nodes with wiht no non-leaving edge from the graph specified by adjacency matrix A.
        :param [OUT] A: Adjacency matrix of the graph.
        :type A: np.ndarray
        :return: Removed indexes list of the adjacency matrix A.
        :rtype: np.ndarray
        """
        __s = np.sum(A, 0)
        __indexes = np.where(__s == 0)
        np.delete(A, __indexes, 0)
        np.delete(A, __indexes, 1)
        return __indexes

    def computeRanks(self, v):
        """ After calling removeOneLevelDeadEnds and computing  the scores of any node, this method can be called.
        This method propagates the scores to rank any deadends.
        :param v: Scores of each nodes of removeOneLevelDeadEnds method output matrix.
        :type v: np.ndarray
        :rtype: np.ndarray
        """
        __v = self.__scaleV(v)
        i = len(self.__states) - 1
        while i >= 0:
            __stage = self.__states[i]
            for index in __stage:
                # Find Parents ...
                __parent_indexes = np.where(self.__A[:, index] != 0)[0]
                if __parent_indexes.size != 0:
                    # Get Scores ...
                    __parent_scores = __v[__parent_indexes]
                    # Get Degrees ...
                    __parent_degrees = np.zeros(__parent_indexes.size)
                    for i in range(__parent_degrees.size):
                        __parent_index = __parent_indexes[i]
                        __parent_degrees[i] = sum(self.__A[__parent_index, :])
                    __v[index] = sum(__parent_scores / __parent_degrees)
            i -= 1
        return __v

    def __scaleV(self, v):
        """ Scale scores vector to real size.
        :param v: is a scores vector of simplified graph.
        :type v: np.ndarray
        :return: scaled scores vector.
        :rtype: np.ndarray
        """
        # __n = self.__A.shape[0]
        # __v = np.zeros(__n)
        # # __sorted_indexes = list(self.__removedIndexes)
        # for i in range(__n):
        #     if i not in self.__removedIndexes:
        #         __v[i] = __v
        __v = list(np.copy(v))
        for __index in self.__removedIndexes:
            __v.insert(__index, 0)
        return __v
