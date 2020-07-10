import os
import numpy as np

curr_dir_path = os.path.dirname(os.path.realpath(__file__))
INP_DIR = os.path.join(curr_dir_path, '../Data/ProgramData_INPUT')

prog_id = '72' # given a maxtrix, find the value that greater than all neighbours

if not os.path.exists(os.path.join(INP_DIR, prog_id)):
    os.mkdir(os.path.join(INP_DIR, prog_id))

for i in range(1, 100+1):
    inp_path = os.path.join(INP_DIR, prog_id, '{}.txt'.format(i))
    with open(inp_path, 'w') as f:
        inp_n = np.random.randint(1, 10, size=1)[0]
        inp_m = np.random.randint(1, 10, size=1)[0]
        f.write('{}\n{}\n'.format(inp_n, inp_m))
        for inp_i in range(inp_n):
            for inp_j in range(inp_m):
                f.write('{}\n'.format(np.random.randint(-10, 100, size=1)[0]))
