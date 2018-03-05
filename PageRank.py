import numpy as np


class PageRank:
    def __init__(self, beta, max_err):
        self.b = beta
        self.A_t = np.ndarray((0, 0))
        self.v = np.ndarray(0)
        self.maxError = max_err
        self.__tax = np.ndarray(0)

    def initTransposedMat(self, transposed_mat):
        del self.A_t
        self.A_t = transposed_mat.copy()
        del self.v
        __n = transposed_mat.shape[0]
        self.v = np.ones(__n)
        del self.__tax
        self.__tax = np.ones(__n) / __n

    def normalize(self):
        self.A_t = self.A_t / self.A_t.sum(axis=0)
        self.A_t[np.isnan(self.A_t)] = 0

    def run(self):
        __i = 0
        while True:
            __i += 1
            __v = self.A_t.dot(self.v) * self.b + self.__tax * (1.0 - self.b)
            if self.__getError(__v) < self.maxError:
                self.v = __v.copy()
                break
            self.v = __v.copy()
        del __v
        return __i

    def __getError(self, v):
        return sum(self.v - v)
