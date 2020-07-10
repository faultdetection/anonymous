import os
import numpy as np

curr_dir_path = os.path.dirname(os.path.realpath(__file__))
INP_DIR = os.path.join(curr_dir_path, '../Data/ProgramData_INPUT')

prog_id = '69'

if not os.path.exists(os.path.join(INP_DIR, prog_id)):
    os.mkdir(os.path.join(INP_DIR, prog_id))

for i in range(1, 100+1):
    inp_path = os.path.join(INP_DIR, prog_id, '{}.txt'.format(i))
    with open(inp_path, 'w') as f:
        inp1 = np.random.choice(list(range(10)), size=np.random.randint(1, 10, size=1)[0], replace=True, p=[0.55, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05])
        inp1 = ''.join([str(inp) for inp in inp1])
        neg_pos = np.random.choice([-1, 1], p=[0.8, 0.2])
        if neg_pos == -1:
            inp1 = '-' + inp1
        inp2 = np.random.choice(list(range(10)), size=np.random.randint(1, 10, size=1)[0], replace=True, p=[0.55, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05])
        inp2 = ''.join([str(inp) for inp in inp2])
        neg_pos = np.random.choice([-1, 1], p=[0.8, 0.2])
        if neg_pos == -1:
            inp2 = '-' + inp2
        f.write('{}\n{}\n'.format(inp1, inp2))
