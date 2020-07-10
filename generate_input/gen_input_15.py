import os
import numpy as np

curr_dir_path = os.path.dirname(os.path.realpath(__file__))
INP_DIR = os.path.join(curr_dir_path, '../Data/ProgramData_INPUT')

prog_id = '15'

if not os.path.exists(os.path.join(INP_DIR, prog_id)):
    os.mkdir(os.path.join(INP_DIR, prog_id))

for i in range(1, 100+1):
    inp_path = os.path.join(INP_DIR, prog_id, '{}.txt'.format(i))
    with open(inp_path, 'w') as f:
        inp_n = np.random.randint(1, 50, size=1)[0]

        inp_matrix = np.random.randint(0, 256, size=(inp_n, inp_n))

        inp_zero_matrix_start = np.random.randint(0, inp_n, size=2)
        inp_zero_matrix_width = np.random.randint(1, 2*(inp_n-inp_zero_matrix_start[0]), size=1)[0]
        inp_zero_matrix_heigh = np.random.randint(1, 2*(inp_n-inp_zero_matrix_start[1]), size=1)[0]

        for w in range(inp_zero_matrix_width):
            for h in range(inp_zero_matrix_heigh):
                if inp_zero_matrix_start[0]+w < inp_n and inp_zero_matrix_start[1]+h < inp_n:
                    inp_matrix[inp_zero_matrix_start[0]+w][inp_zero_matrix_start[1]+h] = 0
        
        f.write('{}\n'.format(inp_n))
        for inp_i in range(inp_n):
            for inp_j in range(inp_n):
                f.write('{}\n'.format(inp_matrix[inp_i][inp_j]))
