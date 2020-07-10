import os
import numpy as np

curr_dir_path = os.path.dirname(os.path.realpath(__file__))
INP_DIR = os.path.join(curr_dir_path, '../Data/ProgramData_INPUT')

prog_id = '8' # given two input arrays, sort then concat them.

if not os.path.exists(os.path.join(INP_DIR, prog_id)):
    os.mkdir(os.path.join(INP_DIR, prog_id))

for i in range(1, 100+1):
    inp_path = os.path.join(INP_DIR, prog_id, '{}.txt'.format(i))
    with open(inp_path, 'w') as f:
        inp_n = np.random.randint(0, 10, size=1)[0]
        inp_m = np.random.randint(0, 10, size=1)[0]
        f.write('{} {}\n'.format(inp_n, inp_m))

        inp_arr_1 = np.random.randint(-5, 5, size=inp_n) if inp_n != 0 else []
        inp_arr_1 = ' '.join(list(map(str, inp_arr_1)))
        inp_arr_2 = np.random.randint(-5, 5, size=inp_m) if inp_m != 0 else []
        inp_arr_2 = ' '.join(list(map(str, inp_arr_2)))
        
        f.write(f'{inp_arr_1}\n')
        f.write(f'{inp_arr_2}\n')
