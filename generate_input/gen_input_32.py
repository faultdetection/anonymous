import os
import numpy as np

curr_dir_path = os.path.dirname(os.path.realpath(__file__))
INP_DIR = os.path.join(curr_dir_path, '../Data/ProgramData_INPUT')

prog_id = '32'

if not os.path.exists(os.path.join(INP_DIR, prog_id)):
    os.mkdir(os.path.join(INP_DIR, prog_id))

for i in range(1, 100+1):
    inp_path = os.path.join(INP_DIR, prog_id, '{}.txt'.format(i))
    with open(inp_path, 'w') as f:
        inp_n = np.random.randint(1, 9, size=1)[0]
        f.write('{}\n'.format(inp_n))
        for _ in range(inp_n):
            inp1 = np.random.choice(list(range(10)), size=np.random.randint(1, 100, size=1)[0], replace=True)
            inp1 = ''.join([str(inp) for inp in inp1])
            inp2 = np.random.choice(list(range(10)), size=np.random.randint(1, 100, size=1)[0], replace=True)
            inp2 = ''.join([str(inp) for inp in inp2])
            f.write('{}\n{}\n'.format(inp1, inp2))
