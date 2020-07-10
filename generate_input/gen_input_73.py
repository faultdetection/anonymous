import os
import numpy as np

curr_dir_path = os.path.dirname(os.path.realpath(__file__))
INP_DIR = os.path.join(curr_dir_path, '../Data/ProgramData_INPUT')

prog_id = '73' # given a matrix, find max values of each row while is the min of each column

if not os.path.exists(os.path.join(INP_DIR, prog_id)):
    os.mkdir(os.path.join(INP_DIR, prog_id))

for i in range(1, 100+1):
    inp_path = os.path.join(INP_DIR, prog_id, '{}.txt'.format(i))
    with open(inp_path, 'w') as f:
        row = np.random.randint(0, 5, size=1)[0]
        col = np.random.randint(0, 5, size=1)[0]
        val = np.random.randint(0, 100, size=1)[0]
        for inp_i in range(5):
            for inp_j in range(5):
                if inp_i == row and inp_j != col:
                    v = np.random.randint(-100, val, size=1)[0]
                elif inp_i != row and inp_j == col:
                    v = np.random.randint(val, 200, size=1)[0]
                elif inp_i == row and inp_j == col:
                    v = val
                else:
                    v = np.random.randint(-100, 200, size=1)[0]
                f.write('{}\n'.format(v))
