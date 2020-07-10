import os
import numpy as np

curr_dir_path = os.path.dirname(os.path.realpath(__file__))
INP_DIR = os.path.join(curr_dir_path, '../Data/ProgramData_INPUT')

prog_id = '10' # given an array, count how many decrease. E.g., input=[2, 4, 3, 1], ans=2+1=3

if not os.path.exists(os.path.join(INP_DIR, prog_id)):
    os.mkdir(os.path.join(INP_DIR, prog_id))

for i in range(1, 100+1):
    inp_path = os.path.join(INP_DIR, prog_id, '{}.txt'.format(i))
    with open(inp_path, 'w') as f:
        inp_n = np.random.randint(1, 10, size=1)[0]
        f.write('{}\n'.format(inp_n))

        inp_arr = np.random.randint(-5, 5, size=inp_n)
        inp_arr = ' '.join(list(map(str, inp_arr)))
        f.write(f'{inp_arr}\n')
