import os
import numpy as np

curr_dir_path = os.path.dirname(os.path.realpath(__file__))
INP_DIR = os.path.join(curr_dir_path, '../Data/ProgramData_INPUT')

prog_id = '87' # input two time, calculate seconds between

if not os.path.exists(os.path.join(INP_DIR, prog_id)):
    os.mkdir(os.path.join(INP_DIR, prog_id))

for i in range(1, 100+1):
    inp_path = os.path.join(INP_DIR, prog_id, '{}.txt'.format(i))
    with open(inp_path, 'w') as f:
        inp_n = np.random.randint(1, 5, size=1)[0]
        for _ in range(inp_n):
            inp_h = np.random.randint(0, 25, size=1)[0]
            inp_m = np.random.randint(0, 61, size=1)[0]
            inp_s = np.random.randint(0, 61, size=1)[0]
            f.write(f'{inp_h} {inp_m} {inp_s} ')
            inp_h = np.random.randint(0, 25, size=1)[0]
            inp_m = np.random.randint(0, 61, size=1)[0]
            inp_s = np.random.randint(0, 61, size=1)[0]
            f.write(f'{inp_h} {inp_m} {inp_s}\n')
        f.write('0 0 0 0 0 0\n')
