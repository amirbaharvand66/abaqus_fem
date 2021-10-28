import numpy as np
import matplotlib.pyplot as plt

def plot_tapered(X, IX, mprop, save_fig):
    '''plot tapered beam'''
    for n in range(np.shape(mprop)[0]):
        x1 = X[n, 0]
        y1 = -mprop[n, 1]
        x2 = X[n, 0]
        y2 = mprop[n, 1]
        x3 = X[n + 1, 0]
        y3 = mprop[n, 1]
        x4 = X[n + 1, 0]
        y4 = -mprop[n, 1]
        plt.plot([x1, x2, x3, x4, x1], [y1, y2, y3, y4, y1], color = 'black')
        plt.xlabel('x', font = 'Lucida Sans Unicode', fontsize = 15)
        plt.ylabel('y', font = 'Lucida Sans Unicode', fontsize = 15)
        plt.xticks(font = 'Lucida Sans Unicode', fontsize = 15)
        plt.yticks(font = 'Lucida Sans Unicode', fontsize = 15)
        plt.axis('equal')
    if save_fig == 'on':
        plt.savefig("../figs/tapered_beam.eps", format="eps", dpi=1000)
    plt.show()


def plot_abq_result(xlabel, ylabel, tapered, save_fig = 'off'):
    '''plot Abaqus result

    input(s):
    xlabel: label for x-axis
    ylabel: label for y-axis
    tapered: tapered/non-tapered beam (on/ff)
    save_fig: save figure (on/off)
    '''
    plt.xlabel(xlabel, font = 'Lucida Sans Unicode', fontsize = 15)
    plt.ylabel(ylabel, font = 'Lucida Sans Unicode', fontsize = 15)
    plt.xticks(font = 'Lucida Sans Unicode', fontsize = 15)
    plt.yticks(font = 'Lucida Sans Unicode', fontsize = 15)
    plt.legend(loc = 'upper left', prop={'size': 15})
    if save_fig == 'on':
        if tapered == 'on':
            plt.savefig("../figs/comparison_tapered.eps", format="eps", dpi=1000)
        if tapered == 'off':
            plt.savefig("../figs/comparison_non_tapered.eps", format="eps", dpi=1000)