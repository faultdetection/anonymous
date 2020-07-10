import os
import numpy as np

curr_dir_path = os.path.dirname(os.path.realpath(__file__))
INP_DIR = os.path.join(curr_dir_path, '../Data/ProgramData_INPUT')

prog_id = '51' # given a vector of chars and a number, convert the vector into a matrix based on the number. Then output if each row of the matrix is the same

if not os.path.exists(os.path.join(INP_DIR, prog_id)):
    os.mkdir(os.path.join(INP_DIR, prog_id))

for i in range(1, 100+1):
    inp_path = os.path.join(INP_DIR, prog_id, '{}.txt'.format(i))
    with open(inp_path, 'w') as f:
        inp_n = np.random.randint(1, 7, size=1)[0]
        inp_v = ''.join(np.random.choice(['a', 'A'], size=np.random.randint(1, 30, size=1)[0], p=[0.9, 0.1]))
        f.write('{}\n'.format(inp_n))
        f.write('{}\n'.format(inp_v))
