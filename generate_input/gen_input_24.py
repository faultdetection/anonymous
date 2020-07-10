import os
import numpy as np

curr_dir_path = os.path.dirname(os.path.realpath(__file__))
INP_DIR = os.path.join(curr_dir_path, '../Data/ProgramData_INPUT')

prog_id = '24' # given a set of strings, output strings of the max length and mi length.

if not os.path.exists(os.path.join(INP_DIR, prog_id)):
    os.mkdir(os.path.join(INP_DIR, prog_id))

for i in range(1, 100+1):
    inp_path = os.path.join(INP_DIR, prog_id, '{}.txt'.format(i))
    with open(inp_path, 'w') as f:
        inp_n = np.random.randint(1, 10, size=1)[0]
        inp_strs = []
        for _ in range(inp_n):
            str1 = np.random.choice(list(range(65, 91))+list(range(97, 123)), size=np.random.randint(1, 20, size=1)[0], replace=True)
            str1 = [chr(inp_i) for inp_i in str1]
            str1 = ''.join(str1)
            inp_strs.append(str1)
        inp_strs = ' '.join(inp_strs)
        f.write(f'{inp_strs}\n')
