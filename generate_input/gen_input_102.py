import os
import numpy as np

curr_dir_path = os.path.dirname(os.path.realpath(__file__))
INP_DIR = os.path.join(curr_dir_path, '../Data/ProgramData_INPUT')

prog_id = '102' # input a list of heights of males and females

if not os.path.exists(os.path.join(INP_DIR, prog_id)):
    os.mkdir(os.path.join(INP_DIR, prog_id))

for i in range(1, 100+1):
    inp_path = os.path.join(INP_DIR, prog_id, '{}.txt'.format(i))
    with open(inp_path, 'w') as f:
        inp_n = np.random.randint(1, 10, size=1)[0]
        f.write(f'{inp_n}\n')
        for _ in range(inp_n):
            s = np.random.choice(['m', 'f', 'n'], size=1, p=[0.45, 0.45, 0.1])[0]
            h = np.random.randint(100, 201, size=1)[0]
            f.write('{} {}\n'.format(s, h))
