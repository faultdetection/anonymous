import os
import numpy as np

curr_dir_path = os.path.dirname(os.path.realpath(__file__))
INP_DIR = os.path.join(curr_dir_path, '../Data/ProgramData_INPUT')

prog_id = '99' # given a list of ages, count percentage in each slots

if not os.path.exists(os.path.join(INP_DIR, prog_id)):
    os.mkdir(os.path.join(INP_DIR, prog_id))

for i in range(1, 100+1):
    inp_path = os.path.join(INP_DIR, prog_id, '{}.txt'.format(i))
    with open(inp_path, 'w') as f:
        inp_n = np.random.randint(1, 10, size=1)[0]
        f.write(f'{inp_n}\n')
        for _ in range(inp_n):
            inp_s1 = np.random.randint(0, 110, size=1)[0]
            f.write('{}\n'.format(inp_s1))
