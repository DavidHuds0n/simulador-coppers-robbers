import random

# ==========================================================================
# --- CONFIGURAÇÕES DO GERADOR DA ILHA ---
# Altere os valores abaixo para criar diferentes cenários de teste.
# ==========================================================================
NUM_VERTICES_PADRAO = 25
ALTITUDE_CASTELO    = 100
ALTITUDE_PORTO      = 0
PROBABILIDADE_EXTRA = 0.4  # Chance de criar arestas adicionais além do caminho base

def gerar_mapa_aleatorio(caminho_arquivo="mapa_exemplo.txt", num_vertices=NUM_VERTICES_PADRAO, num_saidas=3, num_policiais=3):
    """
    Cria uma topologia de ilha procedural respeitando as regras físicas de descida/subida.
    """
    print(f"-> Gerando nova topologia da ilha com {num_vertices} vértices...")
    
    local_roubo = 1 # Castelo é sempre o vértice 1
    saidas = list(range(num_vertices - num_saidas + 1, num_vertices + 1))
    
    # --- Cálculo de Altitudes ---
    # Necessário para definir se o peso será negativo (descida) ou positivo (subida)
    altitudes = {local_roubo: ALTITUDE_CASTELO}
    for s in saidas: altitudes[s] = ALTITUDE_PORTO
    for v in range(2, num_vertices - num_saidas + 1):
        altitudes[v] = random.randint(10, 90)

    # Definição das equipes policiais em posições aleatórias (longe do castelo)
    candidatos_policia = [v for v in range(2, num_vertices + 1) if v not in saidas]
    posicoes_policia = random.sample(candidatos_policia, num_policiais)

    # --- Geração de Arestas ---
    conexoes = []
    for u in range(1, num_vertices - num_saidas + 1):
        # Garante que cada nó tenha pelo menos uma opção de caminho para frente/baixo
        destino_base = random.randint(u + 1, num_vertices)
        conexoes.append((u, destino_base))
        
        if random.random() < PROBABILIDADE_EXTRA:
            destino_extra = random.randint(2, num_vertices)
            if u != destino_extra: conexoes.append((u, destino_extra))

    # --- Aplicação dos Pesos Semânticos ---
    # Descida = Peso Negativo | Subida = Peso Positivo (maior esforço)
    linhas_conexoes = []
    arestas_vistas = set()
    for u, v in conexoes:
        if u == v or (u, v) in arestas_vistas: continue
        arestas_vistas.add((u, v))
        
        if altitudes[u] > altitudes[v]:
            peso = -random.randint(1, 5) # Rapidez da descida
        else:
            peso = random.randint(6, 12) # Esforço da subida
            
        linhas_conexoes.append(f"{u} {v} {peso}")

    # Escrita final no arquivo TXT seguindo o formato de entrada do projeto
    with open(caminho_arquivo, 'w') as f:
        f.write(f"VERTICES: {num_vertices}\n")
        f.write(f"ARESTAS: {len(linhas_conexoes)}\n")
        f.write(f"ROUBO: {local_roubo}\n")
        f.write(f"SAIDAS: {' '.join(map(str, saidas))}\n")
        f.write(f"POLICIAIS: {num_policiais}\n")
        f.write(f"POSICOES_POLICIA: {' '.join(map(str, posicoes_policia))}\n")
        f.write("CONEXOES:\n")
        f.write("\n".join(linhas_conexoes))
        
    print(f"-> Mapa salvo em '{caminho_arquivo}' com sucesso!")