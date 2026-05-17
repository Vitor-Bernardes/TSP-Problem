from graph import Graph


def solve_tsp_bruteforce(graph: Graph, start: int = 0):
    if graph.n < 2:
        return {"route": [start, start], "cost": 0.0, "states": 1, "nodes": 1, "tours_evaluated": 1}

    cities = [i for i in range(graph.n) if i != start]

    best_cost = float("inf")
    best_route = []
    permutacoes_completas = 0
    explorados = 0

    def dfs(current: int, visited: set[int], route: list[int], cost: float):
        nonlocal permutacoes_completas, explorados, best_cost, best_route
        explorados += 1

        if len(visited) == graph.n:
            permutacoes_completas += 1
            total = cost + graph.distance(current, start)
            if total < best_cost:
                best_cost = total
                best_route = [*route, start]
            return

        for nxt in cities:
            if nxt not in visited:
                dfs(
                    nxt,
                    visited | {nxt},
                    [*route, nxt],
                    cost + graph.distance(current, nxt),
                )

    dfs(start, {start}, [start], 0.0)
    return {"route": best_route, "cost": best_cost, "permutacoes_completas": permutacoes_completas, "explorados": explorados}
