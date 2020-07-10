import os
import numpy as np

curr_dir_path = os.path.dirname(os.path.realpath(__file__))
INP_DIR = os.path.join(curr_dir_path, '../Data/ProgramData_INPUT')

prog_id = '31' # input a set of (name, sex, age, score, address)

if not os.path.exists(os.path.join(INP_DIR, prog_id)):
    os.mkdir(os.path.join(INP_DIR, prog_id))

for i in range(1, 100+1):
    inp_path = os.path.join(INP_DIR, prog_id, '{}.txt'.format(i))
    with open(inp_path, 'w') as f:
        inp_n = np.random.randint(1, 6, size=1)[0]
        for inp_i in range(1, inp_n):
            num = str(inp_i)
            name = ''.join(np.random.choice(['a', 'A', '1'], size=np.random.randint(1, 10, size=1)[0]))
            sex = np.random.choice(['m', 'f'], size=1)[0]
            age = np.random.randint(0, 100, size=1)[0]
            score = np.random.randint(0, 1000, size=1)[0] / 10.0
            address = ''.join(np.random.choice(['a', 'A', '1'], size=np.random.randint(1, 10, size=1)[0]))
            f.write(f'{inp_i}\n')
            f.write(f'{name} {sex} {age} {score} {address}\n')
        f.write('end\n')
