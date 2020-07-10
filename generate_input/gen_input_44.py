import os
import numpy as np

curr_dir_path = os.path.dirname(os.path.realpath(__file__))
INP_DIR = os.path.join(curr_dir_path, '../Data/ProgramData_INPUT')

prog_id = '44' # reverse 6 input integer numbers

if not os.path.exists(os.path.join(INP_DIR, prog_id)):
    os.mkdir(os.path.join(INP_DIR, prog_id))

for i in range(1, 100+1):
    inp_path = os.path.join(INP_DIR, prog_id, '{}.txt'.format(i))
    with open(inp_path, 'w') as f:
        inp_1 = np.random.randint(0, 500, size=1)[0]
        inp_2 = np.random.randint(-500, 0, size=1)[0]
        inp_3 = np.random.randint(0, 500, size=1)[0]
        inp_3 = ''.join(['0']*np.random.randint(1, 5, size=1)[0]) + str(inp_3)
        inp_4 = np.random.randint(0, 500, size=1)[0]
        inp_4 = '-' + ''.join(['0']*np.random.randint(1, 5, size=1)[0]) + str(inp_4)
        inp_5 = np.random.randint(0, 500, size=1)[0]
        inp_5 = str(inp_5) + ''.join(['0']*np.random.randint(1, 5, size=1)[0])
        inp_6 = np.random.randint(0, 500, size=1)[0]
        inp_6 = '-' + str(inp_6) + ''.join(['0']*np.random.randint(1, 5, size=1)[0])

        f.write('{}\n{}\n{}\n{}\n{}\n{}\n'.format(inp_1, inp_2, inp_3, inp_4, inp_5, inp_6))
