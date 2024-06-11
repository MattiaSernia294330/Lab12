import networkx as nx

from database.DAO import DAO
class Model:
    def __init__(self):
        self._grafo=nx.Graph()
        self._dizionario_nodi={}
        self._dizionario_retailer={}
        self._bestSol=[]
        self._pesoBest=0
        pass

    def getAllCountry(self):
        return DAO.getAllCountry()
    def creaGrafo(self,anno,country):
        self._grafo.clear()
        nodi=DAO.getNodi(country)
        for nodo in nodi:
            self._dizionario_nodi[nodo.Retailer_code]=nodo
            self._grafo.add_node(nodo)
        print(self.numNodi())
        edges=DAO.GetConnessioni(anno,country)
        for arco in edges:
            if self._grafo.has_edge(self._dizionario_nodi[arco.r1],self._dizionario_nodi[arco.r2]):
                self._grafo[self._dizionario_nodi[arco.r1]][self._dizionario_nodi[arco.r2]]['weight']+=1
            else:
                self._grafo.add_edge(self._dizionario_nodi[arco.r1],self._dizionario_nodi[arco.r2], weight=1)
    def numNodi(self):
        return len(self._grafo.nodes())
    def numArchi(self):
        return len(self._grafo.edges())
    def calcolaVolume(self):
        self._dizionario_retailer = {}
        for nodo in self._grafo.nodes():
            peso=self.pesoIncidente(nodo)
            self._dizionario_retailer[nodo.Retailer_code] = peso
        dizionario=dict(sorted(self._dizionario_retailer.items(), key=lambda x:x[1], reverse=True))
        return dizionario



    def pesoIncidente(self,nodo):
        peso = 0
        for u, v, data in self._grafo.edges(data=True):
            if u == nodo or v == nodo:
                peso += data.get('weight', 0)  # Default weight is 1 if not specified
        return peso

    def ricorsione(self,parziale,n,nodo,pesoattuale):
        successori=list(self._grafo.neighbors(nodo))
        if len(parziale) == n:
            for element in successori.copy():
                if element in parziale[1:]:
                    successori.remove(element)
        else:
            for element in successori.copy():
                if element in parziale:
                    successori.remove(element)
        if len(parziale)==n+1:
            if pesoattuale>self._pesoBest and parziale[0]==parziale[-1]:
                self._bestSol=parziale
                self._pesoBest=pesoattuale
            return
        elif len(successori)==0:
            return
        else:
            for item in successori:
                nuovo_nodo = item
                parziale_nuovo = list(parziale)
                parziale_nuovo.append(nuovo_nodo)
                pesoattuale_nuovo=pesoattuale+self._grafo[nodo][item]['weight']
                self.ricorsione(parziale_nuovo,n,nuovo_nodo,pesoattuale_nuovo)

    def handleRicorsione(self,archi):
        self._pesoBest=0
        for nodes in self._grafo.nodes():
            self.ricorsione([nodes],archi,nodes,0)

    def getPercorso(self):
        lista=[]
        for i in range(len(self._bestSol)-1):
            peso=self._grafo[self._bestSol[i]][self._bestSol[i+1]]['weight']
            lista.append(f"{self._bestSol[i]} -->{self._bestSol[i+1]}: {peso}")
        return lista

    def getPeso(self):
        return self._pesoBest


