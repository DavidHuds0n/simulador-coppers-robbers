from grafo import GrafoIlha
from gerador import gerar_mapa_aleatorio

# ==========================================================================
# --- MOTOR DE SIMULAÇÃO: COPPERS AND ROBBERS ---
# Gerencia a perseguição em turnos e gera o relatório oficial de saída.
# ==========================================================================

def simular_fuga(grafo):
    ladrao_pos = grafo.local_roubo
    policias_pos = list(grafo.posicoes_policia)
    
    turnos = 0
    caminho_ladrao = [ladrao_pos]
    caminhos_policias = {i: [pos] for i, pos in enumerate(policias_pos)}

    # O ladrão é inteligente: ele analisa todos os 6 portos e escolhe o que 
    # possui o menor custo acumulado via Floyd-Warshall 
    porto_alvo = min(grafo.saidas, key=lambda s: grafo.dist[ladrao_pos][s])
    print(f"[IA Ladrão] Alvo identificado: Porto {porto_alvo} (Custo: {grafo.dist[ladrao_pos][porto_alvo]})")

    while True:
        turnos += 1
        print(f"\n--- TURNO {turnos} ---")
        
        # 1. MOVIMENTAÇÃO DO LADRÃO (1 vértice por vez) [cite: 101]
        if ladrao_pos != porto_alvo:
            # Ele usa o conhecimento prévio do mapa para seguir a rota ótima 
            prox = grafo.pegar_proximo_passo(ladrao_pos, porto_alvo)
            if prox:
                ladrao_pos = prox
                caminho_ladrao.append(ladrao_pos)
                print(f"Ladrão moveu para {ladrao_pos}")

        if ladrao_pos in grafo.saidas:
            print("[RESULTADO] O ladrão alcançou um porto e escapou!")
            imprimir_relatorio(False, turnos, caminho_ladrao, caminhos_policias)
            break

        # 2. MOVIMENTAÇÃO DOS POLICIAIS (2 vértices por rodada na perseguição) 
        capturado = False
        for i, pos_pol in enumerate(policias_pos):
            # Durante a perseguição (após o roubo), a polícia dobra a velocidade 
            for passo in range(2):
                if pos_pol == ladrao_pos:
                    capturado = True; break
                
                # A polícia usa drones (identificação em tempo real) para perseguir o ladrão [cite: 70, 107]
                prox_p = grafo.pegar_proximo_passo(pos_pol, ladrao_pos)
                if prox_p:
                    pos_pol = prox_p
                    caminhos_policias[i].append(pos_pol)
            
            policias_pos[i] = pos_pol
            print(f"Equipe {i+1} está no vértice {pos_pol}")
            if pos_pol == ladrao_pos: capturado = True

        if capturado:
            print("\n!!! O LADRÃO FOI ALCANÇADO E PRESO !!!")
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