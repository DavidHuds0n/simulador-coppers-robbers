from grafo import GrafoIlha

def simular_fuga(grafo):
    ladrao_pos = grafo.local_roubo
    policias_pos = list(grafo.posicoes_policia)
    
    # Logs para o relatório final
    turnos = 0
    caminho_ladrao = [ladrao_pos]
    caminhos_policias = {i: [pos] for i, pos in enumerate(policias_pos)}
    
    # Descobre qual é a saída mais próxima do ladrão usando as distâncias pré-calculadas
    saida_alvo = min(grafo.saidas, key=lambda s: grafo.dist[ladrao_pos][s])
    
    while True:
        turnos += 1
        print(f"\n--- TURNO {turnos} ---")
        
        # 1. Movimento do Ladrão (1 vértice por vez)
        if ladrao_pos != saida_alvo:
            prox_passo = grafo.pegar_proximo_passo(ladrao_pos, saida_alvo)
            if prox_passo is not None:
                ladrao_pos = prox_passo
                caminho_ladrao.append(ladrao_pos)
                print(f"Ladrão correu para o vértice {ladrao_pos}.")
        
        # Verifica se o ladrão escapou logo após se mover
        if ladrao_pos in grafo.saidas:
            gerar_relatorio(sucesso_policia=False, turnos=turnos, cam_ladrao=caminho_ladrao, cam_policias=caminhos_policias)
            break

        # 2. Movimento dos Policiais (2 vértices por vez na perseguição)
        ladrao_capturado = False
        
        for i, pos_atual in enumerate(policias_pos):
            for passo in range(2): # Move até 2 vezes
                if pos_atual == ladrao_pos:
                    ladrao_capturado = True
                    break
                    
                prox_passo_policia = grafo.pegar_proximo_passo(pos_atual, ladrao_pos)
                if prox_passo_policia is not None:
                    pos_atual = prox_passo_policia
                    caminhos_policias[i].append(pos_atual)
                    
            policias_pos[i] = pos_atual # Atualiza a posição oficial da equipe
            print(f"Equipe {i+1} avançou para o vértice {pos_atual}.")
            
            if pos_atual == ladrao_pos:
                ladrao_capturado = True
                
        # Verifica condição de vitória da polícia
        if ladrao_capturado:
            print("\n!!! O LADRÃO FOI CERCADO E PRESO !!!")
            gerar_relatorio(sucesso_policia=True, turnos=turnos, cam_ladrao=caminho_ladrao, cam_policias=caminhos_policias)
            break

def gerar_relatorio(sucesso_policia, turnos, cam_ladrao, cam_policias):
    """Gera a saída exigida pelos critérios do projeto."""
    print("\n" + "="*40)
    print("RELATÓRIO OFICIAL DA OPERAÇÃO")
    print("="*40)
    
    if sucesso_policia:
        print(f"Resultado: Ladrão CAPTURADO em {turnos} etapas." ) 
        print(f"Equipes necessárias: {len(cam_policias)}.") 
    else:
        print(f"Resultado: Ladrão ESCAPOU em {turnos} etapas." ) 
        
    print(f"Sequência do Ladrão: {' -> '.join(map(str, cam_ladrao))}") 
    
    print("Caminho percorrido pelas equipes policiais:") 
    for equipe, caminho in cam_policias.items():
        print(f"  Equipe {equipe + 1}: {' -> '.join(map(str, caminho))}")
    print("="*40 + "\n")

if __name__ == "__main__":
    ilha = GrafoIlha()
    print("Carregando mapa e inicializando sistema de segurança...")
    ilha.carregar_mapa("mapa_exemplo.txt")
    
    print("Calculando rotas estratégicas (Floyd-Warshall)...")
    ilha.executar_floyd_warshall()
    
    print("Iniciando simulação de perseguição!")
    simular_fuga(ilha)