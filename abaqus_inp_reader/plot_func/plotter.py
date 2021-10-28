from plot_func.plotter_2d import *

def plotter(node, element, element_type, sketch_type):
    '''Plooter function
    node_list: list of nodes
    element_list: list of elements
    element_type: element type
    sketch_type: type of sketch (shell/wire/point)'''
    if sketch_type == '2d_truss':
        # plot a truss
        truss_plotter(node, element, element_type, sketch_type)

    elif sketch_type == '2d_plane':
        # plot plane stress/plane strain/shell
        plane_plotter(node, element, element_type, sketch_type)