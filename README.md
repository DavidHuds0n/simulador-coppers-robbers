# Projeto: Coppers and Robbers

**Disciplina:** Algoritmos em Grafos - CCT/UFCA (2° Semestre de 2025) 

**Professor:** Carlos Vinicius G. C. Lima 

**Autor:** David Hudson Gomes Alves

---

## Descrição do Projeto
Este sistema simula uma perseguição policial em uma ilha isolada, modelada como um grafo direcionado e ponderado. O objetivo é interceptar um ladrão que tenta escapar do castelo (ponto mais alto) em direção a um dos portos (nível do mar). 

A dificuldade do terreno é representada pelos pesos das arestas: movimentos de descida possuem peso negativo (mais rápidos), enquanto subidas possuem peso positivo (maior esforço físico). Para solucionar o roteamento com pesos negativos de forma eficiente, o sistema utiliza o **Algoritmo de Floyd-Warshall** no pré-processamento, garantindo consultas de caminho mínimo em tempo constante $O(1)$ durante a simulação turno a turno.

---

## Pré-requisitos
* Python 3.x instalado na máquina.
* Nenhuma biblioteca externa é necessária (implementação construída com as estruturas nativas do Python).

---

## Estrutura dos Arquivos
* `main.py`: Script principal que gerencia o loop da simulação (movimentação de 1 vértice para o ladrão e 2 para a polícia por turno) e gera o relatório final.
* `grafo.py`: Módulo contendo a classe do Grafo, o parser do arquivo de texto e o motor matemático (Algoritmo de Floyd-Warshall).
* `mapa_exemplo.txt`: Arquivo de entrada descrevendo a topologia da ilha, pesos das arestas e posições iniciais.
* `gerador.py`: Script gerador procedural de mapas, responsável por criar novas topologias de ilha aleatórias que respeitam as regras físicas de altitude e pesos do projeto.
---

## Como Executar

**1. Configurar o Mapa:**
Certifique-se de que o arquivo de entrada (por padrão, `mapa_exemplo.txt`) está no mesmo diretório dos scripts. O arquivo deve seguir a seguinte formatação:

```text
VERTICES: <quantidade>
ARESTAS: <quantidade>
ROUBO: <vértice_inicial_do_ladrao>
SAIDAS: <vértices_de_saida_separados_por_espaco>
POLICIAIS: <quantidade_de_equipes>
POSICOES_POLICIA: <posicoes_iniciais_separadas_por_espaco>
CONEXOES:
<origem> <destino> <peso>
...
```

**2. Iniciar a Simulação:**
Abra o terminal no diretório do projeto e execute:

```text
python main.py
```

O programa abrirá um menu interativo perguntando se você deseja gerar um NOVO mapa aleatório (digitando 's') ou utilizar o mapa existente no arquivo de texto (digitando 'n'). Após a escolha, a simulação começará.