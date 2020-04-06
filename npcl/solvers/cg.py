import pyopencl.array as cl_array
import numpy as np


def solve_cg(A, b, x_0, tol=np.float32(1e-3), max_iter=None, verbose=False):
    """
    Conjugate Gradient Method.

    This function solves the following problem:
        f(x) = 1/2*x^TAx - x^Tb.

    Inputs:
        A : a python function that computes Ax, i.e.,
            A(x) = Ax,
            for a vector (pyopencl.array.Array) x.
        b : (pyopencl.array.Array) represents the vector b.
        x_0 : (pyopencl.array.Array) represents the initial point x_0.
        tol : (np.float32) represents tolerence value.
        max_iter : (int) maximum number of iteration.

    Outputs:
        x : (pyopencl.array.Array) the solution x.
        k : (int) the total iteration number.
    """
    bnorm = cl_array.sum(b**2).get()
    r = b - A(x_0)
    p = r.copy()
    x = x_0.copy()
    dim = 1
    for d in x.shape:
        dim *= d
    rnorm = cl_array.sum(r**2)
    for k in range(dim):
        Ap = A(p)
        alpha = (rnorm/cl_array.sum(p*Ap)).get()
        x += alpha*p
        r_new = r - alpha*Ap
        rnorm_old = rnorm
        rnorm = cl_array.sum(r_new**2)
        if verbose is True:
            print('iteration number: ', k+1)
        if rnorm.get() < tol**2*bnorm:
            break
        if max_iter is not None:
            if k+1 == max_iter:
                break
        beta = (rnorm/rnorm_old).get()
        p = r_new + beta*p
        r = r_new.copy()
    return x, k