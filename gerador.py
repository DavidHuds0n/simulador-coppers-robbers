import random

def gerar_mapa_aleatorio(caminho_arquivo="mapa_exemplo.txt", num_vertices=20, num_saidas=3, num_policiais=3):
    print(f"-> Gerando nova topologia da ilha com {num_vertices} vértices...")
    
    local_roubo = 1
    # Define as saídas nos últimos vértices
    saidas = list(range(num_vertices - num_saidas + 1, num_vertices + 1))
    
    # Define as altitudes para calcular os pesos corretamente
    altitudes = {}
    altitudes[local_roubo] = 100  # Castelo no topo
    for s in saidas:
        altitudes[s] = 0          # Portos no nível do mar
        
    for v in range(2, num_vertices - num_saidas + 1):
        altitudes[v] = random.randint(10, 90) # Vértices intermediários

    # Posições da polícia (não podem nascer no castelo nem nas saídas)
    candidatos_policia = [v for v in range(2, num_vertices + 1) if v not in saidas]
    posicoes_policia = random.sample(candidatos_policia, num_policiais)

    # Gera as conexões garantindo que exista caminho para descer
    conexoes = []
    
    # Conecta o castelo a alguns vértices logo abaixo
    for _ in range(random.randint(2, 4)):
        destino = random.randint(2, num_vertices - num_saidas)
        conexoes.append((local_roubo, destino))

    # Conecta o meio da ilha
    for u in range(2, num_vertices - num_saidas + 1):
        # Garante pelo menos uma rota de descida para cada nó
        destino_descida = random.randint(u + 1, num_vertices)
        conexoes.append((u, destino_descida))
        
        # Adiciona algumas rotas extras aleatórias (podem ser subidas ou descidas)
        if random.random() > 0.5:
            destino_extra = random.randint(2, num_vertices)
            if u != destino_extra:
                conexoes.append((u, destino_extra))

    # Formata as arestas com os pesos exigidos pelo professor
    arestas_finais = set()
    linhas_conexoes = []
    for u, v in conexoes:
        if u == v or (u, v) in arestas_finais: continue
        
        arestas_finais.add((u, v))
        
        # Se estiver descendo, peso negativo.
        if altitudes[u] > altitudes[v]:
            peso = -random.randint(1, 5)
        # Se estiver subindo, peso positivo e maior em módulo que a descida.
        else:
            peso = random.randint(6, 12)
            
        linhas_conexoes.append(f"{u} {v} {peso}")

    # Escreve no arquivo de texto
    with open(caminho_arquivo, 'w') as f:
        f.write(f"VERTICES: {num_vertices}\n")
        f.write(f"ARESTAS: {len(linhas_conexoes)}\n")
        f.write(f"ROUBO: {local_roubo}\n")
        f.write(f"SAIDAS: {' '.join(map(str, saidas))}\n")
        f.write(f"POLICIAIS: {num_policiais}\n")
        f.write(f"POSICOES_POLICIA: {' '.join(map(str, posicoes_policia))}\n")
        f.write("CONEXOES:\n")
        f.write("\n".join(linhas_conexoes))
        
    print(f"-> Mapa salvo em {caminho_arquivo} com sucesso!\n")