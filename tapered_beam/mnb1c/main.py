from numpy.core.numeric import cross
from inp_file.b01 import *
from mnb1c import *

mnb1c(11, 1000, X, IX, mprop, loads, bound, sigma_y, tapered, load_type, cross_section, 'off')