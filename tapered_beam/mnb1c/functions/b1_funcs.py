from math import *
import numpy as np


def strn_displ_vec(IX, X, n:int):
    """
    calculating strain-displacement vector (B0)
    
    input(s):
    IX : nodal coordinates
    X : topology matrix (element connection matrix)
    n : element number
    
    output(s):
    L0 : initial elemnt length
    edof : element defree og freedom vector
    B0 : strain-displacement vector
    """
    a = IX[n, 0]
    b = IX[n, 1]
    dx = X[b - 1, 0] - X[a - 1, 0] # dx = xj - xi
    L0 = dx
    # element degree of freedom (dof)
    # Originally edof =  np.matrix([ [a, a + 1] ]) 
    # but Python starts from 0
    edof =  np.matrix([ [a - 1, a] ]) 
    B0 = (1 / L0 **2) * np.array([[dx], [-dx]])

    return L0, edof, B0


def bnd_cnd_K(bound, nb, K):
    """
    apply the boundary condition on K
    global stiffness matrix (linear)
    or 
    tangential stiffness matrix (nonlinear)

    inputs(s):
    bound : boundary condition(s) from input file
    nb : number of boundary conditions
    K : global / tangential stiffness matrix 
    """
    for ii in range(nb):
        a = int(bound[ii, 0])
        K[a - 1, :] = 0
        K[:, a - 1] = 0
        K[a - 1, a - 1] = 1

    return K

def build_load_vec(loads, nl, p):
    """
    build load vector

    input(s):
    loads : load(s) from input file
    nl : number of point loads
    p : point load vector
    """
    for ii in range(nl):
        a = int(loads[ii, 0])
        c = loads[ii, 2]
        p[a - 1] = c

    return p