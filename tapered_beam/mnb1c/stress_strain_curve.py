import numpy as np
import matplotlib.pyplot as plt

E = 210e9
sigma_y = 200e6

def stress_strain_curve(E:int, sigma_y:int, max_stress:int, n:int, save_fig:str):
    '''plot the stress-strain curve
    
    input(s):
    E: young's modulus
    sigma_y: yielding stress
    max_stress: maximum stress
    n: number of steps
    save_fig: save figure in .eps format (on\off)
    '''
    sigma = np.linspace(0, max_stress, n)
    epsilon = np.zeros(np.size(sigma))
    for ii in range(len(sigma)):
        if sigma[ii] <= sigma_y:
            epsilon[ii] = sigma[ii] / E
        else:
            epsilon[ii] = sigma_y / E * (sigma[ii] / sigma_y)**(1/0.4) - epsilon[0]
        
    plt.plot(epsilon, sigma/1e6, color = 'black')
    plt.xlabel('$\epsilon$[-]', font = 'Lucida Sans Unicode', fontsize = 15)
    plt.ylabel('$\sigma$[MPa]', font = 'Lucida Sans Unicode', fontsize = 15)
    plt.xticks(font = 'Lucida Sans Unicode', fontsize = 15)
    plt.yticks(font = 'Lucida Sans Unicode', fontsize = 15)
    if save_fig == 'on':
        plt.savefig("stress_strain.eps", format="eps", dpi=1000)
    plt.show()

def plastic_prop(E:int, sigma_y:int, max_stress:int, n:int):
    '''plot the stress-strain curve
    
    input(s):
    E: young's modulus
    sigma_y: yielding stress
    max_stress: maximum stress
    n: number of steps
    '''
    sigma = np.linspace(sigma_y, max_stress, n)
    epsilon = np.zeros(np.size(sigma))
    print('{:.2}, {:}'.format(sigma_y, 0))
    for ii in range(len(sigma)):
        if sigma[ii] <= sigma_y:
            epsilon[ii] = sigma[ii] / E
        else:
            epsilon[ii] = sigma_y / E * (sigma[ii] / sigma_y)**(1/0.4) - epsilon[0]
            print('{:.2}, {:.5}'.format(sigma[ii], epsilon[ii]))


stress_strain_curve(E, sigma_y, 400e6, 10, 'off')
plastic_prop(E, sigma_y, 400e6, 5)