import os
from glob import glob
import re
import random
import pickle
import numpy as np
import subprocess
import time
import argparse

curr_dir_path = os.path.dirname(os.path.realpath(__file__))
COM_ORI_DIR = os.path.join(curr_dir_path, '../Data/ProgramData_COM_ORI')
COM_VALUE_DIR = os.path.join(curr_dir_path, '../Data/ProgramData_COM_INS')
INP_DIR = os.path.join(curr_dir_path, '../Data/ProgramData_INPUT')

OUT_ORI_DIR = os.path.join(curr_dir_path, '../Data/ProgramData_OUT_ORI')
OUT_INS_DIR = os.path.join(curr_dir_path, '../Data/ProgramData_OUT_INS')


def get_inconsistent_files(prog_id):
    bad_files = []

    for inp_i in range(1, 100+1):
        out_ori_files = glob(os.path.join(OUT_ORI_DIR, prog_id, '*_{}.txt'.format(inp_i)))
        out_ori_files.sort()

        output_list = []
        output_count = []
        output_file_pair = {}
        for out_ori_f in out_ori_files:
            out_ins_f = out_ori_f.replace(OUT_ORI_DIR, OUT_INS_DIR)
            if not os.path.exists(out_ins_f):
                print('INS File {} not exists'.format(out_ins_f.split('/')[-1]))
                re_run(prog_id, out_ins_f.split('/')[-1].split('_')[0], inp_i, try_time=0)
                if not os.path.exists(out_ins_f):
                    continue

            # get output from instrumented code
            output_ins = []
            with open(out_ins_f, 'r') as f:
                for line in f.readlines():
                    line = line.strip()
                    if 'Enter' in line:
                        line = line[:line.find('Enter')]
                    if 'DeclareVar' in line:
                        line = line[:line.find('DeclareVar')]
                    if 'Change' in line:
                        line = line[:line.find('Change')]
                    if 'Return' in line:
                        line = line[:line.find('Return')]
                    if line != '':
                        output_ins.append(line)
            output_ins = ''.join(output_ins)
            output_ins = output_ins.replace(' ', '')
            
            # get output from original code
            output_ori = []
            with open(out_ori_f, 'r') as f:
                for line in f.readlines():
                    line = line.strip()
                    if line != '':
                        output_ori.append(line)
            output_ori = ''.join(output_ori)
            output_ori = output_ori.replace(' ', '')

            # if outputs from original code and instrumented code are not identical, try fixing first; if cannot fix, then remove.
            if output_ori != output_ins:
                bad_files.append(out_ins_f)
                print('File {} inconsistent on input {}'.format(out_ori_f.split('/')[-1], inp_i))
                fixed = re_run(prog_id, out_ins_f.split('/')[-1].split('_')[0], inp_i, try_time=0)
                if fixed == 0 and auto_remove:
                    # cannot fix, remove file
                    os.remove(out_ins_f)
                    print('>removed.')
    return bad_files

def re_run(prog_id, code_id, inp_id, try_time=2):
    exe_file_ori = os.path.join(COM_ORI_DIR, prog_id, code_id+'.txt.o')
    exe_file_value = os.path.join(COM_VALUE_DIR, prog_id, code_id+'.txt.o')

    if not os.path.exists(exe_file_value):
        print('exe not exists')
        return -1

    out_path_ori = os.path.join(OUT_ORI_DIR, prog_id, '{}_{}.txt'.format(code_id, inp_id))
    out_path_value = os.path.join(OUT_INS_DIR, prog_id, '{}_{}.txt'.format(code_id, inp_id))

    inp_path = os.path.join(INP_DIR, prog_id, '{}.txt'.format(inp_id))

    for _ in range(try_time):
        # execute
        out_ori = execute(exe_file_ori, inp_path, out_path_ori)
        out_value = execute(exe_file_value, inp_path, out_path_value)
        if out_ori == out_value:
            print('fixed')
            return 1
    print('cannot fix')
    return 0

def execute(exe_path, inp_path, out_path):
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
        # time.sleep(1)
    try:
        output = output.decode('utf-8').strip()
    except:
        return ''
    
    output_final = []
    if len(output) <= 10000000:
        with open(out_path, 'w') as out_f:
            out_f.write(output)
        
        with open(out_path, 'r') as f:
            for line in f.readlines():
                line = line.strip()
                if 'Enter' in line:
                    line = line[:line.find('Enter')]
                if 'DeclareVar' in line:
                    line = line[:line.find('DeclareVar')]
                if 'Change' in line:
                    line = line[:line.find('Change')]
                if 'Return' in line:
                    line = line[:line.find('Return')]
                if line != '':
                    try:
                        output_final.append(line)
                    except:
                        pass
    output_final = ' '.join(output_final)
    return output_final

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='...')
    parser.add_argument('-p', '--prog_id', type=int, required=True, help='problem_id')
    parser.add_argument('-r', '--auto-remove', type=str, required=False, default='True', help='if auto-remove inconsistent files')
    args = parser.parse_args()

    prog_id = str(args.prog_id)
    if args.auto_remove == 'True':
        auto_remove = True
    else:
        auto_remove = False
    bad_files = get_inconsistent_files(prog_id)
