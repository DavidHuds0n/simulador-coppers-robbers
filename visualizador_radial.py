import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

# ==========================================================================
# --- VISUALIZADOR RADIAL DA ILHA ---
# Organiza o grafo em camadas concêntricas a partir do local do roubo.
# Ideal para visualizar a hierarquia de fuga e evitar confusão de arestas.
# ==========================================================================

def carregar_e_desenhar_radial(caminho_arquivo="mapa_exemplo.txt"):
    print("[INFO] Criando visualização radial (estilo radar)...")
    
    G = nx.DiGraph()
    local_roubo = None
    saidas = []
    policias = []

    # 1. Leitura do arquivo para capturar a estrutura e metadados
    try:
        with open(caminho_arquivo, 'r') as f:
            linhas = [l.strip() for l in f if l.strip()]
    except FileNotFoundError:
        print(f"[ERRO] Arquivo {caminho_arquivo} não encontrado.")
        return

    lendo_conexoes = False
    for linha in linhas:
        if lendo_conexoes:
            u, v, peso = map(int, linha.split())
            G.add_edge(u, v, weight=peso)
            continue
        
        chave, valor = linha.split(":")
        if "ROUBO" in chave: local_roubo = int(valor)
        elif "SAIDAS" in chave: saidas = list(map(int, valor.split()))
        elif "POSICOES_POLICIA" in chave: policias = list(map(int, valor.split()))
        elif "CONEXOES" in chave: lendo_conexoes = True

    # 2. Cálculo das camadas (Distância em saltos a partir do roubo)
    # nx.single_source_shortest_path_length retorna {nó: distância}
    distancias = nx.single_source_shortest_path_length(G, local_roubo)
    
    # 3. Mapeamento de Coordenadas Radiais
    pos = {}
    niveis = {}
    for node, d in distancias.items():
        if d not in niveis: niveis[d] = []
        niveis[d].append(node)

    for d, nos_no_nivel in niveis.items():
        raio = d * 3  # Aumenta o raio para cada nível de distância
        for i, node in enumerate(nos_no_nivel):
            # Divide o círculo (2 * PI) pelo número de nós no nível
            angulo = 2 * np.pi * i / len(nos_no_nivel)
            pos[node] = np.array([raio * np.cos(angulo), raio * np.sin(angulo)])

    # 4. Configuração das Cores
    cores_nos = []
    for node in G.nodes():
        if node == local_roubo: cores_nos.append('#e74c3c') # Vermelho (Roubo)
        elif node in saidas: cores_nos.append('#2ecc71')    # Verde (Portos)
        elif node in policias: cores_nos.append('#3498db')  # Azul (Polícia)
        else: cores_nos.append('#bdc3c7')                  # Cinza (Caminhos)

    # 5. Desenho do Gráfico
    plt.figure(figsize=(12, 12))
    plt.title(f"Mapa da Ilha - Visão de Radar (Centro: Vértice {local_roubo})", fontsize=15)

    nx.draw(G, pos, with_labels=True, node_color=cores_nos, node_size=800, 
            font_size=9, font_weight='bold', edge_color='#dcdde1', 
            arrows=True, arrowsize=15, width=1.2)

    # Exibir pesos das arestas
    labels_pesos = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels_pesos, font_size=7)

    # 6. Legenda Detalhada
    from matplotlib.lines import Line2D
    legend_elements = [
        Line2D([0], [0], marker='o', color='w', label='Local do Roubo (Castelo)', markerfacecolor='#e74c3c', markersize=10),
        Line2D([0], [0], marker='o', color='w', label='Portos de Saída', markerfacecolor='#2ecc71', markersize=10),
        Line2D([0], [0], marker='o', color='w', label='Equipes de Polícia', markerfacecolor='#3498db', markersize=10),
        Line2D([0], [0], marker='o', color='w', label='Vértices de Passagem', markerfacecolor='#bdc3c7', markersize=10)
    ]
    plt.legend(handles=legend_elements, loc='upper right', title="Legenda da Ilha")

    print("[INFO] Abrindo visualizador...")
    plt.show()

if __name__ == "__main__":
    carregar_e_desenhar_radial()