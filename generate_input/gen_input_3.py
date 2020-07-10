import os
import numpy as np

curr_dir_path = os.path.dirname(os.path.realpath(__file__))
INP_DIR = os.path.join(curr_dir_path, '../Data/ProgramData_INPUT')

prog_id = '3'

if not os.path.exists(os.path.join(INP_DIR, prog_id)):
    os.mkdir(os.path.join(INP_DIR, prog_id))

for i in range(1, 100+1):
    inp_path = os.path.join(INP_DIR, prog_id, '{}.txt'.format(i))
    with open(inp_path, 'w') as f:
        inp_n = np.random.randint(1, 50, size=1)[0]
        inp_k = np.random.randint(-10000, 10000, size=1)[0]
        f.write('{}\n'.format(inp_n))
        f.write('{}\n'.format(inp_k))

        results = []
        for inp_i in range(inp_n):
            is_add = np.random.choice([0, 1], p=[0.975, 0.025])
            if is_add == 1 and inp_i >= 2:
                r = results[inp_i-1]+results[inp_i-2]
            else:
                r = np.random.randint(-10000, 10000, size=1)[0]
            results.append(r)
            f.write('{}\n'.format(r))
