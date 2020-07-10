import os
import numpy as np

curr_dir_path = os.path.dirname(os.path.realpath(__file__))
INP_DIR = os.path.join(curr_dir_path, '../Data/ProgramData_INPUT')

prog_id = '55' #

if not os.path.exists(os.path.join(INP_DIR, prog_id)):
    os.mkdir(os.path.join(INP_DIR, prog_id))

for i in range(1, 100+1):
    inp_path = os.path.join(INP_DIR, prog_id, '{}.txt'.format(i))
    with open(inp_path, 'w') as f:
        inp_n = np.random.randint(0, 20, size=1)[0]
        inp_m = np.random.randint(0, 20, size=1)[0]
        inp_s = np.random.choice(list(range(ord('a'), ord('z')+1))+list(range(ord('A'), ord('Z')+1))+list(range(ord('0'), ord('9')+1)), size=np.random.randint(1, 25, size=1)[0])
        inp_s = [chr(inp_i) for inp_i in inp_s]
        inp_s = ''.join(inp_s)
        f.write('{}\n{}\n{}\n'.format(inp_n, inp_s, inp_m))
