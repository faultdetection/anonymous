import os
import numpy as np

curr_dir_path = os.path.dirname(os.path.realpath(__file__))
INP_DIR = os.path.join(curr_dir_path, '../Data/ProgramData_INPUT')

prog_id = '39' #input a set of (name, average, evaluate, a, b, amount)

if not os.path.exists(os.path.join(INP_DIR, prog_id)):
    os.mkdir(os.path.join(INP_DIR, prog_id))

for i in range(1, 100+1):
    inp_path = os.path.join(INP_DIR, prog_id, '{}.txt'.format(i))
    with open(inp_path, 'w') as f:
        inp_n = np.random.randint(1, 5, size=1)[0]
        f.write('{}\n'.format(inp_n))

        for _ in range(inp_n):
            inp_1 = ''.join(np.random.choice(['a', 'A', '1'], size=np.random.randint(1, 10, size=1)[0]))
            inp_2 = np.random.randint(0, 100, size=1)[0]
            inp_3 = np.random.randint(0, 100, size=1)[0]
            inp_4 = np.random.choice(['Y', 'N'], size=1)[0]
            inp_5 = np.random.choice(['Y', 'N'], size=1)[0]
            inp_6 = np.random.randint(-10, 10, size=1)[0]
            f.write('{} {} {} {} {} {}\n'.format(inp_1, inp_2, inp_3, inp_4, inp_5, inp_6))
