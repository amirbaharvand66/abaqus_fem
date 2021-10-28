from library.element_lib import *

import matplotlib.pyplot as plt

def truss_plotter(node_list:list, element_list:str, element_type:str, sketch_type:str):
    '''This function plots truss
    node_list: list of nodes
    element_list: list of elements
    element_type: element type
    sketch_type: type of sketch (shell/wire/point)'''
    
    try:
        if element_type in element_lib['wire']:
            if sketch_type == '2d_truss':
                for element in element_list:
                    ni1 = element[1] # node index 1
                    ni2 = element[2] # node index 2
                    x1 = node_list[ni1 - 1][1]
                    y1 = node_list[ni1 - 1][2]
                    x2 = node_list[ni2 - 1][1]
                    y2 = node_list[ni2 - 1][2]
                    plt.plot([x1, x2], [y1, y2], color = 'black', linewidth = 1)
                plt.show()
    except:
        pass
    else:
        print('The element type is not of WIRE category. Choose plot function accordingly!')

def plane_plotter(node_list:list, element_list:str, element_type:str, sketch_type:str):
    '''This function plots plane problems
    node_list: list of nodes
    element_list: list of elements
    element_type: element type
    sketch_type: type of sketch (shell/wire/point)'''
    try: 
        if element_type in element_lib['shell']:
            if sketch_type == '2d_plane':
                for element in element_list:
                    ni1 = element[1] # node index 1
                    ni2 = element[2] # node index 2
                    ni3 = element[3] # node index 2
                    ni4 = element[4] # node index 2
                    x1 = node_list[ni1 - 1][1]
                    y1 = node_list[ni1 - 1][2]
                    x2 = node_list[ni2 - 1][1]
                    y2 = node_list[ni2 - 1][2]
                    x3 = node_list[ni3 - 1][1]
                    y3 = node_list[ni3 - 1][2]
                    x4 = node_list[ni4 - 1][1]
                    y4 = node_list[ni4 - 1][2]
                    plt.plot([x1, x2, x3, x4, x1], [y1, y2, y3, y4, y1], color = 'black', linewidth = 0.1)
                    plt.xlabel('x', font = 'Lucida Sans Unicode', fontsize = 15)
                    plt.ylabel('y', font = 'Lucida Sans Unicode', fontsize = 15)
                    
                plt.axis('equal')
                plt.show()
    except:
        pass
    else:
        print('The element type is not of SHELL category. Choose plot function accordingly!')