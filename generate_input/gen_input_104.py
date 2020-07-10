import os
import numpy as np

curr_dir_path = os.path.dirname(os.path.realpath(__file__))
INP_DIR = os.path.join(curr_dir_path, '../Data/ProgramData_INPUT')

prog_id = '104'

if not os.path.exists(os.path.join(INP_DIR, prog_id)):
    os.mkdir(os.path.join(INP_DIR, prog_id))

for i in range(1, 100+1):
    inp_path = os.path.join(INP_DIR, prog_id, '{}.txt'.format(i))
    with open(inp_path, 'w') as f:
        zero_1 = np.random.choice([0, 1], size=1, p=[0.95, 0.05])
        if zero_1 == 1:
            inp_1 = 0
        else:
            inp_1 = np.random.randint(-200, 200, size=1)[0]
        
        zero_2 = np.random.choice([0, 1], size=1, p=[0.95, 0.05])
        if zero_2 == 1:
            inp_2 = 0
        else:
            inp_2 = np.random.randint(-200, 200, size=1)[0]

        f.write('{}\n'.format(inp_1))
        f.write('{}\n'.format(inp_2))
