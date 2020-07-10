import os
import numpy as np

curr_dir_path = os.path.dirname(os.path.realpath(__file__))
INP_DIR = os.path.join(curr_dir_path, '../Data/ProgramData_INPUT')

prog_id = '5'

if not os.path.exists(os.path.join(INP_DIR, prog_id)):
    os.mkdir(os.path.join(INP_DIR, prog_id))

for i in range(1, 100+1):
    inp_path = os.path.join(INP_DIR, prog_id, '{}.txt'.format(i))
    with open(inp_path, 'w') as f:
        inp_f = np.random.randint(0, 9) / 10.0
        inp_n = np.random.randint(1, 20, size=1)[0]
        inp_1 = np.random.choice(['A', 'T', 'C', 'G', 'X'], size=inp_n, replace=True, p=[0.24, 0.24, 0.24, 0.24, 0.04])

        inp_2 = []
        for inp_1_i in range(len(inp_1)):
            same_p = np.random.choice([0, 1], size=1, p=[0.13, 0.87])
            if same_p == 1:
                inp_2.append(inp_1[inp_1_i])
            else:
                inp_2.append(np.random.choice(['A', 'T', 'C', 'G', 'X'], size=1)[0])
        inp_1 = ''.join(inp_1)
        inp_2 = ''.join(inp_2)
        f.write('{}\n'.format(inp_f))
        f.write('{}\n'.format(inp_1))
        f.write('{}\n'.format(inp_2))
