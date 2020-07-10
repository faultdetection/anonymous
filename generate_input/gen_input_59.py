import os
import numpy as np

curr_dir_path = os.path.dirname(os.path.realpath(__file__))
INP_DIR = os.path.join(curr_dir_path, '../Data/ProgramData_INPUT')

prog_id = '59'

if not os.path.exists(os.path.join(INP_DIR, prog_id)):
    os.mkdir(os.path.join(INP_DIR, prog_id))

for i in range(1, 100+1):
    inp_path = os.path.join(INP_DIR, prog_id, '{}.txt'.format(i))
    with open(inp_path, 'w') as f:
        inp_n = np.random.randint(1, 5, size=1)[0]
        f.write('{}\n'.format(inp_n))
        for inp_i in range(inp_n):
            for inp_j in range(inp_n):
                inp_v = np.random.choice(['#', '@', '.', ',', 'a'], size=1, p=[0.2, 0.2, 0.2, 0.2, 0.2])[0]
                f.write('{}\n'.format(inp_v))
        if inp_n == 1:
            inp_m = 1
        else:
            inp_m = np.random.randint(1, inp_n, size=1)[0]
        f.write('{}\n'.format(inp_m))