import numpy as np
from cholesky_decomposition import block_cholesky_decomposition

def test_block_cholesky_decomposition():
    iter_times = 10000
    for _ in range(iter_times):
        # Generate a random symmetric positive definite matrix
        A = np.random.rand(4, 4)
        L = np.dot(A, A.T)

        indices = np.arange(4)
        F = indices[:2]
        C = indices[2:]

        (B_T, W, B) = block_cholesky_decomposition(L, F, C)
        L_final = B_T @ W @ B
        print(f"Original matrix L:\n{L}")
        assert np.allclose(L, L_final), f"Test failed for indices F={F}, C={C}\nReconstructed matrix L_final:\n{L_final}"
        