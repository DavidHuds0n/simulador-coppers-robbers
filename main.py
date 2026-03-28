from grafo import GrafoIlha
from gerador import gerar_mapa_completo

# ==========================================================================
# --- MOTOR DE SIMULAÇÃO: COPPERS AND ROBBERS ---
# Gerencia a perseguição em turnos e gera o relatório oficial de saída.
# ==========================================================================

import random

def movimentar_patrulha_aleatoria(grafo, eq):
    """
    Move o patrulheiro para um vizinho aleatório, evitando retornar imediatamente.
    """
    vizinhos = list(grafo.adjacencias.get(eq['pos'], {}).keys())
    if not vizinhos:
        return eq['pos']
        
    if len(vizinhos) > 1 and eq['ultimo_pos'] in vizinhos:
        opcoes = [v for v in vizinhos if v != eq['ultimo_pos']]
    else:
        opcoes = vizinhos

    escolha = random.choice(opcoes)
    eq['ultimo_pos'] = eq['pos'] 
    return escolha

def executar_rodada_perseguicao(grafo, num_ativos):
    ladrao_pos = grafo.local_roubo
    porto_alvo = min(grafo.saidas, key=lambda s: grafo.dist[ladrao_pos][s])
    
    equipes = []
    for i, pos in enumerate(grafo.posicoes_policia):
        equipes.append({
            'id': i,
            'pos': pos,
            'status': 'patrulha',
            'ultimo_pos': None,
            'caminho': [pos]
        })

    # Triagem para definir perseguidores ativos
    equipes_ordenadas = sorted(equipes, key=lambda e: grafo.dist[e['pos']][porto_alvo])
    for i in range(min(num_ativos, len(equipes))):
        equipes_ordenadas[i]['status'] = 'perseguicao'

    turnos = 0
    caminho_ladrao = [ladrao_pos]
    
    while True:
        turnos += 1
        
        # 1. Movimentação do Ladrão (Velocidade 1)
        if ladrao_pos != porto_alvo:
            prox_l = grafo.pegar_proximo_passo(ladrao_pos, porto_alvo)
            if prox_l:
                ladrao_pos = prox_l
                caminho_ladrao.append(ladrao_pos)

        # 2. Movimentação da Polícia
        alguem_capturou = False
        for eq in equipes:
            if eq['status'] == 'perseguicao':
                # Perseguidores (Velocidade 2)
                for _ in range(2):
                    # Se o ladrão já foi pego por OUTRA equipe, este policial ainda se move
                    # em direção à posição onde o ladrão foi interceptado.
                    if eq['pos'] == ladrao_pos:
                        alguem_capturou = True
                        # Não damos 'break' aqui para permitir o fim do movimento total do turno
                    
                    prox_p = grafo.pegar_proximo_passo(eq['pos'], ladrao_pos)
                    if prox_p:
                        eq['ultimo_pos'] = eq['pos']
                        eq['pos'] = prox_p
                        eq['caminho'].append(eq['pos'])
            else:
                # Patrulheiros (Velocidade 1)
                nova_pos = movimentar_patrulha_aleatoria(grafo, eq)
                eq['pos'] = nova_pos
                eq['caminho'].append(eq['pos'])
            
            # Verifica se ESTA equipe alcançou o ladrão após seus movimentos
            if eq['pos'] == ladrao_pos:
                alguem_capturou = True

        # 3. Verificação de Condições de Parada (APÓS todos se moverem)
        if alguem_capturou:
            return True, turnos, caminho_ladrao, {e['id']: e['caminho'] for e in equipes}
        
        if ladrao_pos == porto_alvo:
            return False, turnos, caminho_ladrao, {e['id']: e['caminho'] for e in equipes}
def simular_fuga(grafo):
    """
    Gerencia o ciclo de tentativas escalonadas. 
    Mantida conforme estrutura original, apenas garantindo o fluxo.
    """
    total_equipes = len(grafo.posicoes_policia)
    
    for qtd_perseguidores in range(1, total_equipes + 1):
        print(f"\n{'='*20} TENTATIVA {qtd_perseguidores} {'='*20}")
        print(f"[INFO] Operação com {qtd_perseguidores} equipe(s) em perseguição ativa.")
        
        sucesso, turnos, rota_l, rotas_p = executar_rodada_perseguicao(grafo, qtd_perseguidores)
        
        if sucesso:
            print(f"\n!!! SUCESSO NA TENTATIVA {qtd_perseguidores} !!!")
            imprimir_relatorio(True, turnos, rota_l, rotas_p)
            return
        else:
            print(f"\n[FALHA] O ladrão escapou da(s) {qtd_perseguidores} equipe(s).")
            if qtd_perseguidores < total_equipes:
                print("Reiniciando operação com reforço tático...")
            else:
                print("[DERROTA] O ladrão escapou de todo o cerco policial.")
                imprimir_relatorio(False, turnos, rota_l, rotas_p)

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
        gerar_mapa_completo()
    
    ilha = GrafoIlha()
    ilha.carregar_mapa("mapa_exemplo.txt")
    
    print("\n[INFO] Pré-processando rotas otimizadas...")
    ilha.executar_floyd_warshall()
    
    print("[INFO] Simulação iniciada!")
    simular_fuga(ilha)