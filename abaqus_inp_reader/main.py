from inp_reader.inp_reader import *
from plot_func.plotter_2d import *
from pre_processor import *

# read Abaqus .inp file
node, element, element_type, sketch_type = pre_processor('/inp_file/truss.inp')

