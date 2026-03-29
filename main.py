import random
import os
from grafo import GrafoIlha
from gerador import gerar_mapa_completo

def movimentar_patrulha(grafo, pos_atual, pos_anterior):
    # Retorna um vizinho aleatorio, evitando voltar imediatamente para o vertice anterior
    vizinhos = list(grafo.adjacencias.get(pos_atual, {}).keys())
    if not vizinhos:
        return pos_atual
        
    opcoes = [v for v in vizinhos if v != pos_anterior] if len(vizinhos) > 1 and pos_anterior in vizinhos else vizinhos
    return random.choice(opcoes)

def imprimir_relatorio_tentativa(sucesso, turnos, rota_l, rotas_p, tentativa, qtd_viaturas):
    print("\n" + "-" * 60)
    print(f"[{'VITORIA' if sucesso else 'FALHA'}] RELATORIO DA TENTATIVA {tentativa}")
    print("-" * 60)
    print(f"Viaturas Alocadas: {qtd_viaturas}")
    print(f"Duracao da perseguicao: {turnos} turnos")
    print(f"Caminho percorrido pelo Ladrao: {' -> '.join(map(str, rota_l))}")
    print("Caminho percorrido pelas Equipes:")
    for eq_id, rota in rotas_p.items():
        print(f"  Viatura {eq_id + 1}: {' -> '.join(map(str, rota))}")
    print("-" * 60 + "\n")

def executar_simulacao(grafo):
    total_equipes = len(grafo.posicoes_policia)
    
    # Turno 0: Movimentacao previa isolada
    print("\n[LOG] Turno 0: Viaturas em patrulha de rotina...")
    posicoes_iniciais = {}
    for i, pos in enumerate(grafo.posicoes_policia):
        nova_pos = movimentar_patrulha(grafo, pos, None)
        posicoes_iniciais[i] = {
            'pos': nova_pos,
            'ultimo_pos': pos
        }
        print(f"  Viatura {i+1} moveu de {pos} para {nova_pos}.")

    ladrao_inicio = grafo.local_roubo
    print(f"\n[ALERTA] Ocorrencia confirmada no vertice {ladrao_inicio}!")

    # Escalonamento de recursos (1 a N viaturas)
    for qtd_ativos in range(1, total_equipes + 1):
        print(f"\n>>> INICIANDO TENTATIVA DE CERCO ({qtd_ativos} viatura(s) alocada(s))")
        
        porto_alvo = min(grafo.saidas, key=lambda s: grafo.dist[ladrao_inicio][s])
        print(f"[SISTEMA] Rota de fuga provavel identificada: Porto {porto_alvo}.")

        # Restaura posicoes para o estado pos Turno 0
        equipes = []
        for i in range(total_equipes):
            equipes.append({
                'id': i,
                'pos': posicoes_iniciais[i]['pos'],
                'ultimo_pos': posicoes_iniciais[i]['ultimo_pos'],
                'status': 'patrulha',
                'caminho': [posicoes_iniciais[i]['pos']]
            })

        # Triagem tatica
        equipes_ordenadas = sorted(equipes, key=lambda e: grafo.dist[e['pos']][porto_alvo])
        print("[SISTEMA] Triagem de viaturas concluida:")
        for i in range(qtd_ativos):
            equipes_ordenadas[i]['status'] = 'perseguicao'
            print(f"  -> Viatura {equipes_ordenadas[i]['id'] + 1} assumiu modo perseguicao.")

        turnos = 0
        ladrao_pos = ladrao_inicio
        caminho_ladrao = [ladrao_pos]
        capturado = False

        while True:
            turnos += 1
            
            # 1. Movimentacao Fugitivo
            if ladrao_pos != porto_alvo:
                prox_l = grafo.pegar_proximo_passo(ladrao_pos, porto_alvo)
                if prox_l:
                    ladrao_pos = prox_l
                    caminho_ladrao.append(ladrao_pos)

            # 2. Movimentacao Policia
            for eq in equipes:
                if eq['status'] == 'perseguicao':
                    for _ in range(2):
                        if eq['pos'] == ladrao_pos:
                            capturado = True
                        
                        prox_p = grafo.pegar_proximo_passo(eq['pos'], ladrao_pos)
                        if prox_p:
                            eq['ultimo_pos'] = eq['pos']
                            eq['pos'] = prox_p
                            eq['caminho'].append(eq['pos'])
                else:
                    nova_pos = movimentar_patrulha(grafo, eq['pos'], eq['ultimo_pos'])
                    eq['ultimo_pos'] = eq['pos']
                    eq['pos'] = nova_pos
                    eq['caminho'].append(eq['pos'])
                
                if eq['pos'] == ladrao_pos:
                    capturado = True

            # 3. Analise do Turno
            if capturado:
                print(f"\n[SISTEMA] Alvo interceptado no vertice {ladrao_pos}!")
                rotas_finais = {e['id']: e['caminho'] for e in equipes}
                imprimir_relatorio_tentativa(True, turnos, caminho_ladrao, rotas_finais, qtd_ativos, qtd_ativos)
                return True

            if ladrao_pos == porto_alvo:
                print(f"\n[SISTEMA] O alvo alcancou o porto {porto_alvo} e escapou.")
                rotas_finais = {e['id']: e['caminho'] for e in equipes}
                imprimir_relatorio_tentativa(False, turnos, caminho_ladrao, rotas_finais, qtd_ativos, qtd_ativos)
                
                if qtd_ativos < total_equipes:
                    print("[SISTEMA] Reavaliando estrategia. Acionando reforcos para a proxima simulacao...")
                    break # Interrompe o while para iniciar a proxima tentativa no for
                else:
                    print("[SISTEMA] Fuga total. Todas as equipes foram esgotadas.")
                    return False

def main():
    print("SISTEMA DE SEGURANCA: COPPERS & ROBBERS\n")
    
    while True:
        if not os.path.exists("mapa_exemplo.txt") or input("Gerar novo cenario aleatorio? (s/n): ").lower() == 's':
            gerar_mapa_completo()
            
        ilha = GrafoIlha()
        ilha.carregar_mapa("mapa_exemplo.txt")
        
        print("[SISTEMA] Construindo matriz de rotas (Floyd-Warshall)...")
        ilha.executar_floyd_warshall()
        
        sucesso = executar_simulacao(ilha)
        
        if not sucesso:
            if input("Deseja tentar capturar o ladrao em um novo mapa? (s/n): ").lower() != 's':
                break
        else:
            if input("Operacao concluida. Iniciar nova simulacao? (s/n): ").lower() != 's':
                break

    print("Encerrando sistema.")

if __name__ == "__main__":
    main()