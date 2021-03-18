

def element(index, A, B):
    i, j = index
    res = 0
    # get a middle dimension
    N = len(A[0]) or len(B)
    for k in range(N):
        res += A[i][k] * B[k][j]
    return res


matrix1 = [[1, 2], [3, 4]]
matrix2 = [[2, 0], [1, 2]]

print(element((1, 0), matrix1, matrix2))