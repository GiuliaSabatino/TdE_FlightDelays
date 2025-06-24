import networkx as nx

from database.DAO import DAO

class Model:
    def __init__(self):
        self._graph = nx.Graph()
        self._airports = DAO.getAllAirports()
        self._idMapAirports = {}
        for a in self._airports:
            self._idMapAirports[a.ID] = a

    def buildGraph(self, nMin):
        nodes = DAO.getAllNodes(nMin, self._idMapAirports)
        self._graph.add_nodes_from(nodes)
        self.addAllArchi()
        print("num nodi: ", len(self._graph.nodes), "num archi: ", len(self._graph.edges))

    def addAllArchi(self):
        allEdges = DAO.getAllEdges(self._idMapAirports)
        for e in allEdges:
            if e.aeroportoP in self._graph and e.aeroportoA in self._graph: #perchè ho un filtro sui nodi
                # se l'arco esiste già, aggiungo anche i voli di ritorno:
                if self._graph.has_edge(e.aeroportoA, e.aeroportoP):
                    self._graph[e.aeroportoP][e.aeroportoA]["weight"] += e.peso
                else:
                    self._graph.add_edge(e.aeroportoP, e.aeroportoA, weight=e.peso)

    def getGraphDetails(self):
        return self._graph.number_of_nodes(), self._graph.number_of_edges()

    def getAllNodes(self):
        return self._graph.nodes

    def getSortedNeighbors(self, node):
        neighbors = self._graph.neighbors(node)
        # creo una lista di tuple, dove il primo elemento è il nodo mentre il secondo elemento
        # è il peso dell'arco tra il nodo source e il nodo vicino
        neighTuples = []
        for n in neighbors:
            neighTuples.append((n, self._graph[node][n]["weight"]))

        neighTuples.sort(key=lambda x: x[1], reverse=True) #ordino secondo il secondo elemento della tupla, ovvero il peso
        return neighTuples

    def getPath(self, v0, v1):
        path = nx.shortest_path(self._graph, v0, v1)
        return path