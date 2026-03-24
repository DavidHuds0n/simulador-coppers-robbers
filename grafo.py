import math

class GrafoIlha:
    def __init__(self):
        self.num_vertices = 0
        self.num_arestas = 0
        self.local_roubo = None
        self.saidas = []
        self.posicoes_policia = []
        
        # O Grafo original (lista de adjacência) para consultas rápidas de vizinhos
        self.adjacencias = {}
        
        # Matrizes do Floyd-Warshall
        self.dist = {}
        self.prox = {}

    def carregar_mapa(self, caminho_arquivo):
        """Lê o arquivo de texto e monta a estrutura inicial do grafo."""
        with open(caminho_arquivo, 'r') as f:
            linhas = [linha.strip() for linha in f if linha.strip()]
        
        lendo_conexoes = False
        for linha in linhas:
            if lendo_conexoes:
                u, v, peso = map(int, linha.split())
                self._adicionar_aresta(u, v, peso)
                continue
                
            chave, valor = linha.split(":")
            valor = valor.strip()
            
            if chave == "VERTICES": self.num_vertices = int(valor)
            elif chave == "ARESTAS": self.num_arestas = int(valor)
            elif chave == "ROUBO": self.local_roubo = int(valor)
            elif chave == "SAIDAS": self.saidas = list(map(int, valor.split()))
            elif chave == "POSICOES_POLICIA": self.posicoes_policia = list(map(int, valor.split()))
            elif chave == "CONEXOES": lendo_conexoes = True

    def _adicionar_aresta(self, u, v, peso):
        if u not in self.adjacencias: self.adjacencias[u] = {}
        if v not in self.adjacencias: self.adjacencias[v] = {}
        self.adjacencias[u][v] = peso

    def executar_floyd_warshall(self):
        """
        Calcula o caminho mínimo entre todos os pares de vértices.
        Complexidade: O(V^3). Perfeito para rodar uma única vez no pré-processamento.
        """
        vertices = list(self.adjacencias.keys())
        
        # Inicialização das matrizes
        for i in vertices:
            self.dist[i] = {}
            self.prox[i] = {}
            for j in vertices:
                self.dist[i][j] = math.inf
                self.prox[i][j] = None
            
            self.dist[i][i] = 0
            
            # Preenche com as arestas diretas existentes
            for vizinho, peso in self.adjacencias[i].items():
                self.dist[i][vizinho] = peso
                self.prox[i][vizinho] = vizinho

        # O coração do algoritmo: testa se passar por 'k' encurta o caminho de 'i' a 'j'
        for k in vertices:
            for i in vertices:
                for j in vertices:
                    if self.dist[i][k] + self.dist[k][j] < self.dist[i][j]:
                        self.dist[i][j] = self.dist[i][k] + self.dist[k][j]
                        self.prox[i][j] = self.prox[i][k] # Salva o próximo passo

    def pegar_proximo_passo(self, origem, destino):
        """Consulta O(1) para descobrir para onde andar."""
        return self.prox[origem][destino]