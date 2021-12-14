import numpy as np
import scipy as sp
from scipy.linalg import lu_factor, lu_solve

from functions.b1_funcs import *
from functions.nlb1c_funcs import *
from functions.plot_funcs import *
from functions.plots import *
from inp_file.b01 import *

def lm_pm_func(X, IX, mprop, loads, bound, tapered, cross_section, epsilon_p, cnst_type, cnst):
    '''
    Lagrange Multiplier vs Penalty method for contact mechanics 

    input(s):
    X : topology matrix (element connection matrix)
    IX : nodal coordinates
    mprop : material properties
    loads : applied external load
    bound : boundary conditions
    cross_section : beam cross-section
    tapered: tapered beam (on/off)
    epsilon_p = 1 # penalty coefficient
    cnst_type : constraint type - P for penalty/LM for Lagrange Multiplier
    cnst : constraint
    '''
    # import beam data
    X = np.array(X)
    IX = np.array(IX)
    mprop = np.array(mprop)
    loads = np.array(loads)
    bound = np.array(bound)
    cnst = np.array(cnst)

    # required data
    neq = np.shape(X)[0] # number of equations (np.size(X)[0] * np.size(X)[1])
    ne = np.shape(IX)[0] # number of elements
    nb = np.shape(bound)[0] # number of boundary conditions
    nl = np.shape(loads)[0] # number of point loads
    nc = np.shape(cnst)[0] # number of constraints

    # initials
    if cnst_type == 'LM': # lagrane multiplier
        p = np.zeros((neq + 1, 1)) # point load vector
        D = np.zeros((neq + 1, 1)) # global displacement vector
    else: # penalty Method
        p = np.zeros((neq, 1))
        D = np.zeros((neq, 1))

    # initializing
    if cnst_type == 'LM':
        K = np.zeros((neq + 1, neq + 1)) # tangential stiffness matrix (K) for lagrange multiplier
    else:
        K = np.zeros((neq, neq)) # tangential stiffness matrix (K) 

    # computing tangential stiffness matrix (K)
    K = mnl_K(IX, X, mprop, tapered, cnst, cnst_type, cross_section, neq, ne, nc, D, K, epsilon_p)

    # applying the boundary conditions on K
    K = bnd_cnd_K(bound, nb, K)

    # build-up point load vector
    p = build_contact_load_vec(X, loads, cnst, cnst_type, neq, nl, nc, p, epsilon_p)

    # LU factorization
    (LUM, PM) = sp.linalg.lu_factor(K) # Lower Upper Matrix, Permutation Matrix

    # computing dD
    D = sp.linalg.lu_solve((LUM, PM), p)

    return D, ne