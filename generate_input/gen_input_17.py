import os
import numpy as np

curr_dir_path = os.path.dirname(os.path.realpath(__file__))
INP_DIR = os.path.join(curr_dir_path, '../Data/ProgramData_INPUT')

prog_id = '17' # parenthesis mathing

if not os.path.exists(os.path.join(INP_DIR, prog_id)):
    os.mkdir(os.path.join(INP_DIR, prog_id))

for i in range(1, 100+1):
    inp_path = os.path.join(INP_DIR, prog_id, '{}.txt'.format(i))
    with open(inp_path, 'w') as f:
        inp = np.random.choice(['(', ')', '$', '1', 'a'], size=np.random.randint(1, 20, size=1)[0], p=[0.4, 0.4, 0.1, 0.05, 0.05])
        inp = ''.join(inp)
        f.write('{}\n'.format(inp))
