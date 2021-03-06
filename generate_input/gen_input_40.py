import os
import numpy as np

curr_dir_path = os.path.dirname(os.path.realpath(__file__))
INP_DIR = os.path.join(curr_dir_path, '../Data/ProgramData_INPUT')

prog_id = '40' #

if not os.path.exists(os.path.join(INP_DIR, prog_id)):
    os.mkdir(os.path.join(INP_DIR, prog_id))

for i in range(1, 100+1):
    inp_path = os.path.join(INP_DIR, prog_id, '{}.txt'.format(i))
    with open(inp_path, 'w') as f:
        for _ in range(4):
            inp_n = np.random.randint(0, 1000, size=1)[0]/10.0
            f.write('{}\n'.format(inp_n))
        f.write('{}\n'.format(np.random.randint(0, 1800, size=1)[0]/10.0))
