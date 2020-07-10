import os
import numpy as np

curr_dir_path = os.path.dirname(os.path.realpath(__file__))
INP_DIR = os.path.join(curr_dir_path, '../Data/ProgramData_INPUT')

prog_id = '81' # input a matrix and two numbers, exchange this two rows

if not os.path.exists(os.path.join(INP_DIR, prog_id)):
    os.mkdir(os.path.join(INP_DIR, prog_id))

for i in range(1, 100+1):
    inp_path = os.path.join(INP_DIR, prog_id, '{}.txt'.format(i))
    with open(inp_path, 'w') as f:
        for inp_i in range(5):
            for inp_j in range(5):
                f.write('{}\n'.format(np.random.randint(-100, 100, size=1)[0]))
        f.write('{}\n'.format(np.random.randint(1, 6, size=1)[0]))
        f.write('{}\n'.format(np.random.randint(1, 6, size=1)[0]))
