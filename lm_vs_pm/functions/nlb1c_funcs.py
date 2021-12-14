from math import *
import numpy as np
from functions.b1_funcs import *

def mnl_K(IX, X, mprop, tapered, cnst, cnst_type, cross_section, neq, ne, nc, D, K, epsilon_p):
    """
    material nonlinearity tangential stiffness matrix (K)

    input(s):
    X : topology matrix (element connection matrix)
    IX : nodal coordinates
    mprop : material properties
    tapered: tapered beam (on/ff)
    cnst : constraint for contact
    cnst_type : constraint enforcement method
    cross_section: cross_section profile
    neq : number of equations (= dof)
    ne : number of elements
    nc : number of constraints
    D : global displacement vector
    K : initial tangential stiffness matrix
    epsilon_p : penalty coefficient
    """
    for n in range(ne):
        [L0, edof, B0] = strn_displ_vec(IX, X, n)
        c = IX[n, 2]
        d = D[edof, 0] #local displacement vector
        le = np.matmul(np.transpose(B0), np.transpose(d))
        E = mprop[c - 1, 0]
        if tapered == 'off':
            radius = mprop[c - 1, 1]
        else:
            radius = mprop[n, 1]
        if cross_section == 'circular':
            A = pi * radius**2 # cross-sectional area
        ke = A * E * L0 * np.outer(B0, np.transpose(B0)) # local stiffness matrix
        # K assembly
        for ii in range(edof.shape[1]):
            for jj in range(edof.shape[1]):
                K[edof[0, ii], edof[0, jj]] = ke[ii, jj] + K[edof[0, ii], edof[0, jj]] 
    # contact
    for n in range(nc):
        cn = int(cnst[n, 0]) # contact node
        cdof = int(cnst[n, 1]) # contact dof
        coeff = cnst[n, 2] # contact node coefficient
        cv = -cnst[n, 3] # constraint value
        # Penalty Method
        C = np.zeros((1, neq))
        # Penalty
        if cnst_type == 'P':
            for n in range(nc):
                C[n, cn - 1] = coeff
            constraint = np.matmul(np.transpose(C), C) # C_transpose * C
            K = K + epsilon_p * constraint # K and constraint assembly
        # Lagrange Multipliers
        if cnst_type == 'LM':
            for n in range(nc):
                C[n, cn - 1] = coeff
            # K assembly for Lagrange Multiplier
            # [K, C_transpose
            #  C, 0         ]
            K[cn, :-1] = C[0, :]
            K[:-1, cn] = np.transpose(C[0, :])

    return K