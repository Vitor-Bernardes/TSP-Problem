from graph import Graph


def _mst_cost(graph: Graph, nodes: list[int]) -> float:
    if len(nodes) <= 1:
        return 0.0

    in_tree = {nodes[0]}
    out_tree = set(nodes[1:])
    total = 0.0

    while out_tree:
        best_v = None
        best_w = float("inf")

        for u in in_tree:
            for v in out_tree:
                w = graph.distance(u, v)
                if w < best_w:
                    best_w = w
                    best_v = v

        total += best_w
        in_tree.add(best_v)
        out_tree.remove(best_v)

    return total


def _lower_bound(graph: Graph, current: int, visited: set[int], current_cost: float, start: int) -> float:
    unvisited = [i for i in range(graph.n) if i not in visited]

    if not unvisited:
        return current_cost + graph.distance(current, start)

    connect_current = min(graph.distance(current, c) for c in unvisited)
    connect_start = min(graph.distance(c, start) for c in unvisited)
    mst = _mst_cost(graph, unvisited)

    return current_cost + connect_current + mst + connect_start


def solve_tsp_branch_and_bound(graph: Graph, start: int = 0):
    if graph.n < 2:
        return {"route": [start, start], "cost": 0.0, "visited_nodes": 1}

    best_cost = float("inf")
    best_route = []
    explorados = 0
    podados = 0
    tours_evaluated = 0

    def dfs(current: int, visited: set[int], route: list[int], cost: float):
        nonlocal best_cost, best_route, explorados, podados, tours_evaluated
        explorados += 1

        if len(visited) == graph.n:
            total = cost + graph.distance(current, start)
            tours_evaluated += 1
            if total < best_cost:
                best_cost = total
                best_route = [*route, start]
            return

        bound = _lower_bound(graph, current, visited, cost, start)
        if bound >= best_cost:
            podados += 1
            return

        candidates = [c for c in range(graph.n) if c not in visited]
        candidates.sort(key=lambda c: graph.distance(current, c))

        for nxt in candidates:
            dfs(
                nxt,
                visited | {nxt},
                [*route, nxt],
                cost + graph.distance(current, nxt),
            )

    dfs(start, {start}, [start], 0.0)

    return {"route": best_route, "cost": best_cost, "explorados": explorados, "podados": podados, "tours_evaluated": tours_evaluated}
