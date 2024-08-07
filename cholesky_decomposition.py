import numpy as np

# Nested Dissection Meets IPMs: Planar Min-Cost Flow in Nearly-Linear Time
# http://arxiv.org/abs/2205.01562
def schur_complement(L, F, C):
    """
    Computes the Schur complement of a symmetric matrix L with blocks indexed by F and C.
    Sc(L, C) = L_CC - L_CF * L_FF^-1 * L_FC

    Arguments:
    L: Symmetric matrix to decompose
    F: Index set F for block decomposition called `interior`
    C: Index set C for block decomposition called `boundary`

    Returns:
    Sc: Schur complement of L with respect to C
    """
    L_FF = L[np.ix_(F, F)]
    L_CF = L[np.ix_(C, F)]
    L_FC = L[np.ix_(F, C)]
    L_CC = L[np.ix_(C, C)]

    L_FF_inv = np.linalg.inv(L_FF)
    Sc = L_CC - L_CF @ L_FF_inv @ L_FC
    return Sc

# Nested Dissection Meets IPMs: Planar Min-Cost Flow in Nearly-Linear Time
# http://arxiv.org/abs/2205.01562
def block_cholesky_decomposition(L, F, C):
    """
    Perform block Cholesky decomposition on a symmetric matrix L with blocks indexed by F and C.

    Arguments:
    L: Symmetric matrix to decompose
    F: Index set F for block decomposition called `interior`
    C: Index set C for block decomposition called `boundary`

    Returns:
    (B_T, W, B): 3 block matrix which is the Cholesky decomposition of L
    """
    Sc = schur_complement(L, F, C)
    L_FF = L[np.ix_(F, F)]
    L_CF = L[np.ix_(C, F)]
    L_FF_inv = np.linalg.inv(L_FF)

    L_block = np.block([
        [L_FF, np.zeros((len(F), len(C)))],
        [np.zeros((len(F), len(C))), Sc]
    ])

    middle_matrix = np.block([
        [np.eye(len(F)), np.zeros((len(F), len(C)))],
        [L_CF @ L_FF_inv, np.eye(len(C))]
    ])

    return (middle_matrix, L_block, middle_matrix.T)

if __name__ == '__main__':
    L = np.array([[7.3, 1, 0, 0], [1, 20, 3.5, 0], [0, 3.5, 2, 0], [0, 0, 0, 1]])
    F = [0, 1]
    C = [2, 3]
    print('----- Matrix L: -----\n' + str(L) + '\n')
    (B_T, W, B) = block_cholesky_decomposition(L, F, C)
    print("Block Cholesky decomposition L:")
    print('----- Matrix B_T: -----\n' + str(B_T) + '\n')
    print('----- Matrix W: -----\n' + str(W) + '\n')
    print('----- Matrix B: -----\n' + str(B) + '\n')