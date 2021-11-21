from math import *
import numpy as np
from functions.b1_funcs import *

def mnl_K(IX, X, mprop, sigma_y, tapered, cross_section, ne, D, K):
    """
    material nonlinearity tangential stiffness matrix (K)

    input(s):
    X : topology matrix (element connection matrix)
    IX : nodal coordinates
    mprop : material properties
    sigma_y : yielding stress
    tapered: tapered beam (on/ff)
    cross_section: cross_section profile
    ne : number of elements
    D : global displacement vector
    K : initial tangential stiffness matrix
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
        if (le <= sigma_y / E):
            Et = E # tangential stiffness modulus
        else:
            Et = 0.4 * E / (E  * le / sigma_y)**0.6 # tangential stiffness modulus
        ke = A * Et * L0 * np.outer(B0, np.transpose(B0)) # local stiffness matrix
        # K assembly
        for ii in range(edof.shape[1]):
            for jj in range(edof.shape[1]):
                K[edof[0, ii], edof[0, jj]] = ke[ii, jj] + K[edof[0, ii], edof[0, jj]] 
        
    return K


def mnl_int_force(IX, X, mprop, sigma_y, tapered, cross_section, ne, D, R_int):
    """
    material nonlinearity internal force (R_int) for
    computing residual vector (R)
    R = R_int - R_ext

    input(s):
    X : topology matrix (element connection matrix)
    IX : nodal coordinates
    mprop : material properties
    sigma_y : yielding stress
    tapered: tapered beam (on/ff)
    cross_section: cross_section profile
    ne : number of elements
    D : global displacement vector
    R_int : internal force vector
    """
    for n in range(ne):
        [L0, edof, B0] = strn_displ_vec(IX, X, n)
        c = IX[n, 2]
        d = D[edof, 0] #local displacement vector
        le = np.matmul(np.transpose(B0), np.transpose(d)) # local strain
        E = mprop[c - 1, 0]
        if tapered == 'off':
            radius = mprop[c - 1, 1]
        else:
            radius = mprop[n, 1]
        if cross_section == 'circular':
            A = pi * radius**2 # cross-sectional area
        if (le <= sigma_y / E):
            ls = E * le # local stress
        else:
            ls = sigma_y * (E * le / sigma_y)**0.4 # local stress
        N = A * ls # nodal force
        # computing residual vector 
        re = B0 * N * L0  # local residual
        re = np.transpose(re)
        R_int[edof, 0] = re + R_int[edof, 0]
    
    return R_int