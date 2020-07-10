import os
from glob import glob
import re
import random
import pickle
import numpy as np
from tqdm import tqdm
import argparse

curr_dir_path = os.path.dirname(os.path.realpath(__file__))

OUT_INS_DIR = os.path.join(curr_dir_path, '../Data/ProgramData_OUT_INS')
VEC_DIR = os.path.join(curr_dir_path, '../Data/ProgramData_Trace')
if not os.path.exists(VEC_DIR):
    os.mkdir(VEC_DIR)

def parse_output():
    data_all = [] # raw mutation-based representation
    label_all = [] # labels
    type_all = [] # variable types for each variable
    for_all = [] # indicating if the variable is a loop condition
    values_all = [] # raw execution traces
    files_all = [] # filenames of each trace

    for inp_i in tqdm(range(1, 100+1)):
        out_ins_files = glob(os.path.join(OUT_INS_DIR, prog_id, '*_{}.txt'.format(inp_i)))

        # crowd-wisdom: select the mojority of output as the correct output.
        output_list = []
        output_count = []
        output_file_pair = {}
        for out_ori_f in out_ins_files:
            output = []
            with open(out_ori_f, 'r') as f:
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
                        output.append(line)
            output = ' '.join(output)
            output = output.replace(' ', '')
            if output not in output_list:
                output_list.append(output)
                output_count.append(1)
            else:
                output_count[output_list.index(output)] += 1
            output_file_pair[out_ori_f] = output_list.index(output)
        
        # start to extract traces of each execution
        max_count = max(output_count)
        for out_ins_f in output_file_pair:
            if not os.path.exists(out_ins_f):
                continue
            out_vec = {}
            var_order = []
            var_type = {}
            var_in_for = {}
            var_values = {}
            func_scope = []
            with open(out_ins_f, 'r') as out_f:
                for line in out_f.readlines():
                    line = line.strip()
                    if 'EnterFunction:' in line:
                        func_name = line.split(' ')[-1]
                        func_scope.append(func_name)
                    if 'Return' in line:
                        func_scope.pop(-1)
                    if 'DeclareVar:' in line:
                        var = re.search("DeclareVar: [*,&,(,\s]*(\w+)", line).group(1)
                        var = '{}_{}'.format(func_scope[-1], var)
                        if line.find('type: ') != -1:
                            v_type = line[line.find('type: ')+len('type: '):].replace(' ', '')
                            var_type[var] = v_type
                    if 'ChangedVar:' not in line or line.strip() == 'ChangedVar:':
                        continue

                    var = re.search("ChangedVar: [*,&,(,\s]*(\w+)", line).group(1)
                    if len(func_scope) != 0:
                        var = '{}_{}'.format(func_scope[-1], var)
                    # value = re.search("value: [*,&,(,\s]*(\w+)", line).group(1)
                    value = line[line.find('value:')+len('value:'):line.find(', isFor')]
                    try:
                        in_for = re.search("isFor: (True|False)", line).group(1)
                    except:
                        in_for = 'False'

                    # check type
                    if var not in var_type:
                        if in_for == 'True':
                            v_type = 'int'
                        elif line.find('type: ') != -1:
                            v_type = line[line.find('type: ')+len('type: '):].replace(' ', '')
                        else:
                            try:
                                tmp = int(value.strip())
                                v_type = 'int'
                            except:
                                try:
                                    tmp = ord(value.strip())
                                    v_type = 'char'
                                except:
                                    v_type = 'unknown'
                        var_type[var] = v_type
                    # add value
                    if var not in var_order:
                        var_order.append(var)
                        out_vec[var] = 1
                        var_in_for[var] = in_for
                        var_values[var] = [value]
                    else:
                        out_vec[var] += 1
                        if in_for == 'True':
                            var_in_for[var] = in_for
                        var_values[var].append(value)
            var_seq = []
            var_seq_type = []
            var_seq_for = []
            var_seq_values = []
            for var in var_order:
                if (var not in var_type) and var_in_for[var] == 'False':
                    continue
                elif (var not in var_type) and var_in_for[var] == 'True':
                    var_type[var] = 'int'
                var_seq.append(out_vec[var])
                var_seq_type.append(var_type[var])
                var_seq_for.append(var_in_for[var])
                var_seq_values.append(var_values[var])
            data_all.append(var_seq.copy())
            if output_count[output_file_pair[out_ins_f]] == max_count:
                label_all.append(0)
            else:
                label_all.append(1)
            type_all.append(var_seq_type.copy())
            for_all.append(var_seq_for.copy())
            values_all.append(var_seq_values.copy())
            files_all.append(out_ins_f.split('/')[-1])


    with open(os.path.join(VEC_DIR, f'all_mutation_{prog_id}.pickle'), 'wb') as f:
        pickle.dump(data_all, f)
    with open(os.path.join(VEC_DIR, f'all_label_{prog_id}.pickle'), 'wb') as f:
        pickle.dump(label_all, f)
    with open(os.path.join(VEC_DIR, f'all_type_{prog_id}.pickle'), 'wb') as f:
        pickle.dump(type_all, f)
    with open(os.path.join(VEC_DIR, f'all_for_{prog_id}.pickle'), 'wb') as f:
        pickle.dump(for_all, f)
    with open(os.path.join(VEC_DIR, f'all_traces_{prog_id}.pickle'), 'wb') as f:
        pickle.dump(values_all, f)
    with open(os.path.join(VEC_DIR, f'all_files_{prog_id}.pickle'), 'wb') as f:
        pickle.dump(files_all, f)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='...')
    parser.add_argument('-p', '--prog_id', type=int, required=True, help='problem_id')
    args = parser.parse_args()

    prog_id = str(args.prog_id)

    if not os.path.exists(VEC_DIR):
        os.mkdir(VEC_DIR)
    parse_output()
