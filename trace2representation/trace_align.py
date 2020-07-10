import os
from glob import glob
import re
import random
import pickle
import numpy as np
import argparse
from tqdm import tqdm
from scipy import stats

curr_dir_path = os.path.dirname(os.path.realpath(__file__))

drop_var_in_for = False
reorganize_var = True

VEC_DIR = os.path.join(curr_dir_path, '../Data/ProgramData_Trace')
if not os.path.exists(VEC_DIR):
    os.mkdir(VEC_DIR)

def trace_align(prog_id):

    # load data
    with open(os.path.join(VEC_DIR, f'all_mutation_{prog_id}.pickle'), 'rb') as f:
        all_data = pickle.load(f)
    with open(os.path.join(VEC_DIR, f'all_label_{prog_id}.pickle'), 'rb') as f:
        all_label = pickle.load(f)
    with open(os.path.join(VEC_DIR, f'all_for_{prog_id}.pickle'), 'rb') as f:
        all_for = pickle.load(f)
    with open(os.path.join(VEC_DIR, f'all_type_{prog_id}.pickle'), 'rb') as f:
        all_type = pickle.load(f)
        new_all_type = []
        for type_i, each_type in enumerate(all_type):
            new_type = []
            for each_i, t in enumerate(each_type):
                if t == 'int' or t == 'long' or t == 'unsignedshort' or t == 'short':
                    if all_for[type_i][each_i] == 'True':
                        new_type.append('int_for')
                    else:
                        new_type.append('int')
                elif t == 'char':
                    new_type.append('char')
                elif t == 'float' or t == 'double':
                    new_type.append('float')
                elif 'int' in t or 'long' in t:
                    new_type.append('int[]')
                elif 'float' in t or 'double' in t:
                    new_type.append('float[]')
                elif 'char' in t:
                    new_type.append('char[]')
                else:
                    new_type.append('unknown')
                    # print(f'\nUnknown type: {t}')
            new_all_type.append(new_type)
        all_type = new_all_type
    with open(os.path.join(VEC_DIR, f'all_traces_{prog_id}.pickle'), 'rb') as f:
        all_values = pickle.load(f)
    with open(os.path.join(VEC_DIR, f'all_files_{prog_id}.pickle'), 'rb') as f:
        all_files = pickle.load(f)

    # select data based on its length
    select_data = [] # mutation-based representation
    select_label = [] # labels
    select_type = [] # types of each variable in a representation
    select_values = [] # traces of each variable
    select_files = [] # sourcecode filenames of each representation

    for all_i in range(len(all_data)):
        # filter with length
        if len(all_data[all_i]) <= 0:
            continue

        if not reorganize_var:
            new_data = all_data[all_i]
            new_type = all_type[all_i]
            new_values = all_values[all_i]
        else:
            # reorganize var order based on type
            index_int_for = [i for i in range(len(all_type[all_i])) if all_type[all_i][i] == 'int_for']
            index_int = [i for i in range(len(all_type[all_i])) if all_type[all_i][i] == 'int']
            index_float = [i for i in range(len(all_type[all_i])) if all_type[all_i][i] == 'float']
            index_char = [i for i in range(len(all_type[all_i])) if all_type[all_i][i] == 'char']
            index_int_arr = [i for i in range(len(all_type[all_i])) if all_type[all_i][i] == 'int[]']
            index_float_arr = [i for i in range(len(all_type[all_i])) if all_type[all_i][i] == 'float[]']
            index_char_arr = [i for i in range(len(all_type[all_i])) if all_type[all_i][i] == 'char[]']
            index_unknown = [i for i in range(len(all_type[all_i])) if all_type[all_i][i] == 'unknown']
            new_data, new_type, new_values = [], [], []
            [new_data.append(all_data[all_i][i]) for i in index_int_for]
            [new_type.append(all_type[all_i][i]) for i in index_int_for]
            [new_values.append(all_values[all_i][i]) for i in index_int_for]
            [new_data.append(all_data[all_i][i]) for i in index_int]
            [new_type.append(all_type[all_i][i]) for i in index_int]
            [new_values.append(all_values[all_i][i]) for i in index_int]
            [new_data.append(all_data[all_i][i]) for i in index_float]
            [new_type.append(all_type[all_i][i]) for i in index_float]
            [new_values.append(all_values[all_i][i]) for i in index_float]
            [new_data.append(all_data[all_i][i]) for i in index_char]
            [new_type.append(all_type[all_i][i]) for i in index_char]
            [new_values.append(all_values[all_i][i]) for i in index_char]
            [new_data.append(all_data[all_i][i]) for i in index_int_arr]
            [new_type.append(all_type[all_i][i]) for i in index_int_arr]
            [new_values.append(all_values[all_i][i]) for i in index_int_arr]
            [new_data.append(all_data[all_i][i]) for i in index_float_arr]
            [new_type.append(all_type[all_i][i]) for i in index_float_arr]
            [new_values.append(all_values[all_i][i]) for i in index_float_arr]
            [new_data.append(all_data[all_i][i]) for i in index_char_arr]
            [new_type.append(all_type[all_i][i]) for i in index_char_arr]
            [new_values.append(all_values[all_i][i]) for i in index_char_arr]
            [new_data.append(all_data[all_i][i]) for i in index_unknown]
            [new_type.append(all_type[all_i][i]) for i in index_unknown]
            [new_values.append(all_values[all_i][i]) for i in index_unknown]
        # replace address-style value to '0'(for int/float) or '\0' (for char)
        for i in range(len(new_values)):
            for j in range(len(new_values[i])):
                if '0x' in new_values[i][j]:
                    if 'int' in new_type[i] or 'float' in new_type[i]:
                        new_values[i][j] = '0'
                    elif 'char' in new_type[i]:
                        new_values[i][j] = '\0'

        select_data.append(new_data)
        select_label.append(all_label[all_i])
        select_type.append(new_type)
        # slice values
        for v_i, v in enumerate(new_values):
            if len(v) > 5000:
                new_values[v_i] = new_values[v_i][:5000]
        select_values.append(new_values)
        select_files.append(all_files[all_i])
    
    def min_dist(new_data, global_data_list):
        # find value range
        global_value_range = []
        for global_i in range(len(global_data_list)-1):
            value_range = sorted(list(set(global_data_list[global_i])))
            global_value_range.append(value_range)
        new_value_range = sorted(list(set(new_data)))
        global_new_value_range = []
        for v_range in global_value_range:
            if -1 in v_range:
                v_range.remove(-1)
            global_new_value_range.append(sorted(list(set(v_range+new_value_range))))
        # calculate distribution
        global_distribution = []
        new_data_distribution = []
        for global_i, v_range in enumerate(global_new_value_range):
            tmp_global_dist = []
            tmp_new_dist = []
            for v in v_range:
                tmp_global_dist.append((global_data_list[global_i].count(v)+1)/len(global_data_list[global_i]))
                tmp_new_dist.append((new_data.count(v)+1) / len(new_data))
            global_distribution.append(tmp_global_dist.copy())
            new_data_distribution.append(tmp_new_dist.copy())
        # calculate KL-divergence along all features
        kl_dist = []
        for global_i in range(len(global_distribution)):
            kl_dist.append(stats.entropy(new_data_distribution[global_i], global_distribution[global_i]))
        # choose the one with minimun KL dist and less than threshold
        return kl_dist

    def cal_append_index(kl_dist_list):
        append_index_list = {}
        for kl_type in kl_dist_list:
            kl_dist = np.array(kl_dist_list[kl_type])
            append_index_list[kl_type] = [-1]*len(kl_dist)
            for kl_i in range(len(kl_dist[0])):
                append_from_list  = np.argsort(kl_dist[:, kl_i])
                for append_from in append_from_list:
                    if append_index_list[kl_type][append_from] == -1:
                        append_index_list[kl_type][append_from] = kl_i
                        break
        return append_index_list


    # first, count all types
    type_list = []
    type_count = []
    for v_type in select_type:
        if v_type not in type_list:
            type_list.append(v_type)
            type_count.append(1)
        else:
            type_count[type_list.index(v_type)] += 1
    # second, define global_type
    max_int_for, max_int, max_float, max_char, max_int_arr, max_float_arr, max_char_arr, max_unknown = 0, 0, 0, 0, 0, 0, 0, 0
    for v_type in type_list:
        if v_type.count('int_for') > max_int_for:
            max_int_for = v_type.count('int_for')
        elif v_type.count('int') > max_int:
            max_int = v_type.count('int')
        elif v_type.count('float') > max_float:
            max_float = v_type.count('float')
        elif v_type.count('char') > max_char:
            max_char = v_type.count('char')
        elif v_type.count('int[]') > max_int_arr:
            max_int_arr = v_type.count('int[]')
        elif v_type.count('float[]') > max_float_arr:
            max_float_arr = v_type.count('float[]')
        elif v_type.count('char[]') > max_char_arr:
            max_char_arr = v_type.count('char[]')
        elif v_type.count('unknown') > max_unknown:
            max_unknown = v_type.count('unknown')
    # iteratively add traces into global_type based on descend order of type_count.
    sorted_type_list = [type_list[i] for i in np.argsort(type_count)[::-1]]
    sorted_data_list = [0]*len(sorted_type_list)
    sorted_values_list = [0]*len(sorted_type_list)
    sorted_label_list = [0]*len(sorted_type_list)
    sorted_files_list = [0]*len(sorted_type_list)
    for data_i in range(len(select_data)):
        type_index = sorted_type_list.index(select_type[data_i])
        assert type_index >= 0
        if sorted_data_list[type_index] == 0:
            sorted_data_list[type_index] = []
            sorted_values_list[type_index] = []
            sorted_label_list[type_index] = []
            sorted_files_list[type_index] = []
        sorted_data_list[type_index].append(select_data[data_i])
        sorted_values_list[type_index].append(select_values[data_i])
        sorted_label_list[type_index].append(select_label[data_i])
        sorted_files_list[type_index].append(select_files[data_i])

    global_data = {} # mutation-based representation
    global_values = {} # traces of each variable
    global_label = [] # labels
    global_files = [] # sourcecode filenames of each representation
    global_index = {}

    # choose the number of seed variables
    all_lens = [len(d) for d in select_data]
    select_length = 8
    for all_l in [4, 5, 6, 7, 8]:
        data_num = sum([all_lens.count(data_l) for data_l in range(1, all_l+1)])
        if data_num / len(select_data) >= 0.8:
            select_length = all_l
            break
    print(f'selected number of variables: {select_length}')

    select_sorted_type = sorted_type_list[0]
    for each_type in sorted_type_list:
        if len(each_type) == select_length:
            select_sorted_type = each_type
            break

    # append seed mutation-based representations
    for sorted_i in range(len(sorted_data_list)):
        if sorted_type_list[sorted_i] != select_sorted_type:
            continue
        for data_i in range(len(sorted_data_list[sorted_i])):
            for each_i, each_type in enumerate(select_sorted_type):
                if each_type not in global_data:
                    global_data[each_type] = [[]]
                    global_values[each_type] = [[]]
                    global_index[each_type] = 0
                global_data[each_type][global_index[each_type]].append(sorted_data_list[sorted_i][data_i][each_i])
                global_values[each_type][global_index[each_type]].append(sorted_values_list[sorted_i][data_i][each_i])
                global_index[each_type] += 1
                if global_index[each_type] == len(global_data[each_type]):
                    global_data[each_type].append([])
                    global_values[each_type].append([])
            for each_i, each_type in enumerate(sorted_type_list[sorted_i]):
                global_index[each_type] = 0
            global_label.append(sorted_label_list[sorted_i][data_i])
            global_files.append(sorted_files_list[sorted_i][data_i])

    # iteratively add new traces based on K-L distance of seed and new mutation-based representation
    print('Align traces...')
    data_i = -1
    for data_list in tqdm(sorted_data_list):
        data_i += 1
        data_type = sorted_type_list[data_i]

        if data_type == select_sorted_type:
            continue

        kl_dist_list = {}
        for each_i, each_type in enumerate(data_type):
            if each_type not in global_data:
                continue
            each_data = [data[each_i] for data in data_list]
            kl_dist = min_dist(each_data, global_data[each_type])
            if each_type not in kl_dist_list:
                kl_dist_list[each_type] = []
            kl_dist_list[each_type].append(kl_dist)
        append_index_list = cal_append_index(kl_dist_list)
        for append_type in append_index_list:
            has_append_to = []
            for append_from, append_to in enumerate(append_index_list[append_type]):
                if append_to != -1:
                    append_from = data_type.index(append_type) + append_from
                    append_to_data = [data[append_from] for data in data_list]
                    append_to_values = [value[append_from] for value in sorted_values_list[data_i]]
                    global_data[append_type][append_to].extend(append_to_data)
                    global_values[append_type][append_to].extend(append_to_values)
                    has_append_to.append(append_to)
            # when lenght of new_data is less than global_data
            for append_to in range(len(global_data[append_type])-1):
                if append_to not in has_append_to:
                    global_data[append_type][append_to].extend([-1]*(len(data_list)))
                    global_values[append_type][append_to].extend([['-1'] for _ in range(len(data_list))])
        # check if all types are appended
        for global_type in global_data:
            if global_type not in append_index_list.keys():
                for append_to in range(len(global_data[global_type])-1):
                    global_data[global_type][append_to].extend([-1]*(len(data_list)))
                    global_values[global_type][append_to].extend([['-1'] for _ in range(len(data_list))])
        
        global_label.extend(sorted_label_list[data_i])
        global_files.extend(sorted_files_list[data_i])

    # organize aligned data
    select_data = []
    select_values = []
    for global_type in global_data:
        for i in range(len(global_data[global_type])-1):
            if select_data == []:
                select_data = np.array([global_data[global_type][i]])
                select_values = [global_values[global_type][i]]
            else:
                select_data = np.concatenate((select_data, [global_data[global_type][i]]))
                select_values.append(global_values[global_type][i])
    select_data = select_data.T
    select_values = list(map(list, zip(*select_values)))
    select_label = global_label
    select_files = global_files
    select_type = [select_sorted_type]*len(select_label)

    with open(os.path.join(VEC_DIR, f'all_mutation_aligned_{prog_id}.pickle'), 'wb') as f:
        pickle.dump(select_data, f)
    with open(os.path.join(VEC_DIR, f'all_traces_aligned_{prog_id}.pickle'), 'wb') as f:
        pickle.dump(select_values, f)
    with open(os.path.join(VEC_DIR, f'all_label_aligned_{prog_id}.pickle'), 'wb') as f:
        pickle.dump(select_label, f)
    with open(os.path.join(VEC_DIR, f'all_files_aligned_{prog_id}.pickle'), 'wb') as f:
        pickle.dump(select_files, f)
    with open(os.path.join(VEC_DIR, f'all_type_aligned_{prog_id}.pickle'), 'wb') as f:
            pickle.dump(select_type, f)
    print('\nTrace Align Done.')

if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(description='...')
    parser.add_argument('-p', '--prog_id', type=int, required=True, help='problem_id')
    args = parser.parse_args()

    prog_id = str(args.prog_id)

    trace_align(prog_id)

