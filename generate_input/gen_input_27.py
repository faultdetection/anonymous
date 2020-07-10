import os
import numpy as np

curr_dir_path = os.path.dirname(os.path.realpath(__file__))
INP_DIR = os.path.join(curr_dir_path, '../Data/ProgramData_INPUT')

prog_id = '27' # input a set of tuples of size three, each is a (x,y,z) for an equation. Output the solutions.

if not os.path.exists(os.path.join(INP_DIR, prog_id)):
    os.mkdir(os.path.join(INP_DIR, prog_id))

for i in range(1, 100+1):
    inp_path = os.path.join(INP_DIR, prog_id, '{}.txt'.format(i))
    with open(inp_path, 'w') as f:
        inp_n = np.random.randint(1, 10, size=1)[0]
        f.write(f'{inp_n}\n')
        for _ in range(inp_n):
            inp_a = np.random.randint(0, 100, size=3)
            inp_a = inp_a / 10.0
            inp_a = ' '.join(list(map(str, inp_a)))
            f.write(f'{inp_a}\n')
