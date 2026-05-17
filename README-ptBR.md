🌎 Language / Idioma:  
[🇺🇸 English](README.md) | [🇧🇷 Português](README-ptBR.md)

---

# 🗺️ TSP — Comparando Métodos de Busca de Estado

Implementação e comparação de três abordagens para resolver o **Problema do Caixeiro Viajante (TSP — Travelling Salesman Problem)**: força bruta, branch and bound e a heurística 2-opt.

---

## 📋 Sumário

- [Sobre](#sobre)
- [O Problema do Caixeiro Viajante](#o-problema-do-caixeiro-viajante)
- [Métodos Implementados](#métodos-implementados)
  - [Força Bruta](#1-força-bruta)
  - [Branch and Bound](#2-branch-and-bound)
  - [Heurística 2-opt](#3-heurística-2-opt)
- [Comparação dos Métodos](#comparação-dos-métodos)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Instâncias Disponíveis](#instâncias-disponíveis)
- [Como Rodar](#como-rodar)
- [Exemplos de Saída](#exemplos-de-saída)
- [Formato dos Arquivos .tsp](#formato-dos-arquivos-tsp)

---

## Sobre

Este projeto implementa e compara três estratégias clássicas de busca de estado aplicadas ao TSP. Cada método é avaliado em três dimensões:

- 🎯 **Qualidade da solução** — quão próximo o resultado está do ótimo real?
- ⚡ **Eficiência da busca** — quantos nós foram explorados, podados ou iterados?
- 📈 **Escalabilidade** — em que tamanho de problema cada abordagem começa a falhar?

Quando a solução exata está disponível, o programa também calcula o **gap de otimalidade** da heurística, fornecendo uma medida concreta de quanto de qualidade foi trocado por velocidade.

---

## 🧩 O Problema do Caixeiro Viajante

Dado um conjunto de cidades e as distâncias entre cada par delas, o objetivo é encontrar a **rota mais curta que visita todas as cidades exatamente uma vez e retorna à cidade de origem**.

Apesar da formulação simples, o TSP é **NP-difícil**: o número de rotas possíveis cresce fatorialmente com o número de cidades. Com `n` cidades, há `(n-1)!` permutações a considerar — 362.880 rotas para apenas 10 cidades, e mais de 60 trilhões para 20.

---

## ⚙️ Métodos Implementados

### 1. Força Bruta

**Arquivo:** `brute_force.py`

Explora **todas as permutações possíveis** de cidades por meio de uma busca em profundidade (DFS) recursiva. Garante o ótimo global, mas tem complexidade **O(n!)** — tornando-se impraticável para mais de ~11 cidades.

**Como funciona:**

1. Fixa a cidade inicial (nó `start`).
2. Executa uma DFS por todas as ordenações possíveis das cidades restantes.
3. A cada rota completa, calcula o custo total (incluindo o retorno) e atualiza o melhor resultado se for menor.
4. Retorna a rota de menor custo junto com as métricas de exploração.

**Métricas reportadas:**
- `permutacoes_completas` — total de rotas completas avaliadas, igual a `(n-1)!`
- `explorados` — total de nós expandidos na árvore de busca

**Complexidade:** O(n!) em tempo, O(n) em espaço (pilha de recursão)

**Limite prático:** até **11 cidades** (configurado em `main.py`)

---

### 2. Branch and Bound

**Arquivo:** `branch_bound.py`

Uma evolução da força bruta que introduz **podas**: sempre que o limite inferior do custo de um caminho parcial já atinge ou supera a melhor solução conhecida, aquele ramo inteiro é descartado sem precisar ser explorado.

**Como funciona:**

1. Também executa uma DFS recursiva a partir de `start`.
2. Antes de expandir cada nó, calcula um **lower bound** (limite inferior) para o custo total de qualquer rota que passe por aquele estado parcial. O bound é composto por quatro partes:
   - Custo acumulado até o momento
   - Aresta mais barata conectando o nó atual a alguma cidade não visitada
   - Custo da **Árvore Geradora Mínima (MST)** sobre todas as cidades não visitadas (calculada com o algoritmo de Prim)
   - Aresta mais barata conectando alguma cidade não visitada de volta à origem
3. Se `lower_bound >= melhor_custo_conhecido`, o ramo é **podado**.
4. Os candidatos em cada nível são ordenados pela aresta mais barata a partir do nó atual — isso favorece encontrar boas soluções cedo e torna as podas mais eficazes.

**Métricas reportadas:**
- `tours_evaluated` — soluções completas encontradas
- `explorados` — nós efetivamente expandidos
- `podados` — ramos descartados pela poda

**Complexidade:** O(n!) no pior caso, mas muito inferior na prática devido às podas

**Limite prático:** até **16 cidades** (configurado em `main.py`)

---

### 3. Heurística 2-opt

**Arquivo:** `two_opt.py`

Não garante a solução ótima, mas encontra **rotas de boa qualidade em tempo polinomial** — aplicável a instâncias grandes com centenas ou milhares de cidades.

**Como funciona:**

1. **Construção inicial:** gera uma rota de partida usando o algoritmo do **vizinho mais próximo** (`nearest_neighbor_initial_route`) — começa em `start` e sempre se move para a cidade não visitada mais próxima.
2. **Refinamento 2-opt:** testa iterativamente todas as trocas possíveis de dois segmentos da rota. Uma troca 2-opt remove duas arestas e reconecta os segmentos resultantes na ordem inversa. Se a nova rota for mais barata, ela substitui a atual.
3. O loop termina quando nenhuma troca 2-opt melhora a solução (ótimo local atingido).

**Métricas reportadas:**
- `tours_evaluated` — rotas candidatas avaliadas durante as trocas
- `iterations` — passagens completas por todas as trocas possíveis até a convergência

**Complexidade:** O(n²) por iteração, O(n² × k) no total, onde `k` é o número de iterações até convergência

**Sem limite de tamanho:** roda em todas as instâncias, incluindo a280 (280 cidades)

---

## 📊 Comparação dos Métodos

| Critério | Força Bruta | Branch and Bound | 2-opt |
|---|---|---|---|
| **Garantia de ótimo** | ✅ Sim | ✅ Sim | ❌ Não (ótimo local) |
| **Complexidade** | O(n!) | O(n!) com podas | O(n² × iter) |
| **Escalabilidade** | Até ~11 cidades | Até ~16 cidades | Sem limite prático |
| **Velocidade** | Lento | Moderado | Muito rápido |
| **Lower bound** | Não utiliza | MST + vizinhos | N/A |
| **Estratégia** | Busca exaustiva | Busca exaustiva com poda | Busca local iterativa |

**Quando usar cada um:**

- 🔵 **Força bruta** — instâncias pequenas (até ~11 cidades) onde o ótimo exato é necessário e o tempo não é crítico.
- 🟡 **Branch and bound** — instâncias pequenas a médias (até ~16 cidades) onde ainda se exige a solução ótima, mas com execução significativamente mais rápida que a força bruta.
- 🟢 **2-opt** — instâncias grandes onde a velocidade importa. A solução pode não ser ótima, mas o gap costuma ser pequeno na prática.

---

## 🗂️ Estrutura do Projeto

```
tsp/
├── main.py              # Ponto de entrada: carrega o grafo e executa os 3 métodos
├── graph.py             # Classe Graph: lê arquivos .tsp e calcula distâncias
├── brute_force.py       # Método 1: força bruta por DFS exaustiva
├── branch_bound.py      # Método 2: branch and bound com lower bound por MST
├── two_opt.py           # Método 3: heurística 2-opt com inicialização por vizinho mais próximo
└── instances/
    ├── test4.tsp        # 4 cidades (quadrado) — bom para testes rápidos
    ├── test8.tsp        # 8 cidades — roda os 3 métodos
    ├── bayg29.tsp       # 29 cidades (Bavária) — apenas 2-opt
    ├── gr48.tsp         # 48 cidades — apenas 2-opt
    ├── brazil58.tsp     # 58 cidades brasileiras — apenas 2-opt
    └── a280.tsp         # 280 cidades (problema de perfuração) — apenas 2-opt
```

### Descrição dos módulos

**`graph.py` — Classe `Graph`**

Responsável pela leitura dos arquivos `.tsp` e pela representação do grafo como matriz de distâncias. Formatos suportados:

- `EDGE_WEIGHT_TYPE`: `EUC_2D`, `CEIL_2D`, `ATT` (calculados a partir de coordenadas)
- `EDGE_WEIGHT_FORMAT`: `FULL_MATRIX`, `UPPER_ROW`, `UPPER_DIAG_ROW`, `LOWER_ROW`, `LOWER_DIAG_ROW` (matrizes explícitas)

**`main.py` — Orquestrador**

- Valida o argumento de linha de comando
- Carrega o grafo a partir do arquivo `.tsp`
- Decide quais métodos executar com base no tamanho da instância:
  - Força bruta: apenas se `n ≤ 11`
  - Branch and bound: apenas se `n ≤ 16`
  - 2-opt: sempre
- Exibe os resultados de cada método e calcula o gap da heurística quando o ótimo está disponível

---

## 📦 Instâncias Disponíveis

| Arquivo | Cidades | Formato | Origem | Métodos executados |
|---|---|---|---|---|
| `test4.tsp` | 4 | EUC_2D | Personalizada | Brute Force + B&B + 2-opt |
| `test8.tsp` | 8 | EUC_2D | Personalizada | Brute Force + B&B + 2-opt |
| `bayg29.tsp` | 29 | UPPER_ROW | Bavária, Alemanha | Apenas 2-opt |
| `gr48.tsp` | 48 | Explícito | Estradas da Grécia | Apenas 2-opt |
| `brazil58.tsp` | 58 | UPPER_ROW | Cidades brasileiras | Apenas 2-opt |
| `a280.tsp` | 280 | EUC_2D | Problema de perfuração | Apenas 2-opt |

As instâncias de benchmark são originadas da [TSPLIB](http://comopt.ifi.uni-heidelberg.de/software/TSPLIB95/), a biblioteca de referência para benchmarks de TSP.

---

## 🚀 Como Rodar

### Pré-requisitos

- **Python 3.10 ou superior** (type hints com `set[int]` exigem 3.9+)
- Sem dependências externas — apenas a biblioteca padrão do Python

### Instalação

```bash
# Clone o repositório
git clone https://github.com/seu-usuario/seu-repositorio.git
cd seu-repositorio/tsp
```

### Execução

```bash
python main.py <caminho-para-arquivo.tsp>
```

### Exemplos

```bash
# Instância pequena — roda os 3 métodos e mostra o gap de otimalidade
python main.py instances/test4.tsp

# Instância de 8 cidades — ainda roda força bruta e branch and bound
python main.py instances/test8.tsp

# Instância maior — roda apenas o 2-opt
python main.py instances/bayg29.tsp

# Instância grande — apenas 2-opt (280 cidades)
python main.py instances/a280.tsp
```

### Usando um arquivo .tsp personalizado

O programa aceita qualquer arquivo `.tsp` válido no formato TSPLIB. Basta fornecer o caminho completo:

```bash
python main.py /caminho/para/minha_instancia.tsp
```

---

## 🖥️ Exemplos de Saída

### `test4.tsp` (4 cidades)

```
Grafo carregado de: instances/test4.tsp
Cidades: 4

=== Brute Force ===
Rota: C0 -> C1 -> C2 -> C3 -> C0
Custo: 40.00
Permutações completas avaliadas: 6
Nós explorados: 16

=== Branch and Bound ===
Rota: C0 -> C1 -> C2 -> C3 -> C0
Custo: 40.00
Soluções completas avaliadas: 1
Nós explorados: 7
Nós podados: 9

=== 2-opt ===
Rota: C0 -> C1 -> C2 -> C3 -> C0
Custo: 40.00
Soluções candidatas avaliadas: 4
Iterações: 2

Gap da heuristica em relacao ao otimo: 0.00%
Qualidade da heuristica: 100.00% do otimo
```

### `bayg29.tsp` (29 cidades — apenas 2-opt)

```
Grafo carregado de: instances/bayg29.tsp
Cidades: 29
Pulando brute force: instância com 29 cidades é grande demais para exaustão
Pulando branch and bound: instância com 29 cidades pode demorar muito

=== 2-opt ===
Rota: C0 -> C5 -> C21 -> ...
Custo: 1789.00
Soluções candidatas avaliadas: 3240
Iterações: 5
```

---

## 📄 Formato dos Arquivos .tsp

O projeto segue o formato **TSPLIB**. Campos suportados:

```
NAME : nome_da_instancia
TYPE : TSP
DIMENSION : <número de cidades>
EDGE_WEIGHT_TYPE : EUC_2D | CEIL_2D | ATT | EXPLICIT
EDGE_WEIGHT_FORMAT : FULL_MATRIX | UPPER_ROW | UPPER_DIAG_ROW | LOWER_ROW | LOWER_DIAG_ROW
NODE_COORD_SECTION
  <id> <x> <y>
  ...
EDGE_WEIGHT_SECTION
  <valores da matriz>
EOF
```

**Exemplo mínimo com coordenadas (`EUC_2D`):**

```
NAME : exemplo
TYPE : TSP
DIMENSION : 3
EDGE_WEIGHT_TYPE : EUC_2D
NODE_COORD_SECTION
  1  0  0
  2  5  0
  3  2  4
EOF
```

As distâncias euclidianas são calculadas automaticamente a partir das coordenadas.
