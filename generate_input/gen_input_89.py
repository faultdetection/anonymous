import os
import numpy as np

curr_dir_path = os.path.dirname(os.path.realpath(__file__))
INP_DIR = os.path.join(curr_dir_path, '../Data/ProgramData_INPUT')

prog_id = '89' #

if not os.path.exists(os.path.join(INP_DIR, prog_id)):
    os.mkdir(os.path.join(INP_DIR, prog_id))

for i in range(1, 100+1):
    inp_path = os.path.join(INP_DIR, prog_id, '{}.txt'.format(i))
    with open(inp_path, 'w') as f:
        inp_n = np.random.randint(2, 20, size=1)[0]
        f.write('{}\n'.format(inp_n))
        inp_k = np.random.randint(0, inp_n, size=1)[0]
        inp_v1 = []
        for inp_i in range(2*inp_n):
            inp_v = np.random.randint(0, 50, size=1)[0]
            if inp_v != inp_k:
                inp_v1.append(inp_v)
        inp_v2 = [inp_k]*(inp_n-1)
        for inp_i in range(len(inp_v2), len(inp_v1)):
            inp_v = np.random.randint(0, 50, size=1)[0]
            if inp_v != inp_k:
                inp_v2.append(inp_v)
        np.random.shuffle(inp_v1)
        np.random.shuffle(inp_v2)
        for v1, v2 in zip(inp_v1, inp_v2):
            f.write('{} {}\n'.format(v1, v2))
        f.write('0 0\n')
