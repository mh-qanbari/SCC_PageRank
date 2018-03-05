import numpy as np
from IndexMap import IndexMap
from PageRank import PageRank
from StronglyConnectedComponent import SCC

nan = float("nan")

if __name__ == '__main__':
    N = 7115
    E = 103689
    A_t = np.zeros((N, N), dtype=np.float)
    A = np.zeros((N, N), dtype=np.float)
    index_map = IndexMap()

    print "Loading ",
    with open("Wiki-Vote.txt", mode='r') as data_file:
        for line in data_file:
            if line[0] == '#':
                continue
            line = line.replace('\n', '')
            ij_list = line.split('\t')
            i = index_map.getIndex(int(ij_list[0]))
            j = index_map.getIndex(int(ij_list[1]))
            A_t[j, i] = 1
            A[i, j] = 1
    print "is finished."

    print " [1] : SCC .............................................. "
    scc = SCC(A)
    A_temp = scc.removeDeadEnds()
    print "> PageRank started..."
    pr = PageRank(beta=0.8, max_err=0.0001)
    pr.initTransposedMat(A_temp.transpose())
    pr.normalize()
    iter_count = pr.run()
    print "PageRank finished."
    print "> Propagate scores of PageRank"
    v = scc.computeRanks(pr.v)
    indexes = np.array(v).argsort()[-10:][::-1]
    print "Best nodes:"
    for index in indexes:
        print '\t', index_map.nodes[index], '\t', v[index]
    print " [1]; ................................................... "
    # print ""
