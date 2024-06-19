from itertools import combinations

def branch_and_bound(N, M, b, reviewer_lists):
    # Sắp xếp các bài báo theo số lượng nhà phê bình có thể (tăng dần)
    papers = sorted(range(N), key=lambda x: len(reviewer_lists[x]))
    best_load = float('inf')
    best_assignment = [None] * N
    
    def dfs(paper_index, current_loads, current_assignment):
        nonlocal best_load, best_assignment
        
        # Cập nhật lời giải tốt nhất nếu tất cả các bài báo đã được xử lý
        if paper_index == N:
            max_load = max(current_loads)
            if max_load < best_load:
                best_load = max_load
                best_assignment = current_assignment[:]
            return
        
        paper = papers[paper_index]
        available_reviewers = reviewer_lists[paper]
        
        # Tạo các nhánh mới cho từng cách chọn b nhà phê bình
        for reviewers in combinations(available_reviewers, b):
            new_loads = current_loads[:]
            feasible = True
            
            for reviewer in reviewers:
                new_loads[reviewer - 1] += 1
                # Cắt nhánh nếu tải trọng vượt quá giới hạn tốt nhất hiện tại
                if new_loads[reviewer - 1] > best_load:
                    feasible = False
                    break
            
            if feasible:
                dfs(paper_index + 1, new_loads, current_assignment + [(paper, reviewers)])
    
    # Khởi tạo tải trọng nhà phê bình bằng 0
    initial_loads = [0] * M
    dfs(0, initial_loads, [])
    
    # Xuất kết quả tối ưu
    if best_load == float('inf'):
        print("No feasible solution.")
    else:
        print(N)
        for assignment in sorted(best_assignment, key=lambda x: x[0]):
            print(str(b) + ' ' + ' '.join(map(str, assignment[1])))

N, M, b = map(int, input().split())
reviewer_lists = []
for _ in range(N):
    k, *reviewers = map(int, input().split())
    reviewer_lists.append(reviewers)

branch_and_bound(N, M, b, reviewer_lists)
