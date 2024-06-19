import random

def generate_initial_solution(N, M, b, reviewer_lists):
    solution = {}
    for i in range(N):
        solution[i] = random.sample(reviewer_lists[i], b)
    return solution

def calculate_max_load(solution, M):
    loads = [0] * M
    for reviewers in solution.values():
        for reviewer in reviewers:
            loads[reviewer - 1] += 1
    return max(loads)

def generate_neighbors(solution, N, reviewer_lists, b):
    neighbors = []
    for i in range(N):
        for j in range(b):
            current_reviewer = solution[i][j]
            possible_replacements = [r for r in reviewer_lists[i] if r != current_reviewer]
            for new_reviewer in possible_replacements:
                new_solution = {k: v[:] for k, v in solution.items()}
                new_solution[i][j] = new_reviewer
                neighbors.append(new_solution)
    return neighbors

def tabu_search(N, M, b, reviewer_lists, max_iterations, tabu_size):
    # Generate initial solution
    current_solution = generate_initial_solution(N, M, b, reviewer_lists)
    best_solution = current_solution
    best_cost = calculate_max_load(current_solution, M)
    
    tabu_list = []
    
    for iteration in range(max_iterations):
        neighbors = generate_neighbors(current_solution, N, reviewer_lists, b)
        neighbors = [neighbor for neighbor in neighbors if neighbor not in tabu_list]
        
        # Evaluate neighbors
        best_neighbor = None
        best_neighbor_cost = float('inf')
        
        for neighbor in neighbors:
            cost = calculate_max_load(neighbor, M)
            if cost < best_neighbor_cost:
                best_neighbor = neighbor
                best_neighbor_cost = cost
        
        # Update current solution
        if best_neighbor and best_neighbor_cost < best_cost:
            current_solution = best_neighbor
            best_cost = best_neighbor_cost
            best_solution = best_neighbor
            if len(tabu_list) >= tabu_size:
                tabu_list.pop(0)
            tabu_list.append(current_solution)
        
        # No improvement
        if not best_neighbor:
            break
    
    return best_solution, best_cost

N, M, b = map(int, input().split())
reviewer_lists = []
for _ in range(N):
    k, *reviewers = map(int, input().split())
    reviewer_lists.append(reviewers)
max_iterations = 20
tabu_size = 10

solution, cost = tabu_search(N, M, b, reviewer_lists, max_iterations, tabu_size)
print(N)
for paper, reviewers in solution.items():
    print(str(b) + ' ' + ' '.join(map(str,reviewers)))
