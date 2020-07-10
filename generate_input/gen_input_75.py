import os
import numpy as np

curr_dir_path = os.path.dirname(os.path.realpath(__file__))
INP_DIR = os.path.join(curr_dir_path, '../Data/ProgramData_INPUT')

prog_id = '75' #

if not os.path.exists(os.path.join(INP_DIR, prog_id)):
    os.mkdir(os.path.join(INP_DIR, prog_id))

for i in range(1, 100+1):
    inp_path = os.path.join(INP_DIR, prog_id, '{}.txt'.format(i))
    with open(inp_path, 'w') as f:
        inp_n = np.random.randint(-100, 100, size=np.random.randint(1, 25, size=1)[0])
        inp_m = np.random.randint(-100, 100, size=len(inp_n))
        f.write('{}\n'.format(','.join(list(map(str, inp_n)))))
        f.write('{}\n'.format(','.join(list(map(str, inp_m)))))
