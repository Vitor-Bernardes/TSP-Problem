from graph import Graph


def route_cost(graph: Graph, route):
    return sum(graph.distance(route[i], route[i + 1]) for i in range(len(route) - 1))


def nearest_neighbor_initial_route(graph: Graph, start: int = 0):
    unvisited = set(range(graph.n))
    unvisited.remove(start)

    route = [start]
    current = start

    while unvisited:
        nxt = min(unvisited, key=lambda c: graph.distance(current, c))
        route.append(nxt)
        unvisited.remove(nxt)
        current = nxt

    route.append(start)
    return route


def solve_tsp_two_opt(graph: Graph, start: int = 0):
    if graph.n < 2:
        return {"route": [start, start], "cost": 0.0, "iterations": 0}

    route = nearest_neighbor_initial_route(graph, start)
    iterations = 0
    tours_evaluated = 1

    while True:
        improved = False
        iterations += 1
        best_cost = route_cost(graph, route)

        for i in range(1, len(route) - 2):
            for j in range(i + 1, len(route) - 1):
                if j - i == 1:
                    continue

                new_route = route[:i] + route[i:j][::-1] + route[j:]
                new_cost = route_cost(graph, new_route)
                tours_evaluated += 1

                if new_cost < best_cost:
                    route = new_route
                    best_cost = new_cost
                    improved = True

        if not improved:
            break

    return {"route": route, "cost": route_cost(graph, route), "iterations": iterations, "nodes": iterations, "tours_evaluated": tours_evaluated}
