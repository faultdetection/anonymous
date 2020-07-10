import os
import numpy as np

curr_dir_path = os.path.dirname(os.path.realpath(__file__))
INP_DIR = os.path.join(curr_dir_path, '../Data/ProgramData_INPUT')

prog_id = '80' # calculate the number of days between two dates

if not os.path.exists(os.path.join(INP_DIR, prog_id)):
    os.mkdir(os.path.join(INP_DIR, prog_id))

for i in range(1, 100+1):
    inp_path = os.path.join(INP_DIR, prog_id, '{}.txt'.format(i))
    with open(inp_path, 'w') as f:
        inp_y1 = np.random.randint(1900, 2000, size=1)[0]
        inp_m1 = np.random.randint(1, 13, size=1)[0]
        inp_d1 = np.random.randint(1, 32, size=1)[0]
        inp_y2 = np.random.randint(inp_y1, 2020, size=1)[0]
        inp_m2 = np.random.randint(1, 13, size=1)[0]
        inp_d2 = np.random.randint(1, 32, size=1)[0]
        f.write('{} {} {}\n'.format(inp_y1, inp_m1, inp_d1))
        f.write('{} {} {}\n'.format(inp_y2, inp_m2, inp_d2))
