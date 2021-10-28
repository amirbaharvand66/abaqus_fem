from inp_reader.inp_reader import *
from plot_func.plotter_2d import *
from plot_func.plotter import *

def pre_processor(file_name):
    '''Pre-processor function
    file_name: name of the .inp file'''
    [node, element, element_type] = inp_reader(file_name)
    node = str2float(node, 'float')
    element = str2float(element, 'int')
    sketch_type = sketch_identifier(node, element_type)
    plotter(node, element, element_type, sketch_type)
    return node, element, element_type, sketch_type

