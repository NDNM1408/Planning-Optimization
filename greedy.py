
def assign_papers(N, M, b, reviewer_lists):
    from heapq import heappush, heappop, heapify


    reviewer_load = {i: 0 for i in range(1, M + 1)}

    paper_assignments = []


    for i in range(N):
        available_reviewers = reviewer_lists[i]

        reviewers_heap = []
        for reviewer in available_reviewers:
            heappush(reviewers_heap, (reviewer_load[reviewer], reviewer))
        
        assigned_reviewers = []

        for _ in range(b):
            if reviewers_heap:
                load, reviewer = heappop(reviewers_heap)
                assigned_reviewers.append(reviewer)
                reviewer_load[reviewer] += 1
        

        paper_assignments.append(assigned_reviewers)

    print(N)
    for assignment in paper_assignments:
        print(str(b) + ' ' + ' '.join(map(str, assignment)))


N, M, b = map(int, input().split())
reviewer_lists = []
for _ in range(N):
    k, *reviewers = map(int, input().split())
    reviewer_lists.append(reviewers)

assign_papers(N, M, b, reviewer_lists)
