import numpy as np

from library.element_lib import *

def inp_reader(file_name:str):
    '''This function reads data from a Abaqus .inp file
    file_name: name of the .inp file'''

    import os
    file_path = os.getcwd()
    n = [] # nodes
    e = [] # element
    e_type = '' # element type
    tmp_str = ''
    assert os.path.getsize(file_path  + file_name) != 0, 'Empty .inp file'
    with open(file_path  + file_name) as truss_inp_file:
        for line in truss_inp_file:
            if '*' in line.strip():
                if line.strip() == '*Node':
                    tmp_str = 'NODE'
                    continue
                if '*Element, type' in line.strip():
                    # extract element type
                    tmp_e_type = line.strip().split('=')
                    e_type = tmp_e_type[-1]
                    tmp_str = 'ELEMENT'
                    continue
                else:
                    tmp_str = ''
                    continue
            
            if tmp_str == 'NODE':
                n.append(line.strip())
            elif tmp_str == 'ELEMENT':
                e.append(line.strip())
    return n, e, e_type

def str2float(list_of_str:list, data_type:str):
    '''This function converts list of strings to specified
    data type
    list_of_str: a list of numbers in string format
    data_type = type of data to convert to in string format'''

    x = []
    if data_type == 'int':
        for item in range(len(list_of_str)):
            tmp = list(map(int, list_of_str[item].split(',')))
            x.append(tmp)
    elif data_type == 'float':
        for item in range(len(list_of_str)):
            tmp = list(map(float, list_of_str[item].split(',')))
            x.append(tmp)
    return np.array(x)

def sketch_identifier(node:np.numarray, element_type:str):
    '''This function determine the sketch domain for plotting
    2d/3d
    node: node coordinates
    element_type: element type'''

    sketch_type = ''
    # 2d case
    if node.shape[1] == 3:
        if element_type in element_lib['wire']:
            sketch_type = '2d_truss'
        elif element_type in element_lib['shell']:
            sketch_type = '2d_plane'
    # 3d case
    return sketch_type
