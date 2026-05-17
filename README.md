🌎 Language / Idioma:  
[🇺🇸 English](README.md) | [🇧🇷 Português](README-ptBR.md)

---

# 🗺️ TSP — Comparing State Search Methods

A hands-on implementation and comparison of three approaches to solve the **Travelling Salesman Problem (TSP)**: brute force, branch and bound, and the 2-opt heuristic.

---

## 📋 Table of Contents

- [About](#about)
- [The Travelling Salesman Problem](#the-travelling-salesman-problem)
- [Implemented Methods](#implemented-methods)
  - [Brute Force](#1-brute-force)
  - [Branch and Bound](#2-branch-and-bound)
  - [2-opt Heuristic](#3-2-opt-heuristic)
- [Method Comparison](#method-comparison)
- [Project Structure](#project-structure)
- [Available Instances](#available-instances)
- [Getting Started](#getting-started)
- [Sample Output](#sample-output)
- [.tsp File Format](#tsp-file-format)

---

## About

This project implements and benchmarks three classic state-search strategies applied to the TSP. Each method is evaluated across three dimensions:

- 🎯 **Solution quality** — how close is the found route to the true optimum?
- ⚡ **Search efficiency** — how many nodes were explored, pruned, or iterated over?
- 📈 **Scalability** — at what problem size does each approach break down?

When an exact solution is available, the program also computes the **optimality gap** of the heuristic, giving a concrete measure of how much quality was traded for speed.

---

## 🧩 The Travelling Salesman Problem

Given a set of cities and the distances between every pair of them, the goal is to find the **shortest route that visits every city exactly once and returns to the starting city**.

Despite its simple formulation, TSP is **NP-hard**: the number of possible routes grows factorially with the number of cities. With `n` cities, there are `(n-1)!` permutations to consider — that's 362,880 routes for just 10 cities, and over 60 trillion for 20.

---

## ⚙️ Implemented Methods

### 1. Brute Force

**File:** `brute_force.py`

Explores **every possible permutation** of cities through a recursive depth-first search (DFS). Guarantees the global optimum, but has **O(n!)** complexity — making it impractical beyond ~11 cities.

**How it works:**

1. Fixes the starting city (node `start`).
2. Runs a DFS through all possible orderings of the remaining cities.
3. At each complete route, computes the total cost (including the return trip) and updates the best result if it's an improvement.
4. Returns the minimum-cost route along with exploration metrics.

**Reported metrics:**
- `permutacoes_completas` — total complete routes evaluated, equal to `(n-1)!`
- `explorados` — total nodes expanded in the search tree

**Complexity:** O(n!) time, O(n) space (recursion stack)

**Practical limit:** up to **11 cities** (set in `main.py`)

---

### 2. Branch and Bound

**File:** `branch_bound.py`

An upgrade over brute force that introduces **pruning**: whenever the lower bound of a partial path's cost already meets or exceeds the best known solution, that entire branch is discarded without being explored further.

**How it works:**

1. Also runs a recursive DFS starting from `start`.
2. Before expanding each node, computes a **lower bound** on the total cost of any route passing through that partial state. The bound is built from four components:
   - Accumulated cost so far
   - Cheapest edge connecting the current node to any unvisited city
   - **Minimum Spanning Tree (MST)** cost over all unvisited cities (computed with Prim's algorithm)
   - Cheapest edge connecting any unvisited city back to the origin
3. If `lower_bound >= best_known_cost`, the branch is **pruned**.
4. Candidates at each level are sorted by the cheapest edge from the current node — this favors finding good solutions early and makes pruning more effective.

**Reported metrics:**
- `tours_evaluated` — complete solutions found
- `explorados` — nodes actually expanded
- `podados` — branches discarded by pruning

**Complexity:** O(n!) worst case, but far less in practice due to pruning

**Practical limit:** up to **16 cities** (set in `main.py`)

---

### 3. 2-opt Heuristic

**File:** `two_opt.py`

Doesn't guarantee the optimal solution, but finds **high-quality routes in polynomial time** — applicable to large instances with hundreds or thousands of cities.

**How it works:**

1. **Initial construction:** builds a starting route using the **nearest neighbor** algorithm (`nearest_neighbor_initial_route`) — begins at `start` and always moves to the closest unvisited city.
2. **2-opt refinement:** iteratively tests all possible swaps of two route segments. A 2-opt swap removes two edges and reconnects the resulting segments in reverse order. If the new route is cheaper, it replaces the current one.
3. The loop terminates when no 2-opt swap improves the solution (local optimum reached).

**Reported metrics:**
- `tours_evaluated` — candidate routes evaluated during swaps
- `iterations` — full passes over all possible swaps until convergence

**Complexity:** O(n²) per iteration, O(n² × k) total, where `k` is the number of iterations until convergence

**No size limit:** runs on all instances, including a280 (280 cities)

---

## 📊 Method Comparison

| Criterion | Brute Force | Branch and Bound | 2-opt |
|---|---|---|---|
| **Optimal guarantee** | ✅ Yes | ✅ Yes | ❌ No (local optimum) |
| **Complexity** | O(n!) | O(n!) with pruning | O(n² × iter) |
| **Scalability** | Up to ~11 cities | Up to ~16 cities | No practical limit |
| **Speed** | Slow | Moderate | Very fast |
| **Lower bound** | Not used | MST + neighbors | N/A |
| **Strategy** | Exhaustive search | Exhaustive search with pruning | Iterative local search |

**When to use each:**

- 🔵 **Brute force** — tiny instances (up to ~11 cities) where the exact optimum is required and runtime is not a concern.
- 🟡 **Branch and bound** — small to medium instances (up to ~16 cities) where you still need the optimal solution but want significantly faster execution than brute force.
- 🟢 **2-opt** — large instances where speed matters. The solution may not be optimal, but the gap is usually small in practice.

---

## 🗂️ Project Structure

```
tsp/
├── main.py              # Entry point: loads the graph and runs all 3 methods
├── graph.py             # Graph class: parses .tsp files and computes distances
├── brute_force.py       # Method 1: exhaustive DFS brute force
├── branch_bound.py      # Method 2: branch and bound with MST-based lower bound
├── two_opt.py           # Method 3: 2-opt heuristic with nearest-neighbor initialization
└── instances/
    ├── test4.tsp        # 4 cities (square) — good for quick testing
    ├── test8.tsp        # 8 cities — runs all 3 methods
    ├── bayg29.tsp       # 29 cities (Bavaria) — 2-opt only
    ├── gr48.tsp         # 48 cities — 2-opt only
    ├── brazil58.tsp     # 58 Brazilian cities — 2-opt only
    └── a280.tsp         # 280 cities (drilling problem) — 2-opt only
```

### Module descriptions

**`graph.py` — `Graph` class**

Handles reading `.tsp` files and representing the graph as a distance matrix. Supported formats:

- `EDGE_WEIGHT_TYPE`: `EUC_2D`, `CEIL_2D`, `ATT` (computed from coordinates)
- `EDGE_WEIGHT_FORMAT`: `FULL_MATRIX`, `UPPER_ROW`, `UPPER_DIAG_ROW`, `LOWER_ROW`, `LOWER_DIAG_ROW` (explicit matrices)

**`main.py` — Orchestrator**

- Validates the command-line argument
- Loads the graph from the `.tsp` file
- Decides which methods to run based on instance size:
  - Brute force: only if `n ≤ 11`
  - Branch and bound: only if `n ≤ 16`
  - 2-opt: always
- Prints results for each method and computes the heuristic gap when the optimum is available

---

## 📦 Available Instances

| File | Cities | Format | Origin | Methods run |
|---|---|---|---|---|
| `test4.tsp` | 4 | EUC_2D | Custom | Brute Force + B&B + 2-opt |
| `test8.tsp` | 8 | EUC_2D | Custom | Brute Force + B&B + 2-opt |
| `bayg29.tsp` | 29 | UPPER_ROW | Bavaria, Germany | 2-opt only |
| `gr48.tsp` | 48 | Explicit | Greece Roads | 2-opt only |
| `brazil58.tsp` | 58 | UPPER_ROW | Brazilian cities | 2-opt only |
| `a280.tsp` | 280 | EUC_2D | Drilling problem | 2-opt only |

Benchmark instances are sourced from [TSPLIB](http://comopt.ifi.uni-heidelberg.de/software/TSPLIB95/), the standard reference library for TSP benchmarks.

---

## 🚀 Getting Started

### Prerequisites

- **Python 3.10 or higher** (`set[int]` type hints require 3.9+)
- No external dependencies — pure Python standard library

### Installation

```bash
# Clone the repository
git clone https://github.com/your-username/your-repo.git
cd your-repo/tsp
```

### Running

```bash
python main.py <path-to-file.tsp>
```

### Examples

```bash
# Small instance — runs all 3 methods and shows the optimality gap
python main.py instances/test4.tsp

# 8-city instance — still runs brute force and branch and bound
python main.py instances/test8.tsp

# Larger instance — runs 2-opt only
python main.py instances/bayg29.tsp

# Large instance — 2-opt only (280 cities)
python main.py instances/a280.tsp
```

### Using a custom .tsp file

The program accepts any valid TSPLIB-formatted `.tsp` file. Just provide the full path:

```bash
python main.py /path/to/my_instance.tsp
```

---

## 🖥️ Sample Output

### `test4.tsp` (4 cities)

```
Graph loaded from: instances/test4.tsp
Cities: 4

=== Brute Force ===
Route: C0 -> C1 -> C2 -> C3 -> C0
Cost: 40.00
Complete permutations evaluated: 6
Nodes explored: 16

=== Branch and Bound ===
Route: C0 -> C1 -> C2 -> C3 -> C0
Cost: 40.00
Complete solutions evaluated: 1
Nodes explored: 7
Nodes pruned: 9

=== 2-opt ===
Route: C0 -> C1 -> C2 -> C3 -> C0
Cost: 40.00
Candidate routes evaluated: 4
Iterations: 2

Heuristic gap from optimum: 0.00%
Heuristic quality: 100.00% of optimum
```

### `bayg29.tsp` (29 cities — 2-opt only)

```
Graph loaded from: instances/bayg29.tsp
Cities: 29
Skipping brute force: instance with 29 cities is too large for exhaustive search
Skipping branch and bound: instance with 29 cities may take too long

=== 2-opt ===
Route: C0 -> C5 -> C21 -> ...
Cost: 1789.00
Candidate routes evaluated: 3240
Iterations: 5
```

---

## 📄 .tsp File Format

The project follows the **TSPLIB** format. Supported fields:

```
NAME : instance_name
TYPE : TSP
DIMENSION : <number of cities>
EDGE_WEIGHT_TYPE : EUC_2D | CEIL_2D | ATT | EXPLICIT
EDGE_WEIGHT_FORMAT : FULL_MATRIX | UPPER_ROW | UPPER_DIAG_ROW | LOWER_ROW | LOWER_DIAG_ROW
NODE_COORD_SECTION
  <id> <x> <y>
  ...
EDGE_WEIGHT_SECTION
  <matrix values>
EOF
```

**Minimal example with coordinates (`EUC_2D`):**

```
NAME : example
TYPE : TSP
DIMENSION : 3
EDGE_WEIGHT_TYPE : EUC_2D
NODE_COORD_SECTION
  1  0  0
  2  5  0
  3  2  4
EOF
```

Euclidean distances are computed automatically from the coordinates.
