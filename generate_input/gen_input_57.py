import os
import numpy as np

curr_dir_path = os.path.dirname(os.path.realpath(__file__))
INP_DIR = os.path.join(curr_dir_path, '../Data/ProgramData_INPUT')

prog_id = '57' # remove postfix of input strings

if not os.path.exists(os.path.join(INP_DIR, prog_id)):
    os.mkdir(os.path.join(INP_DIR, prog_id))

for i in range(1, 100+1):
    inp_path = os.path.join(INP_DIR, prog_id, '{}.txt'.format(i))
    with open(inp_path, 'w') as f:
        inp_n = np.random.randint(1, 5, size=1)[0]
        f.write(f'{inp_n}\n')
        for _ in range(inp_n):
            inp_s = ''.join(np.random.choice(['a', 'A', '-'], size=np.random.randint(1, 20, size=1)[0]))
            inp_post = np.random.choice(['er', 'ing', 'ly', 'ee', 'int', 'li'], size=1)[0]
            f.write('{}\n'.format(inp_s+inp_post))
