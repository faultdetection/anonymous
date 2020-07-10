import os
import numpy as np

curr_dir_path = os.path.dirname(os.path.realpath(__file__))
INP_DIR = os.path.join(curr_dir_path, '../Data/ProgramData_INPUT')

prog_id = '46' # input a matrix

if not os.path.exists(os.path.join(INP_DIR, prog_id)):
    os.mkdir(os.path.join(INP_DIR, prog_id))

for i in range(1, 100+1):
    inp_path = os.path.join(INP_DIR, prog_id, '{}.txt'.format(i))
    with open(inp_path, 'w') as f:
        inp_row = np.random.randint(1, 10, size=1)[0]
        inp_col = np.random.randint(1, 10, size=1)[0]
        f.write('{}\n{}\n'.format(inp_row, inp_col))
        for row_i in range(inp_row):
            for col_i in range(inp_col):
                inp_v = np.random.randint(-10, 10, size=1)[0]
                f.write('{}\n'.format(inp_v))
