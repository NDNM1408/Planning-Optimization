def bfs(capacity, source, sink, parent):
    visited = [False] * len(capacity)
    queue = [source]
    visited[source] = True

    while queue:
        u = queue.pop(0)

        for ind, val in enumerate(capacity[u]):
            if visited[ind] == False and val > 0:
                queue.append(ind)
                visited[ind] = True
                parent[ind] = u
                if ind == sink:
                    return True
    return False

def edmonds_karp(capacity, source, sink, num_papers, num_reviewers):
    size = len(capacity)
    parent = [-1] * size
    max_flow = 0
    residual = [row[:] for row in capacity]  
    
    while bfs(residual, source, sink, parent):
        path_flow = float('Inf')
        s = sink

        while s != source:
            path_flow = min(path_flow, residual[parent[s]][s])
            s = parent[s]

        v = sink
        while v != source:
            u = parent[v]
            residual[u][v] -= path_flow
            residual[v][u] += path_flow
            v = parent[v]

        max_flow += path_flow
    
    assignments = [[] for _ in range(num_papers)]
    if max_flow == num_papers * b:
        for i in range(1, num_papers + 1):
            for j in range(1, num_reviewers + 1):
                if capacity[i][num_papers + j] - residual[i][num_papers + j] > 0:
                    assignments[i-1].append(j)
    
    return max_flow, assignments


def can_assign(N, M, b, reviewer_lists, max_load):
    num_nodes = N + M + 2
    source = 0
    sink = num_nodes - 1

    capacity = [[0] * num_nodes for _ in range(num_nodes)]

    for i in range(1, N + 1):
        capacity[source][i] = b

    for i in range(1, N + 1):
        for reviewer in reviewer_lists[i - 1]:
            capacity[i][N + reviewer] = 1

    # Setup capacity from reviewers to sink
    for j in range(1, M + 1):
        capacity[N + j][sink] = max_load

    flow_value, _ = edmonds_karp(capacity, source, sink, N, M)
    return flow_value == N * b


def find_min_max_load(N, M, b, reviewer_lists):
    low, high = 1, 1000000000
    best_load = high

    while low <= high:
        mid = (low + high) // 2
        if can_assign(N, M, b, reviewer_lists, mid):
            best_load = mid
            high = mid - 1
        else:
            low = mid + 1

    return best_load

def assign_reviewers(N, M, b, reviewer_lists, max_load):
    num_nodes = N + M + 2
    source = 0
    sink = num_nodes - 1

    capacity = [[0] * num_nodes for _ in range(num_nodes)]

    for i in range(1, N + 1):
        capacity[source][i] = b

    for i in range(1, N + 1):
        for reviewer in reviewer_lists[i - 1]:
            capacity[i][N + reviewer] = 1

    for j in range(1, M + 1):
        capacity[N + j][sink] = max_load

    flow_value, assignments = edmonds_karp(capacity, source, sink, N, M)
    if flow_value == N * b:
        return assignments
    else:
        return []
    
N, M, b = map(int, input().split())
reviewer_lists = []
for _ in range(N):
    k, *reviewers = map(int, input().split())
    reviewer_lists.append(reviewers)

import time
start = time.time()
min_load = find_min_max_load(N, M, b, reviewer_lists)
assignments = assign_reviewers(N, M, b, reviewer_lists, min_load)
print("TIME ", time.time() - start)

print(N)
for i, assigned_reviewers in enumerate(assignments, 1):
    print(str(b) + ' ' + ' '.join(map(str,assigned_reviewers)))
