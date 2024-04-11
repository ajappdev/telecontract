# Create your tests here.


def solution(A):
    # write your code in Python 3.6
    A.sort()
    A = list(dict.fromkeys(list(map(int, A))))
    expected_next = min(A)
    for a in A:
        if expected_next != a:
            if expected_next > 0:
                return int(expected_next)
            else:
                expected_next += 1
        else:
            expected_next += 1
    if expected_next < 0:
        return 1
    else:
        return int(expected_next)

A = [500.3, 356.9]
print(solution(A))

