import os
os.system('cls')
import numpy as np
import matplotlib.pyplot as plt

from inp_file.b01 import *
from lm_vs_pm import *

epsilon_p_list = np.linspace(1, 1e10, 10) # penalty coefficient
size = np.shape(epsilon_p_list)[0]
d_ = np.zeros(size) # displacement at free end of the beam

for epsilon_p in range(size):
    d, ne = lm_pm_func(X, IX, mprop, loads, bound, tapered, cross_section, epsilon_p_list[epsilon_p], 'P', cnst)
    d_[epsilon_p] = d[cnst[0][0] - 1]
print(d_ - 0.0001)
fig = plt.figure(figsize = (8.5, 5))
plt.plot(epsilon_p_list, d_ - 0.0001, 'o-k')
plt.xlabel('Penalty Coefficient', font = 'Lucida Sans Unicode', fontsize = 15)
plt.ylabel('Penetration[mm]', font = 'Lucida Sans Unicode', fontsize = 15)
plt.xticks(font = 'Lucida Sans Unicode', fontsize = 15)
plt.yticks(font = 'Lucida Sans Unicode', fontsize = 15)
# plt.savefig("penalty.eps", format="eps", dpi=1000)

# Lagrage Multiplier
# d_ = lm_pm_func(X, IX, mprop, loads, bound, tapered, cross_section, 1, 'P', cnst)

# plot deformed and undeformed configuration
plot_def_udef_not_fancy(IX, X, d, ne, 'm')
plot_rigid_wall(X, ne, cnst, 0.01)
# plt.savefig("penalty.png", format="png")
plt.show()