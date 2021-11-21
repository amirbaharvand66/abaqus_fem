from math import *
import numpy as np
import matplotlib.pyplot as plt

from functions.b1_funcs import *
from functions.mnb1is import *
from analytic_abq_sol import *
from functions.plot_funcs import *

def mnb1c(inc:int, max_itr:int, X, IX, mprop, loads, bound, sigma_y, tapered, load_type, cross_section, save_fig:str = 'off', epsilon:float = 1e-12):
    '''
    Material Nonlinearity Bar element one-dimensional Code

    Assumptions:
    - Due to only uniaxial loading, the beam element is reduced to a bar element.
    - The tapered beam is reduced to a beam with a constant cross-section over the x-axis.
    - Boundary conditions are furthered simplified by removing the displacement in y-direction.
    - The applied stress is replaced by its equivalent point load.
    - The effect of body force and traction are neglected and the numerical model only supports point loads.
    
    input(s):
    inc : number of increments
    max_itr: maximum iteration in each load increment
    X : topology matrix (element connection matrix)
    IX : nodal coordinates
    mprop : material properties
    loads : applied external load
    bound : boundary conditions
    sigma_y : yielding stress
    tapered: tapered beam (on/ff)
    cross_section: cross_section profile
    save_fig: save figure (on/off)
    epsilon: criterion for satisfying equilibrium
    '''

    # import beam data
    X = np.array(X)
    IX = np.array(IX)
    mprop = np.array(mprop)
    loads = np.array(loads)
    bound = np.array(bound)

    # revise the input file in case of applied loading 
    # is not at the end of the beam
    rp = int(loads[0, 0]) # revise point
    X = X[:rp]
    IX = IX[:rp - 1]

    # load type
    if load_type == 'pressure':
        if cross_section == 'circular':
            radius = mprop[0][1]
            loads[-1][-1] = loads[-1][-1] * (pi * radius**2)

    # required data
    neq = np.shape(X)[0] # number of equations (np.size(X)[0] * np.size(X)[1])
    ne = np.shape(IX)[0] # number of elements
    nb = np.shape(bound)[0] # number of boundary conditions
    nl = np.shape(loads)[0] # number of point loads

    # initials
    p = np.zeros((neq, 1)) # point load vector
    D = np.zeros((neq, 1)) # global displacement vector
    dD = np.zeros((neq, 1), dtype = 'd') # infinitesimal displacement vector
    R = np.zeros((neq, 1)) # internal force (residual vector)
    inc = inc # number of increments
    d_ = np.zeros((neq, inc)) # final displacement vector for plotting
    p_ = np.zeros((neq, inc)) # final force vector for plotting

    # plot tapered beam
    if tapered == 'on':
        fig = plt.subplots(figsize = (10, 8))
        plot_tapered(X, IX, mprop, save_fig)

    #analytical solution
    fig = plt.subplots(figsize = (12, 8))
    if tapered == 'off':
        analytic_sol(IX, mprop, loads, sigma_y, 1, cross_section, nl)

    # newton-raphson method (implicit)
    max_itr = max_itr # maximum iteration in NR method
    epsilon = epsilon # for accepting difference between the external force and residuals
    d_, p_, marker, label = mnb1is(X, IX, mprop, loads, bound, cross_section, sigma_y, tapered, neq, ne, nl, nb, p, D, dD, \
                                R, inc, d_, p_, 'NR', max_itr = max_itr, epsilon = epsilon)
    plt.plot(d_[rp - 1, :], p_[rp - 1, :], marker, label = label, markersize = 15)

    # modifield newton-raphson method (implicit)
    d_, p_, marker, label = mnb1is(X, IX, mprop, loads, bound, cross_section, sigma_y, tapered, neq, ne, nl, nb, p, D, dD, \
                                R, inc, d_, p_, 'MNR', max_itr = max_itr, epsilon = epsilon)
    plt.plot(d_[rp - 1, :], p_[rp - 1, :], marker, label = label, linestyle = '-.')

    #Abaqus result for constant cross-section with r = 30e-3 m
    if tapered == 'off':
        # 5 points for the definition of plastic behavior
        abq_result("rpt_files/abq_non_tapered_load_displ_5.rpt", "Non-tapered(Abaqus)", 'o', 'blue', 5) 
        # 50 points for the definition of plastic behavior
        abq_result("rpt_files/abq_non_tapered_load_displ_50.rpt", "Non-tapered(Abaqus)", '^', 'green', 50)
        plot_abq_result('Displacement in $x$-direction [m]', 'Applied load in $x$-direction [N]', tapered)
    else:
        # 5 points for the definition of plastic behavior - 2d tapered
        abq_result("rpt_files/abq_tapered_2d_load_displ_5.rpt", "Tapered 2d(Abaqus)", 'd', 'brown') 
        # 5 points for the definition of plastic behavior - 3d tapered
        abq_result("rpt_files/abq_tapered_3d_load_displ_5.rpt", "Tapered 3d(Abaqus)", '>', 'red')
        plot_abq_result('Displacement in $x$-direction [m]', 'Applied load in $x$-direction [N]', tapered)
    plt.show()