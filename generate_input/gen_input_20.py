import os
import numpy as np

curr_dir_path = os.path.dirname(os.path.realpath(__file__))
INP_DIR = os.path.join(curr_dir_path, '../Data/ProgramData_INPUT')

prog_id = '20' # insert a string1 to another string2 based on alphabet order.

if not os.path.exists(os.path.join(INP_DIR, prog_id)):
    os.mkdir(os.path.join(INP_DIR, prog_id))

for i in range(1, 100+1):
    inp_path = os.path.join(INP_DIR, prog_id, '{}.txt'.format(i))
    with open(inp_path, 'w') as f:
        inp_str1 = np.random.choice(list(range(65, 91))+list(range(97, 123)), size=np.random.randint(1, 20, size=1)[0], replace=True)
        inp_str1 = [chr(inp_i) for inp_i in inp_str1]
        inp_str2 = np.random.choice(list(range(65, 91))+list(range(97, 123)), size=np.random.randint(1, 20, size=1)[0], replace=True)
        inp_str2 = [chr(inp_i) for inp_i in inp_str2]
        inp_str1 = ''.join(inp_str1)
        inp_str2 = ''.join(inp_str2)
        f.write('{}\n'.format(inp_str1))
        f.write('{}\n'.format(inp_str2))
