from grafo import GrafoIlha
from gerador import gerar_mapa_aleatorio

# ==========================================================================
# --- MOTOR DE SIMULAÇÃO: COPPERS AND ROBBERS ---
# Gerencia a perseguição em turnos e gera o relatório oficial de saída.
# ==========================================================================

def simular_fuga(grafo):
    """
    Executa o loop principal da perseguição.
    Regras: Ladrão anda 1 passo, Polícia anda 2 passos por rodada.
    """
    ladrao_pos = grafo.local_roubo
    policias_pos = list(grafo.posicoes_policia)
    
    # Estruturas para o relatório final (Análise e Discussão)
    turnos = 0
    caminho_ladrao = [ladrao_pos]
    caminhos_policias = {i: [pos] for i, pos in enumerate(policias_pos)}
    
    # Estratégia do Ladrão: Ir para a saída que oferece o menor custo total
    saida_alvo = min(grafo.saidas, key=lambda s: grafo.dist[ladrao_pos][s])
    
    while True:
        turnos += 1
        print(f"\n--- TURNO {turnos} ---")
        
        # --- 1. MOVIMENTAÇÃO DO LADRÃO ---
        if ladrao_pos != saida_alvo:
            prox = grafo.pegar_proximo_passo(ladrao_pos, saida_alvo)
            if prox:
                ladrao_pos = prox
                caminho_ladrao.append(ladrao_pos)
                print(f"O Ladrão desceu para o vértice {ladrao_pos}.")
        
        # Condição de Vitória 1: Fuga bem-sucedida
        if ladrao_pos in grafo.saidas:
            imprimir_relatorio(False, turnos, caminho_ladrao, caminhos_policias)
            break

        # --- 2. MOVIMENTAÇÃO DA POLÍCIA ---
        capturado = False
        for i, pos_atual in enumerate(policias_pos):
            # A polícia é 2x mais rápida: executa dois movimentos por turno
            for movimento in range(2):
                if pos_atual == ladrao_pos:
                    capturado = True; break
                
                # A polícia sempre recalcula o caminho mínimo até a posição atual do ladrão
                passo = grafo.pegar_proximo_passo(pos_atual, ladrao_pos)
                if passo:
                    pos_atual = passo
                    caminhos_policias[i].append(pos_atual)
            
            policias_pos[i] = pos_atual
            print(f"Equipe {i+1} avançou para o vértice {pos_atual}.")
            if pos_atual == ladrao_pos: capturado = True
                
        # Condição de Vitória 2: Captura
        if capturado:
            print("\n!!! O LADRÃO FOI CERCADO E PRESO !!!")
            imprimir_relatorio(True, turnos, caminho_ladrao, caminhos_policias)
            break

def imprimir_relatorio(sucesso_policia, turnos, cam_ladrao, cam_policias):
    """Gera a saída detalhada para o arquivo de análise do projeto."""
    print("\n" + "="*45)
    print("      RELATÓRIO FINAL DA OPERAÇÃO")
    print("="*45)
    
    etapa_str = "etapa" if turnos == 1 else "etapas"
    
    if sucesso_policia:
        print(f"STATUS: Ladrão CAPTURADO em {turnos} {etapa_str}.")
        print(f"MOMENTO DO ALCANCE: Turno {turnos}.")
    else:
        print(f"STATUS: Ladrão ESCAPOU em {turnos} {etapa_str}.")
        
    print(f"EQUIPES ENVOLVIDAS: {len(cam_policias)}")
    print(f"TRAJETÓRIA DO LADRÃO: {' -> '.join(map(str, cam_ladrao))}")
    print("TRAJETÓRIA DAS EQUIPES:")
    for equipe, rota in cam_policias.items():
        print(f"  Equipe {equipe+1}: {' -> '.join(map(str, rota))}")
    print("="*45 + "\n")

# --- BLOCO PRINCIPAL ---
if __name__ == "__main__":
    print("="*45)
    print("   SISTEMA DE SEGURANÇA: COPPERS & ROBBERS")
    print("="*45)
    
    # Interação para geração de dados
    if input("Deseja gerar um novo cenário aleatório? (s/n): ").lower() == 's':
        gerar_mapa_aleatorio()
    
    ilha = GrafoIlha()
    ilha.carregar_mapa("mapa_exemplo.txt")
    
    print("\n[INFO] Pré-processando rotas otimizadas...")
    ilha.executar_floyd_warshall()
    
    print("[INFO] Simulação iniciada!")
    simular_fuga(ilha)