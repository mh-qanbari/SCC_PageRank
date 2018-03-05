class IndexMap:
    def __init__(self):
        self.nodes = []
        self.nodesSize = -1

    def getIndex(self, node_id):
        """ returns index of nodeId
        :param node_id: node id.
        :type node_id: int
        :return: index of nodeId
        :rtype: int
        """
        if node_id not in self.nodes:
            self.nodes.append(node_id)
            self.nodesSize += 1
            return self.nodesSize
        else:
            return self.nodes.index(node_id)
