import os
import numpy as np

curr_dir_path = os.path.dirname(os.path.realpath(__file__))
INP_DIR = os.path.join(curr_dir_path, '../Data/ProgramData_INPUT')

prog_id = '28' # input several strings (seperated by space), output length of each string

if not os.path.exists(os.path.join(INP_DIR, prog_id)):
    os.mkdir(os.path.join(INP_DIR, prog_id))

for i in range(1, 100+1):
    inp_path = os.path.join(INP_DIR, prog_id, '{}.txt'.format(i))
    with open(inp_path, 'w') as f:
        inp = np.random.choice([' ', 'a', '\\', '0'], size=np.random.randint(1, 20, size=1)[0], p=[0.4, 0.2, 0.2, 0.2])
        inp = ''.join(inp)
        f.write('{}\n'.format(inp))
