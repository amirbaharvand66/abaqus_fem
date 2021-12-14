from math import *
import numpy as np
import matplotlib
from matplotlib import pyplot as plt
from matplotlib.lines import Line2D
       
def plot_def_udef_not_fancy(IX, X, D:list, ne:int, unit:str):
    """
    plot bar deformed and undeformed states wothout stress state
    (no compressive/tensile stress indicator)
    
    input(s):
    IX : nodal coordinates
    X : topology matrix (element connection matrix)
    D : global displacement vector
    ne : number of elements
    unit : x-axis unit
    """
    fig, ax = plt.subplots(figsize = (5, 5))
    label_list = []
    X = np.array(X)
    IX = np.array(IX)
    # initialize x, y
    x = np.zeros((1, X.shape[1]))
    y = np.zeros((1, X.shape[1]))
    for n in range(ne):
        # plot the undeformed state
        a = IX[n, 0]
        b = IX[n, 1]
        x = np.array([[ X[a - 1, 0], X[b - 1, 0] ]])
        y = np.array([[X[a - 1, 1], X[b - 1, 1] ]])
        plt.plot(x.T, y.T, marker = 'o', markersize = 7, color = 'k', label = 'Undeformed')
        # plot the deformed state
        x = x + np.array([[ D[a - 1, 0], D[b - 1, 0] ]])
        y = y + 0 # bar element
        plt.plot(x.T, y.T, marker = 's', color = 'r', linestyle = '--', label = 'Deformed state')
        plt.xlabel('x-axis' + '[' + unit + ']', font = 'Lucida Sans Unicode', fontsize = 15)
        plt.xticks(font = 'Lucida Sans Unicode', fontsize = 15)
        plt.tick_params(left = False, labelleft = False)
    
        handles, labels = ax.get_legend_handles_labels()
        for a_label in labels:
            if a_label not in label_list:
                label_list.append(a_label)
    plt.legend(label_list, prop={'size': 15})

def plot_rigid_wall(X, ne, cnst, h:float):
    '''plot rigid wall
    input(s):
    X : topology matrix (element connection matrix)
    ne : number of elements
    cnst : constraint for contact
    h : wall height
    zoom : zoom(on/off)
    '''
    X = np.array(X)
    x = X[ne, 0] - cnst[-1][-1]
    y = h/2
    plt.plot([x, x], [-y, y], color = 'k')
    plt.text(1.02 * x, -y/4, 'Rigid wall', rotation = 90, font = 'Lucida Sans Unicode', fontsize = 15)