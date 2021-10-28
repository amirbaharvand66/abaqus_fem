# Coordinates of nodes,
X = [   [0.00,  0.00], 
        [0.25,  0.00], 
        [0.50,  0.00],
        [0.75,  0.00],
        [1.00,  0.00]   ]

# Topology matrix IX(node1,node2,propno),
IX = [  [1,  2,  1],
        [2,  3,  1],
        [3,  4,  1],
        [4,  5,  1] ]

# Control Parameters
cross_section = 'circular' # beam cross-section
tapered = 'off' # tapered beam(on/off)

# Element property matrix mprop = [ E radius ],
# The present code only supports circular beam cross-section
if tapered == 'off':
        mprop = [   [210e9, 30e-3]   ]
else:
        mprop = [   [210e9, 37.5e-3 / 2],
                    [210e9, 32.5e-3 / 2],
                    [210e9, 27.5e-3 / 2], 
                    [210e9, 22.5e-3 / 2], ]

# Plastic behavior
sigma_y = 200e6

# Prescribed loads mat(node,ldof,load)
# The present code only supports point loads
loads = [   [5,   1, 1.5 * -sigma_y]    ]
load_type = 'pressure'

# Boundary conditions mat(node,ldof,disp)   
# For 2d beam element, u, v, theta(rotation)
bound = [   [1,  1,  0.0]  ]

