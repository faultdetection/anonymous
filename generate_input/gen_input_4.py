import os
import numpy as np

curr_dir_path = os.path.dirname(os.path.realpath(__file__))
INP_DIR = os.path.join(curr_dir_path, '../Data/ProgramData_INPUT')

prog_id = '4'

if not os.path.exists(os.path.join(INP_DIR, prog_id)):
    os.mkdir(os.path.join(INP_DIR, prog_id))

for i in range(1, 100+1):
    inp_path = os.path.join(INP_DIR, prog_id, '{}.txt'.format(i))
    with open(inp_path, 'w') as f:
        inp_row = np.random.randint(1, 20, size=1)[0]
        inp_col = np.random.randint(1, 20, size=1)[0]
        f.write('{}\n'.format(inp_row))
        f.write('{}\n'.format(inp_col))
        for inp_i in range(inp_row):
            row_data = []
            for inp_j in range(inp_col):
                row_data.append(str(np.random.randint(-10000, 10000, size=1)[0]))
            row_data = ' '.join(row_data)
            f.write('{}\n'.format(row_data))
