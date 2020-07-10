import os
import numpy as np

curr_dir_path = os.path.dirname(os.path.realpath(__file__))
INP_DIR = os.path.join(curr_dir_path, '../Data/ProgramData_INPUT')

prog_id = '95' # compare two input strings >, <, =

if not os.path.exists(os.path.join(INP_DIR, prog_id)):
    os.mkdir(os.path.join(INP_DIR, prog_id))

for i in range(1, 100+1):
    inp_path = os.path.join(INP_DIR, prog_id, '{}.txt'.format(i))
    with open(inp_path, 'w') as f:
        inp_s1 = np.random.choice(list(range(ord('A'), ord('Z')+1))+list(range(ord('a'), ord('z')+1))+list(range(ord('0'), ord('9')+1)), size=np.random.randint(1, 50, size=1)[0])
        inp_s1 = ''.join(list(map(chr, inp_s1)))
        inp_s2 = np.random.choice(list(range(ord('A'), ord('Z')+1))+list(range(ord('a'), ord('z')+1))+list(range(ord('0'), ord('9')+1)), size=np.random.randint(1, 50, size=1)[0])
        inp_s2 = ''.join(list(map(chr, inp_s2)))
        f.write('{}\n{}\n'.format(inp_s1, inp_s2))
