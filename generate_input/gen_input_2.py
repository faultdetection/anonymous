import os
import numpy as np

curr_dir_path = os.path.dirname(os.path.realpath(__file__))
INP_DIR = os.path.join(curr_dir_path, '../Data/ProgramData_INPUT')

prog_id = '2'

if not os.path.exists(os.path.join(INP_DIR, prog_id)):
    os.mkdir(os.path.join(INP_DIR, prog_id))

for i in range(1, 100+1):
    inp_path = os.path.join(INP_DIR, prog_id, '{}.txt'.format(i))
    with open(inp_path, 'w') as f:
        inp_n = np.random.randint(1, 20, size=1)[0]

        f.write('{}\n'.format(inp_n))
        for _ in range(inp_n):
            num = np.random.randint(0, 10, size=1)[0]
            book_size = np.random.randint(1, 20, size=1)[0]
            book = np.random.randint(ord('A'), ord('Z'), size=book_size)
            book = ''.join([chr(book_i) for book_i in book])
            f.write('{} {}\n'.format(num, book))
