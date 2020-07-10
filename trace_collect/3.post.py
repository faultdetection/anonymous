from glob import glob
import os
import shutil
from tqdm import tqdm
import argparse

curr_dir_path = os.path.dirname(os.path.realpath(__file__))
OUT_VALUE_DIR = os.path.join(curr_dir_path, '../Data/ProgramData_OUT_INS')

def post():
    if not os.path.exists(os.path.join(OUT_VALUE_DIR, prog_id+'_new')):
        os.makedirs(os.path.join(OUT_VALUE_DIR, prog_id+'_new'))

    out_value_files = glob(os.path.join(OUT_VALUE_DIR, prog_id, '*.txt'))

    for f in out_value_files:
        if '_new' in f:
            os.rename(f, f.replace('_new', ''))

    for out_value_f in tqdm(out_value_files):
        out_value_f_new = out_value_f.replace(f'/{prog_id}/', f'/{prog_id}_new/')
        with open(out_value_f, 'r') as f, open(out_value_f_new, 'w') as f_new:
            line = f.readline()
            while line:
                if 'ChangedVar:' in line and line[:len('ChangedVar:')] != 'ChangedVar:':
                    new_line_1 = line[:line.find('ChangedVar:')]
                    new_line_2 = line[line.find('ChangedVar:'):]
                    f_new.write(new_line_1 + '\n')
                    f_new.write(new_line_2 + '\n')
                elif 'Return' in line and line[:len('Return')] != 'Return':
                    new_line_1 = line[:line.find('Return')]
                    new_line_2 = line[line.find('Return'):]
                    f_new.write(new_line_1 + '\n')
                    f_new.write(new_line_2 + '\n')
                elif 'ChangedVar:' in line and 'isFor:' not in line:
                    if 'Return' in line:
                        new_line_1 = line[:line.find('Return')]
                        new_line_2 = line[line.find('Return'):]
                        f_new.write(new_line_1 + '\n')
                        f_new.write(new_line_2 + '\n')
                    elif 'EnterFunction' in line:
                        second_line = f.readline()
                        if 'isFor:' not in second_line:
                            if 'EnterFunction:' not in line:
                                print('\n!ERROR!')
                                exit(1)
                            else:
                                third_line = f.readline()
                                # assert 'ChangedVar' not in third_line and 'isFor' in third_line
                                line_1 = line[:line.find('EnterFunction')]
                                line_2 = line[line.find('EnterFunction'):]
                                new_line_1 = line_1 + third_line.strip()
                                new_line_2 = line_2.strip()
                                new_line_3 = second_line.strip()
                                f_new.write(new_line_1 + '\n')
                                f_new.write(new_line_2 + '\n')
                                f_new.write(new_line_3 + '\n')
                        else:
                            new_line = line.strip() + second_line.strip()
                            f_new.write(new_line + '\n')
                else:
                    f_new.write(line)
                line = f.readline()

    shutil.rmtree(os.path.join(OUT_VALUE_DIR, prog_id))
    os.rename(os.path.join(OUT_VALUE_DIR, prog_id+'_new'), os.path.join(OUT_VALUE_DIR, prog_id))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='...')
    parser.add_argument('-p', '--prog_id', type=int, required=True, help='problem_id')
    args = parser.parse_args()

    prog_id = str(args.prog_id)
    post()
