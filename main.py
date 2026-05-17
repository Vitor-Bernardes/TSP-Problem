import sys
from pathlib import Path

from branch_bound import solve_tsp_branch_and_bound
from brute_force import solve_tsp_bruteforce
from graph import Graph
from two_opt import solve_tsp_two_opt


def resolve_tsp_path(path_str: str) -> str:
    path = Path(path_str)
    if path.is_file() and path.suffix.lower() == '.tsp':
        return str(path)
    raise SystemExit(f'Entrada invalida: forneca um caminho para um arquivo .tsp existente')


def main():
    if len(sys.argv) < 2:
        raise SystemExit('Uso: python main.py <arquivo.tsp>')

    data_path = resolve_tsp_path(sys.argv[1])
    try:
        graph = Graph.from_tsp_file(data_path)
    except Exception:
        raise SystemExit('Entrada invalida: forneca um arquivo .tsp')
    print(f"Grafo carregado de: {data_path}")
    start = 0
    print(f"Cidades: {graph.n}")

    brute = None
    bnb = None
    if graph.n <= 11:
        brute = solve_tsp_bruteforce(graph, start=start)
    else:
        print(f'Pulando brute force: instância com {graph.n} cidades é grande demais para exaustão')

    if graph.n <= 16:
        bnb = solve_tsp_branch_and_bound(graph, start=start)
    else:
        print(f'Pulando branch and bound: instância com {graph.n} cidades pode demorar muito')

    heuristic = solve_tsp_two_opt(graph, start=start)

    for title, result in [
        ("Brute Force", brute),
        ("Branch and Bound", bnb),
        ("2-opt", heuristic),
    ]:
        if result is None:
            continue
        route = " -> ".join(graph.city_names[i] for i in result["route"])
        print(f"\n=== {title} ===")
        print(f"Rota: {route}")
        print(f"Custo: {result['cost']:.2f}")
        
        if title == "Brute Force":
            print(f"Permutações completas avaliadas: {result['permutacoes_completas']}")
            print(f"Nós explorados: {result['explorados']}")
        elif title == "Branch and Bound":
            print(f"Soluções completas avaliadas: {result['tours_evaluated']}")
            print(f"Nós explorados: {result['explorados']}")
            if brute is not None:
                podados = brute['explorados'] - result['explorados']
                print(f"Nós podados: {podados}")
            else:
                print(f"Nós podados: {result['podados']}")
        elif title == "2-opt":
            print(f"Soluções candidatas avaliadas: {result['tours_evaluated']}")
            print(f"Iterações: {result['iterations']}")

    if brute is not None and brute["cost"] > 0:
        gap = ((heuristic["cost"] - brute["cost"]) / brute["cost"]) * 100
        print(f"\nGap da heuristica em relacao ao otimo: {gap:.2f}%")
        print(f"Qualidade media da heuristica: {100 - gap:.2f}% do otimo")


if __name__ == "__main__":
    main()
