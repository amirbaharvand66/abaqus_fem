import math
import numpy as np
import matplotlib.pyplot as plt

def analytic_sol(IX, mprop, loads, sigma_y, L, cross_section, nl):
    '''Analytic solution
    input(s):
    E: young's modulus
    sigma_y: yieding stress
    mprop : material properties
    L = beam length
    cross_section: cross_section profile
    nl : number of point loads
    '''
    # extract data
    E = mprop[0, 0]
    radius = mprop[0, 1]
    if cross_section == 'circular':
            A = math.pi * radius**2 # cross-sectional area

    for ii in range(nl):
        p_max = loads[ii, 2]
        
    #initializing
    p = 0
    d = 0
    p_vec = []
    d_vec = []

    while p <= abs(p_max):
        d += 1e-4
        epsilon = d / L
        if epsilon <= sigma_y / E:
            sigma = E * epsilon
            p = sigma * A
        else:
            sigma = sigma_y * (E * epsilon / sigma_y)**0.4
            p = sigma * A
        d_vec.append(-d)
        p_vec.append(-p)

    plt.plot(d_vec, p_vec, label = "Analytical", linestyle = '-', marker = '*', color = 'black')

def abq_result(file_name:str, label:str, marker:str, color:str, n:int = None):
    '''Abaqus result for constant cross-section with r = 30e-3 m
    input(s):
    file_name: Abaqus .rpt file name
    label = plot label for legend
    linestyle = linestyle for plot
    marker = marker for plot
    color = plot color
    n: number of plastic point
    '''
    raw_data = np.genfromtxt(file_name)
    d_const = raw_data[1:, 0]
    p_const = raw_data[1:, 1]
    if n == None:
        plt.plot(d_const, p_const, label = label, \
        linestyle = '--', marker = marker, color = color)
    else:
        plt.plot(d_const, p_const, label = label  + str(n), \
        linestyle = '--', marker = marker, color = color)
