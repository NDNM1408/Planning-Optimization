import random

def hill_climbing(N, M, b, reviewer_lists):
    # Khởi tạo phân công ngẫu nhiên
    assignments = {i: random.sample(reviewer_lists[i], b) for i in range(N)}
    reviewer_loads = [0] * M

    # Tính tải trọng ban đầu
    for reviewers in assignments.values():
        for reviewer in reviewers:
            reviewer_loads[reviewer - 1] += 1

    def max_load():
        return max(reviewer_loads)

    # Hàm cải thiện lời giải
    def try_improve():
        nonlocal assignments, reviewer_loads
        for i in range(N):
            current_reviewers = assignments[i]
            current_max_load = max_load()
            for r in current_reviewers:
                potential_reviewers = [x for x in reviewer_lists[i] if x not in current_reviewers]
                for new_r in potential_reviewers:
                    # Thử thay thế nhà phê bình và tính toán tải trọng mới
                    new_reviewers = [new_r if x == r else x for x in current_reviewers]
                    temp_loads = reviewer_loads[:]
                    temp_loads[r - 1] -= 1
                    temp_loads[new_r - 1] += 1
                    new_max_load = max(temp_loads)

                    # Nếu cải thiện được tải trọng tối đa, cập nhật phân công
                    if new_max_load < current_max_load:
                        assignments[i] = new_reviewers
                        reviewer_loads = temp_loads
                        return True
        return False

    # Lặp cho đến khi không còn cải thiện
    while try_improve():
        pass

    # Xuất kết quả
    print(N)
    for reviewers in assignments.items():
        print(str(b) + ' ' + ' '.join(map(str, reviewers[1])))


N, M, b = map(int, input().split())
reviewer_lists = []
for _ in range(N):
    k, *reviewers = map(int, input().split())
    reviewer_lists.append(reviewers)

hill_climbing(N, M, b, reviewer_lists)
