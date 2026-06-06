import numpy as np

TESTING = True

def reduce_matrix_mod2(M):
    """
    Not fully mathematically canonical, might break in complex use cases
    """
    if type(M) == int:
        return 0, 0

    rows, cols = np.shape(M)
    column_index = dict.fromkeys(range(rows), None)
    new_M = M.copy()
    rank = 0
    
    for j in range(cols):
        while True:
            col = new_M[:, j]
            pivot = np.where(col == 1)[0]
            if pivot.size == 0:
                break
            pivot = pivot[0]

            if column_index[pivot] is not None:
                new_M[:, j] = (new_M[:, column_index[pivot]] + col) % 2
            else:
                rank += 1
                column_index[pivot] = j
                break
    return new_M, rank


if __name__ == "__main__":
    if TESTING:
        M = np.array([[1,0], [1,0], [1,0], [1,0], [1,0]])
        print(reduce_matrix_mod2(M))