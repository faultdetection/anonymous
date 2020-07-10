import os
import numpy as np

curr_dir_path = os.path.dirname(os.path.realpath(__file__))
INP_DIR = os.path.join(curr_dir_path, '../Data/ProgramData_INPUT')

prog_id = '35' # 

if not os.path.exists(os.path.join(INP_DIR, prog_id)):
    os.mkdir(os.path.join(INP_DIR, prog_id))

for i in range(1, 100+1):
    inp_path = os.path.join(INP_DIR, prog_id, '{}.txt'.format(i))
    with open(inp_path, 'w') as f:
        inp_n1 = np.random.randint(1, 11, size=1)[0]
        inp_n2 = np.random.randint(1, 11, size=1)[0]
        f.write('{},{}\n'.format(inp_n1, inp_n2))
        for inp_i1 in range(inp_n1):
            for inp_i2 in range(inp_n2):
                f.write('{}\n'.format(np.random.randint(-10, 10, size=1)[0]))
