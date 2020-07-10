import os
import subprocess
import multiprocessing
import argparse

curr_dir_path = os.path.dirname(os.path.realpath(__file__))
COM_DIR = os.path.join(curr_dir_path, '../Data/ProgramData_COM_INS')
INP_DIR = os.path.join(curr_dir_path, '../Data/ProgramData_INPUT')
OUT_DIR = os.path.join(curr_dir_path, '../Data/ProgramData_OUT_INS')
if not os.path.exists(OUT_DIR):
    os.mkdir(OUT_DIR)

def auto_run(inp_i):
    inp_path = os.path.join(INP_DIR, prog_id, '{}.txt'.format(inp_i))
    print('executing on input {}'.format(inp_i))
    for exe_file in os.listdir(os.path.join(COM_DIR, prog_id)):
        if '.txt.o' not in exe_file:
            continue
        exe_path = os.path.join(COM_DIR, prog_id, exe_file)
        out_path = os.path.join(OUT_DIR, prog_id, exe_file.replace('.txt.o', '_{}.txt'.format(inp_i)))
        # if os.path.exists(out_path):
            # continue
        # execute
        process = subprocess.Popen([exe_path], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        with open(inp_path, 'r') as inp_f:
            for line in inp_f.readlines():
                line = line.strip()
                if line == '':
                    continue
                try:
                    process.stdin.write((line + "\n").encode('utf-8'))
                except:
                    break
        try:
            output, errs = process.communicate(timeout=1)
        except subprocess.TimeoutExpired:
            process.kill()
            continue
            output, errs = process.communicate()
        try:
            output = output.decode('utf-8').strip()
        except:
            continue
        if len(output) > 10000000:
            continue
        with open(out_path, 'w') as out_f:
            out_f.write(output)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='...')
    parser.add_argument('-p', '--prog_id', type=int, required=True, help='problem_id')
    args = parser.parse_args()

    prog_id = str(args.prog_id)
    if not os.path.exists(OUT_DIR):
        os.mkdir(OUT_DIR)
    if not os.path.exists(os.path.join(OUT_DIR, prog_id)):
        os.mkdir(os.path.join(OUT_DIR, prog_id))
    
    inp_range = list(range(1, 100+1))
    pool = multiprocessing.Pool(5)
    pool.map(auto_run, inp_range)
