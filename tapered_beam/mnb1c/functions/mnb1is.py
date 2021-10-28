import numpy as np
import scipy as sp
from scipy.linalg import lu_factor, lu_solve
import matplotlib.pyplot as plt

from functions.b1_funcs import *
from functions.nlb1c_funcs import *

def mnb1is(X, IX, mprop, loads, bound, cross_section, sigma_y, tapered, neq, ne, nl, nb, p, D, dD, \
    R, inc, d_, p_, method, max_itr = 0, epsilon = 0):
    """
    FEM nonlinear
    Material Nonlinearity Beam Implicit Solvers (mnbsi) including:
    1. Newton-Raphson method (NR)
    2. Modified Newton-Raphson method (MNR)
    
    input(s):
    X : topology matrix (element connection matrix)
    IX : nodal coordinates
    mprop : material properties
    loads : applied external load
    bound : boundary conditions
    sigma_y : yielding stress
    tapered: tapered beam (on/ff)
    cross_section: cross_section profile
    neq : number of equations (= dof)
    ne : number of elements
    nl : number of point loads
    nb : number of boundary conditions
    p : point load vector
    D : global displacement vector
    dD : infinitesimal displacement vector
    R : internal force (residual vector)
    inc : number of increments
    d_ : final displacement vector for plotting
    p_ : final force vector for plotting
    max_itr : maximum iteration for each load increment in NR and MNR methods
    epsilon : required for acceptance criterion of residuals in NR and MNR methods
    method : method for solving problem
    """

    ###############################
    # 1. Newton-Raphson (NR) method
    ###############################
    if method == 'NR':
        label = 'Newton-Raphson Method' 
        marker = '-x'

        print('###############################')
        print('# Newton-Raphson (MNR) method #')
        print('###############################')
        print('Load Increment \t\t Iteration')
        print('************** \t\t *********')
        
        # build-up point load vector
        p = build_load_vec(loads, nl, p)
        dp = p / inc # creating load increment
        
        for l_inc in range(inc): # loop over l_inc (load increment)
            
            for eq_itr in range (max_itr):
                               
                # initializing
                K = np.zeros((neq, neq)) # tangential stiffness matrix (K) resets for each iteration in an increment
                R_int = np.zeros((neq, 1)) # internal force
                
                # computing R_int
                R_int = mnl_int_force(IX, X, mprop, sigma_y, tapered, cross_section, ne, D, R_int)
            
                # computing R = R_int - p
                R = R_int - (l_inc + 1) * dp
                
                # applying boundary conditions on R
                for ii in range(nb):
                    a = int(bound[ii, 0])
                    R[a - 1 , :] = 0
                    
                # strop iteration criterion
                if np.linalg.norm(R) <= epsilon * np.linalg.norm(p):
                    break
                
                # computing tangential stiffness matrix (K)
                K = mnl_K(IX, X, mprop, sigma_y, tapered, cross_section, ne, D, K)

                # applying the boundary conditions on K
                K = bnd_cnd_K(bound, nb, K)
                        
                # LU factorization
                (LUM, PM) = sp.linalg.lu_factor(K) # Lower Upper Matrix, Permutation Matrix
                
                # computing dD
                dD = sp.linalg.lu_solve((-LUM, PM), R) # -inv(UM) * (inv(LM) * R);
                D = D + dD

            # increment and iteration check
            if eq_itr + 1 >= max_itr:
                print("MAXIMUM NUMBER OF ITEARTION REACHED!!!")
                break

            # saving displacement and force
            d_[:, l_inc] = D[:, 0]
            p_[:, l_inc] = (l_inc + 1) * dp[:, 0]

            # monitor load increments and iteration
            print('{:d} \t\t\t {:d}'.format(l_inc, eq_itr))    
                
    
    # #########################################
    # # 2. Modified Newton-Raphson (MNR) method
    # #########################################
    if method == 'MNR':
        label = 'Modified Newton-Raphson Method'
        marker = '-s'
        
        print('########################################')
        print('# Modified Newton-Raphson (MNR) method #')
        print('########################################')
        print('Load Increment \t\t Iteration')
        print('************** \t\t *********')

        # build-up point load vector
        p = build_load_vec(loads, nl, p)
        dp = p / inc # creating load increment

        # initializing
        K = np.zeros((neq, neq)) # tangential stiffness matrix (K)
        
        for l_inc in range(inc): # loop over l_inc (load increment)
            
            # computing tangential stiffness matrix (K)
            K = mnl_K(IX, X, mprop, sigma_y, tapered, cross_section, ne, D, K)

            # applying the boundary conditions on K
            K = bnd_cnd_K(bound, nb, K)
                    
            # LU factorization
            (LUM, PM) = sp.linalg.lu_factor(K) # Lower Upper Matrix, Permutation Matrix
            
            for eq_itr in range (max_itr):

                # reset tangential stiffness matrix (K) for each iteration in an increment
                K = np.zeros((neq, neq)) 
                R_int = np.zeros((neq, 1)) # internal force
                
                # computing R_int
                R_int = mnl_int_force(IX, X, mprop, sigma_y, tapered, cross_section, ne, D, R_int)
            
                # computing R = R_int - p
                R = R_int - (l_inc + 1) * dp
                
                # applying boundary conditions on R
                for ii in range(nb):
                    a = int(bound[ii, 0])
                    R[a - 1 , :] = 0
                    
                # strop iteration criterion
                if np.linalg.norm(R) <= epsilon * np.linalg.norm(p):
                    break
                    
                # computing dD
                dD = sp.linalg.lu_solve((-LUM, PM), R) # -inv(UM) * (inv(LM) * R);
                D = D + dD
            
            # increment and iteration check
            if eq_itr + 1 >= max_itr:
                print("MAXIMUM NUMBER OF ITEARTION REACHED!!!")
                break
            
            # saving displacement and force
            d_[:, l_inc] = D[:, 0]
            p_[:, l_inc] = (l_inc + 1) * dp[:, 0] 

            # monitor load increments and iteration
            print('{:d} \t\t\t {:d}'.format(l_inc, eq_itr)) 
                       
    
    return d_, p_, marker, label