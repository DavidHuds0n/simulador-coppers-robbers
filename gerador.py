import random

# ==========================================================================
# --- GERADOR DE MAPA ESCALÁVEL E ESTRATÉGICO ---
# Este código cria a ilha garantindo que o ladrão não escape no 1º turno
# e que a física do relevo impeça erros matemáticos (ciclos negativos).
# ==========================================================================

def gerar_mapa_completo(caminho_arquivo="mapa_exemplo.txt"):
    print("=== Configuração da Ilha: Coppers and Robbers ===")
    
    # 1. Definição da Escala do Grafo
    try:
        n = int(input("Digite a quantidade de vértices (ex: 30): "))
    except ValueError:
        print("[AVISO] Entrada inválida. Usando padrão de 30 vértices.")
        n = 30

    local_roubo = 1
    num_saidas = max(3, int(n * 0.20))    # 20% do mapa são portos
    num_policiais = max(2, int(n * 0.10)) # 10% do mapa são policiais

    # 2. Posicionamento Estratégico (Filtro de Proximidade)
    # Sorteamos as saídas apenas na metade final dos vértices para garantir distância do Vértice 1
    candidatos_saidas = [v for v in range(n // 3, n + 1) if v != local_roubo]
    saidas = random.sample(candidatos_saidas, num_saidas)

    # Policiais começam em posições aleatórias, longe do roubo e das saídas
    candidatos_policia = [v for v in range(2, n + 1) if v not in saidas]
    posicoes_policia = random.sample(candidatos_policia, num_policiais)

    # 3. Atribuição de Relevo (Altitudes)
    # O Roubo é o ponto mais alto (100) e os Portos os mais baixos (0)
    altitudes = {local_roubo: 100}
    for s in saidas: altitudes[s] = 0
    for v in range(2, n + 1):
        if v not in altitudes:
            altitudes[v] = random.randint(20, 80) # Terreno intermediário

    # 4. Criação de Conexões com Regras de Segurança
    conexoes_set = set()

    def eh_conexao_valida(u, v):
        # REGRA DE OURO: Proibido ligar o Roubo direto a um Porto (Saída)
        if u == local_roubo and v in saidas: return False
        if v == local_roubo and u in saidas: return False
        return u != v

    # Garantia de Conectividade Forte (Anel que liga todos os nós)
    nos_embaralhados = list(range(1, n + 1))
    random.shuffle(nos_embaralhados)
    for i in range(n):
        u, v = nos_embaralhados[i], nos_embaralhados[(i + 1) % n]
        if eh_conexao_valida(u, v):
            conexoes_set.add((min(u, v), max(u, v)))

    # Adição de Atalhos Proporcionais
    num_atalhos = int(n * 1.5)
    for _ in range(num_atalhos):
        u, v = random.sample(range(1, n + 1), 2)
        if eh_conexao_valida(u, v):
            conexoes_set.add((min(u, v), max(u, v)))

    # 5. Cálculo de Pesos (Física de Esforço - Ida e Volta)
    linhas_conexoes = []
    for u, v in conexoes_set:
        diff = altitudes[u] - altitudes[v]
        esforco_base = max(1, abs(diff) // 10)
        penalidade_subida = random.randint(10, 15) # Garante que peso total do ciclo seja > 0

        if altitudes[u] > altitudes[v]:
            # u -> v (Descida: Rápida/Negativa) | v -> u (Subida: Lenta/Positiva)
            linhas_conexoes.append(f"{u} {v} {-esforco_base}")
            linhas_conexoes.append(f"{v} {u} {esforco_base + penalidade_subida}")
        elif altitudes[u] < altitudes[v]:
            # v -> u (Descida) | u -> v (Subida)
            linhas_conexoes.append(f"{v} {u} {-esforco_base}")
            linhas_conexoes.append(f"{u} {v} {esforco_base + penalidade_subida}")
        else:
            # Planície: esforço positivo igual para ambos os lados
            linhas_conexoes.append(f"{u} {v} {esforco_base + 5}")
            linhas_conexoes.append(f"{v} {u} {esforco_base + 5}")

    # 6. Escrita do Arquivo .txt
    with open(caminho_arquivo, 'w') as f:
        f.write(f"VERTICES: {n}\n")
        f.write(f"ARESTAS: {len(linhas_conexoes)}\n")
        f.write(f"ROUBO: {local_roubo}\n")
        f.write(f"SAIDAS: {' '.join(map(str, sorted(saidas)))}\n")
        f.write(f"POLICIAIS: {num_policiais}\n")
        f.write(f"POSICOES_POLICIA: {' '.join(map(str, posicoes_policia))}\n")
        f.write("CONEXOES:\n")
        f.write("\n".join(linhas_conexoes))

    print(f"\n[SUCESSO] Mapa '{caminho_arquivo}' gerado com {n} vértices!")

if __name__ == "__main__":
    gerar_mapa_completo()