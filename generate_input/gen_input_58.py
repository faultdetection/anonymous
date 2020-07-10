import os
import numpy as np

curr_dir_path = os.path.dirname(os.path.realpath(__file__))
INP_DIR = os.path.join(curr_dir_path, '../Data/ProgramData_INPUT')

prog_id = '58' # if input is a valid variable name

if not os.path.exists(os.path.join(INP_DIR, prog_id)):
    os.mkdir(os.path.join(INP_DIR, prog_id))

for i in range(1, 100+1):
    inp_path = os.path.join(INP_DIR, prog_id, '{}.txt'.format(i))
    with open(inp_path, 'w') as f:
        inp_n = np.random.randint(1, 5, size=1)[0]
        f.write(f'{inp_n}\n')
        for _ in range(inp_n):
            inp_s = np.random.choice([ord('_')]*50+list(range(ord('a'), ord('z')+1))+list(range(ord('A'), ord('Z')+1))+list(range(ord('0'), ord('9')+1)), size=np.random.randint(1, 25, size=1)[0])
            f.write('{}\n'.format(''.join(list(map(chr, inp_s)))))
