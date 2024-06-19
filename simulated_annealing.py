import random
import math

def simulated_annealing(N, M, b, reviewer_lists):
    def initial_solution():
        return {i: random.sample(reviewer_lists[i], b) for i in range(N)}

    def calculate_max_load(assignments):
        loads = [0] * M
        for reviewers in assignments.values():
            for reviewer in reviewers:
                loads[reviewer - 1] += 1
        return max(loads)

    def neighbor(assignments):
        paper = random.choice(list(assignments.keys()))
        current_reviewers = assignments[paper]
        potential_reviewers = [r for r in reviewer_lists[paper] if r not in current_reviewers]
        if potential_reviewers:
            new_reviewer = random.choice(potential_reviewers)
            replaced_reviewer = random.choice(current_reviewers)
            new_reviewers = [new_reviewer if x == replaced_reviewer else x for x in current_reviewers]
            new_assignments = assignments.copy()
            new_assignments[paper] = new_reviewers
            return new_assignments
        return assignments

    def acceptance_probability(old_cost, new_cost, temperature):
        if new_cost < old_cost:
            return 1.0
        else:
            return math.exp((old_cost - new_cost) / temperature)

    current_solution = initial_solution()
    current_cost = calculate_max_load(current_solution)
    temperature = 1.0
    cooling_rate = 0.99
    minimum_temperature = 0.01

    while temperature > minimum_temperature:
        new_solution = neighbor(current_solution)
        new_cost = calculate_max_load(new_solution)
        if acceptance_probability(current_cost, new_cost, temperature) > random.random():
            current_solution = new_solution
            current_cost = new_cost

        temperature *= cooling_rate

    print(N)
    for reviewers in current_solution.items():
        print(str(b) + ' ' + ' '.join(map(str, reviewers[1])))

N, M, b = map(int, input().split())
reviewer_lists = []
for _ in range(N):
    k, *reviewers = map(int, input().split())
    reviewer_lists.append(reviewers)

simulated_annealing(N, M, b, reviewer_lists)
