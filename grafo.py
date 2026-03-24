import math

# ==========================================================================
# --- ESTRUTURA DE DADOS PARA A ILHA (GRAFO PONDERADO) ---
# Esta classe gerencia a representação da ilha e o pré-processamento de rotas.
# ==========================================================================

class GrafoIlha:
    def __init__(self):
        """
        Inicializa as estruturas base do grafo.
        Utiliza listas de adjacência para o grafo e matrizes para o Floyd-Warshall.
        """
        self.num_vertices = 0
        self.num_arestas = 0
        self.local_roubo = None
        self.saidas = []
        self.posicoes_policia = []
        
        # Grafo original para consultas rápidas de vizinhança direta
        self.adjacencias = {}
        
        # Matrizes de distância e próximos passos (Roteamento)
        self.dist = {}
        self.prox = {}

    def carregar_mapa(self, caminho_arquivo):
        """
        Realiza o parse do arquivo de configuração .txt.
        Estrutura esperada: Cabeçalhos com parâmetros seguidos pela lista de arestas.
        """
        try:
            with open(caminho_arquivo, 'r') as f:
                linhas = [linha.strip() for linha in f if linha.strip()]
        except FileNotFoundError:
            print(f"[ERRO] Arquivo {caminho_arquivo} não encontrado.")
            return

        lendo_conexoes = False
        for linha in linhas:
            if lendo_conexoes:
                u, v, peso = map(int, linha.split())
                self._adicionar_aresta(u, v, peso)
                continue
                
            chave, valor = linha.split(":")
            valor = valor.strip()
            
            # Mapeamento dos parâmetros globais da simulação
            if chave == "VERTICES": self.num_vertices = int(valor)
            elif chave == "ARESTAS": self.num_arestas = int(valor)
            elif chave == "ROUBO": self.local_roubo = int(valor)
            elif chave == "SAIDAS": self.saidas = list(map(int, valor.split()))
            elif chave == "POSICOES_POLICIA": self.posicoes_policia = list(map(int, valor.split()))
            elif chave == "CONEXOES": lendo_conexoes = True

    def _adicionar_aresta(self, u, v, peso):
        """Helper interno para popular a lista de adjacências."""
        if u not in self.adjacencias: self.adjacencias[u] = {}
        if v not in self.adjacencias: self.adjacencias[v] = {}
        self.adjacencias[u][v] = peso

    # --------------------------------------------------------------------------
    # ALGORITMO DE FLOYD-WARSHALL
    # --------------------------------------------------------------------------
    def executar_floyd_warshall(self):
        """
        Calcula o caminho mínimo entre todos os pares de vértices (All-Pairs Shortest Path).
        
        * Por que Floyd-Warshall? Como o projeto possui pesos negativos (descidas), 
          precisamos de um algoritmo que lide com isso sem entrar em loops infinitos 
          (garantido que não há ciclos negativos pela regra do professor).
        * Performance: O(V³). Ideal para rodar uma única vez antes da simulação.
        """
        vertices = list(range(1, self.num_vertices + 1))
        
        # Inicialização: Distância 0 para si mesmo e INF para os demais
        for i in vertices:
            self.dist[i] = {j: math.inf for j in vertices}
            self.prox[i] = {j: None for j in vertices}
            self.dist[i][i] = 0
            
            # Define as distâncias diretas das arestas existentes
            if i in self.adjacencias:
                for vizinho, peso in self.adjacencias[i].items():
                    self.dist[i][vizinho] = peso
                    self.prox[i][vizinho] = vizinho

        # Triplo loop dinâmico: Verifica se passar por 'k' encurta o caminho de 'i' a 'j'
        for k in vertices:
            for i in vertices:
                for j in vertices:
                    if self.dist[i][k] + self.dist[k][j] < self.dist[i][j]:
                        self.dist[i][j] = self.dist[i][k] + self.dist[k][j]
                        self.prox[i][j] = self.prox[i][k] # Salva o roteamento para reconstrução

    def pegar_proximo_passo(self, origem, destino):
        """Consulta a matriz de sucessores em O(1) para ditar o movimento."""
        if origem not in self.prox or destino not in self.prox[origem]:
            return None
        return self.prox[origem][destino]