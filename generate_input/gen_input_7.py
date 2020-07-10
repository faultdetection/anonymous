import os
import numpy as np

curr_dir_path = os.path.dirname(os.path.realpath(__file__))
INP_DIR = os.path.join(curr_dir_path, '../Data/ProgramData_INPUT')

prog_id = '7'

if not os.path.exists(os.path.join(INP_DIR, prog_id)):
    os.mkdir(os.path.join(INP_DIR, prog_id))

for i in range(1, 100+1):
    inp_path = os.path.join(INP_DIR, prog_id, '{}.txt'.format(i))
    with open(inp_path, 'w') as f:
        inp_str1 = np.random.choice(list(range(65, 70)), size=np.random.randint(1, 20, size=1)[0], replace=True)

        sub_len = np.random.randint(1, max(min(len(inp_str1), 5), 2), size=1)[0]
        start_pos = np.random.randint(len(inp_str1), size=1)[0]
        inp_str2 = inp_str1[start_pos:start_pos+sub_len]

        inp_str3 = np.random.choice(list(range(65, 70)), size=np.random.randint(1, 2*sub_len, size=1)[0], replace=True)

        inp_str1 = [chr(i) for i in inp_str1]
        inp_str2 = [chr(i) for i in inp_str2]
        inp_str3 = [chr(i) for i in inp_str3]
        inp_str1 = ''.join(inp_str1)
        inp_str2 = ''.join(inp_str2)
        inp_str3 = ''.join(inp_str3)
        f.write('{}\n'.format(inp_str1))
        f.write('{}\n'.format(inp_str2))
        f.write('{}\n'.format(inp_str3))
