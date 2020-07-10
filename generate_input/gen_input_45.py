import os
import numpy as np

curr_dir_path = os.path.dirname(os.path.realpath(__file__))
INP_DIR = os.path.join(curr_dir_path, '../Data/ProgramData_INPUT')

prog_id = '45' # string index

if not os.path.exists(os.path.join(INP_DIR, prog_id)):
    os.mkdir(os.path.join(INP_DIR, prog_id))

for i in range(1, 100+1):
    inp_path = os.path.join(INP_DIR, prog_id, '{}.txt'.format(i))
    with open(inp_path, 'w') as f:
        inp_str1 = ''.join(np.random.choice(['a', 'A'], size=5, replace=True))
        inp_str2 = ''.join(np.random.choice(['a', 'A'], size=25, replace=True))
        f.write('{}\n{}\n'.format(inp_str1, inp_str2))
