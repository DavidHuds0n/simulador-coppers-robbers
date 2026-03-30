# Projeto: Coppers and Robbers

**Disciplina:** Algoritmos em Grafos - CCT/UFCA (2° Semestre de 2025) 

**Professor:** Carlos Vinicius G. C. Lima 

**Autores:** David Hudson Gomes Alves e Luann Alves Pereira de Lima

---

## Descrição do Projeto
Este sistema simula uma perseguição policial em uma ilha isolada, modelada como um grafo direcionado e ponderado. O objetivo é interceptar um ladrão que tenta escapar do castelo (ponto mais alto) em direção a um dos portos (nível do mar). 

A dificuldade do terreno é representada pelos pesos das arestas: movimentos de descida possuem peso negativo (mais rápidos), enquanto subidas possuem peso positivo (maior esforço físico). Para solucionar o roteamento com pesos negativos de forma eficiente e sem ciclos negativos, o sistema utiliza o **Algoritmo de Floyd-Warshall** no pré-processamento. Isso garante que as consultas de caminho mínimo durante a simulação (turno a turno) ocorram em tempo constante $O(1)$.

A inteligência da simulação aplica uma estratégia de escalonamento de recursos: o sistema tenta capturar o alvo utilizando a menor quantidade possível de viaturas, acionando primeiro as equipes taticamente mais próximas e mantendo as demais em patrulha civil.

---

## Divisão de Tarefas
Para a execução deste projeto, as responsabilidades foram divididas da seguinte forma:

* **David Hudson:** Infraestrutura de Dados e Matemática. Responsável pela geração procedural dos mapas (garantindo as regras físicas de relevo), modelagem da classe do Grafo, leitura do arquivo de configuração e implementação do algoritmo de Floyd-Warshall.
* **Luann Alves:** Lógica de Negócio e Motor de Turnos. Responsável pelo algoritmo de triagem de equipes (alocação de recursos), movimentação diferenciada (patrulha vs. perseguição), escalonamento de tentativas (cerco) e geração dos relatórios de análise no terminal.

---

## Pré-requisitos
* Python 3.x instalado na máquina.
* Nenhuma biblioteca externa é necessária (implementação construída nativamente para as lógicas de grafos).

---

## Estrutura dos Arquivos
* `main.py`: Script principal que gerencia o loop da simulação (movimentação diferenciada por turno, relatórios de tentativas e controle do Turno 0).
* `grafo.py`: Módulo contendo a classe do Grafo, o parser do arquivo de texto e o motor matemático (Algoritmo de Floyd-Warshall).
* `mapa_exemplo.txt`: Arquivo de entrada descrevendo a topologia da ilha, pesos das arestas e posições iniciais.
* `gerador.py`: Script gerador procedural de mapas, responsável por criar novas topologias de ilha aleatórias que respeitam as regras do projeto.

---

## Como Executar

**1. Configurar o Mapa:**
Certifique-se de que o arquivo de entrada (por padrão, `mapa_exemplo.txt`) está no mesmo diretório dos scripts. O arquivo deve seguir a formatação oficial do projeto:

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

```bash
python main.py
```

O programa abrirá um menu interativo perguntando se você deseja gerar um NOVO mapa aleatório (digitando 's') ou utilizar o mapa existente no arquivo de texto (digitando 'n'). Após a escolha, o sistema processará as rotas e a simulação começará com relatórios gerados a cada tentativa de cerco.

---

## Vídeo de Apresentação
Conforme exigido nas especificações do projeto, segue o link com a explicação técnica das implementações de ambos os membros da equipe:

* **Apresentação Completa (David Hudson e Luann Alves):** [Assistir no Google Drive](https://drive.google.com/file/d/1yStg1EYTitB5qVV1ga6fm93vFODuu6Q2/view?usp=sharing)