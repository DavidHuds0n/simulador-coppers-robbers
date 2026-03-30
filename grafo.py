import math

class GrafoIlha:
    """
    Estrutura de dados para a ilha (Grafo Ponderado).
    Gerencia a representacao da ilha e o pre-processamento de rotas.
    """
    def __init__(self):
        """
        Inicializa as estruturas base do grafo.
        Utiliza listas de adjacencia para o grafo e matrizes para o Floyd-Warshall.
        """
        self.num_vertices = 0
        self.num_arestas = 0
        self.local_roubo = None
        self.saidas = []
        self.posicoes_policia = []
        
        # Grafo original para consultas rapidas de vizinhanca direta
        self.adjacencias = {}
        
        # Matrizes de distancia e proximos passos (Roteamento)
        self.dist = {}
        self.prox = {}

    def carregar_mapa(self, caminho_arquivo):
        """
        Realiza o parse do arquivo de configuracao .txt.
        Estrutura esperada: Cabecalhos com parametros seguidos pela lista de arestas.
        """
        try:
            with open(caminho_arquivo, 'r') as f:
                linhas = [linha.strip() for linha in f if linha.strip()]
        except FileNotFoundError:
            print(f"[ERRO] Arquivo {caminho_arquivo} nao encontrado.")
            return

        lendo_conexoes = False
        for linha in linhas:
            if lendo_conexoes:
                u, v, peso = map(int, linha.split())
                self._adicionar_aresta(u, v, peso)
                continue
                
            chave, valor = linha.split(":")
            valor = valor.strip()
            
            # Mapeamento dos parametros globais da simulacao
            if chave == "VERTICES": 
                self.num_vertices = int(valor)
            elif chave == "ARESTAS": 
                self.num_arestas = int(valor)
            elif chave == "ROUBO": 
                self.local_roubo = int(valor)
            elif chave == "SAIDAS": 
                self.saidas = list(map(int, valor.split()))
            elif chave == "POSICOES_POLICIA": 
                self.posicoes_policia = list(map(int, valor.split()))
            elif chave == "CONEXOES": 
                lendo_conexoes = True

    def _adicionar_aresta(self, u, v, peso):
        """Helper interno para popular a lista de adjacencias."""
        if u not in self.adjacencias: 
            self.adjacencias[u] = {}
        if v not in self.adjacencias: 
            self.adjacencias[v] = {}
        self.adjacencias[u][v] = peso

    def executar_floyd_warshall(self):
        """
        Calcula o caminho minimo entre todos os pares de vertices (All-Pairs Shortest Path).
        
        Como o projeto possui pesos negativos (descidas), usamos um algoritmo que lide
        com isso sem loops infinitos. Performance: O(V^3).
        """
        vertices = list(range(1, self.num_vertices + 1))
        
        # Inicializacao: Distancia 0 para si mesmo e INF para os demais
        for i in vertices:
            self.dist[i] = {j: math.inf for j in vertices}
            self.prox[i] = {j: None for j in vertices}
            self.dist[i][i] = 0
            
            # Define as distancias diretas das arestas existentes
            if i in self.adjacencias:
                for vizinho, peso in self.adjacencias[i].items():
                    self.dist[i][vizinho] = peso
                    self.prox[i][vizinho] = vizinho

        # Triplo loop dinamico: Verifica se passar por 'k' encurta o caminho de 'i' a 'j'
        for k in vertices:
            for i in vertices:
                for j in vertices:
                    if self.dist[i][k] + self.dist[k][j] < self.dist[i][j]:
                        self.dist[i][j] = self.dist[i][k] + self.dist[k][j]
                        self.prox[i][j] = self.prox[i][k] # Salva o roteamento para reconstrucao

    def pegar_proximo_passo(self, origem, destino):
        """Consulta a matriz de sucessores em O(1) para ditar o movimento."""
        if origem not in self.prox or destino not in self.prox[origem]:
            return None
        return self.prox[origem][destino]