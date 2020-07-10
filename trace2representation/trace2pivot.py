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

def get_pivot_data(select_data, select_type, select_values, pivot_values, process_char=False):
    # get pivot data
    select_pivot = []
    for value_i in range(len(select_values)):
        vec_pivot = []
        for vec_i in range(len(select_values[value_i])):
            if 'int' in select_type[value_i][vec_i]:
                try:
                    values = [int(v) for v in select_values[value_i][vec_i]]
                except:
                    values = [-1]*len(select_values[value_i][vec_i])
                pivot = [0] * (len(pivot_values[vec_i])+1) # two values for an int variable, i.e., [>=, <]
                for v in values:
                    for pivot_i in range(len(pivot_values[vec_i])):
                        if v <= int(pivot_values[vec_i][pivot_i]):
                            pivot[pivot_i] += 1
                            break
                    if v > int(pivot_values[vec_i][-1]):
                        pivot[-1] += 1
                vec_pivot.extend(pivot)
            elif 'float' in select_type[value_i][vec_i]:
                try:
                    values = [float(v) for v in select_values[value_i][vec_i]]
                except:
                    values = [-1]*len(select_values[value_i][vec_i])
                pivot = [0] * (len(pivot_values[vec_i])+1) # two values for an int variable, i.e., [>=, <]
                for v in values:
                    for pivot_i in range(len(pivot_values[vec_i])):
                        if v <= float(pivot_values[vec_i][pivot_i]):
                            pivot[pivot_i] += 1
                            break
                    if v > float(pivot_values[vec_i][-1]):
                        pivot[-1] += 1
                vec_pivot.extend(pivot)
            elif 'char' in select_type[value_i][vec_i] and process_char:
                values = [v for v in select_values[value_i][vec_i]]
                pivot = [0] * (len(pivot_values[vec_i])+1) # two values for an int variable, i.e., [>=, <]
                for v in values:
                    for pivot_i in range(len(pivot_values[vec_i])):
                        if v <= pivot_values[vec_i][pivot_i]:
                            pivot[pivot_i] += 1
                            break
                    if v > pivot_values[vec_i][-1]:
                        pivot[-1] += 1
                vec_pivot.extend(pivot)
            else:
                vec_pivot.append(select_data[value_i][vec_i])
        select_pivot.append(vec_pivot.copy())
    return select_pivot

def get_pivot_value(select_data, select_type, select_values, num_pivot=1, process_char=False, method='even'):
    # get values range for all variables
    values_range = []
    for col in range(len(select_values[0])):
        col_type = select_type[0][col]
        one_column = []
        for value in select_values:
            if 'int' in col_type:
                try:
                    _value = [int(v.strip()) for v in value[col]]
                except:
                    continue
            elif 'float' in col_type:
                _value = [float(v.strip()) for v in value[col]]
            else:
                _value = [v.strip() for v in value[col]]
            one_column.extend(_value)
        one_column.sort()
        values_range.append(list(one_column))

    # get pivot values from 1 to max_num_pivot
    pivot_value = []
    for v_range in values_range:
        v_range = sorted(list(set(v_range)))
        select_pivot = []
        if method == 'even':
            select_len = min(num_pivot, len(v_range))
            for select_i in range(1, select_len+1):
                select_pivot.append(v_range[int(select_i/(select_len+1)*len(v_range))])
        elif method == 'order':
            select_len = min(num_pivot, len(v_range))
            for select_i in range(0, select_len):
                if select_i < num_pivot:
                    select_pivot.append(v_range[int(select_i/select_len*len(v_range))])
        else:
            print('Unknown pivot method.')
            exit(1)
        pivot_value.append(select_pivot)

    pivot_data = get_pivot_data(select_data, select_type, select_values, pivot_value, process_char)
    return pivot_data, pivot_value

def parse_trace(prog_id, num_pivot=1):

    # mutation-based representation
    with open(os.path.join(VEC_DIR, f'all_mutation_aligned_{prog_id}.pickle'), 'rb') as f:
        select_data = pickle.load(f)
    # raw traces
    with open(os.path.join(VEC_DIR, f'all_traces_aligned_{prog_id}.pickle'), 'rb') as f:
        select_values = pickle.load(f)
    with open(os.path.join(VEC_DIR, f'all_label_aligned_{prog_id}.pickle'), 'rb') as f:
        select_label = pickle.load(f)
    with open(os.path.join(VEC_DIR, f'all_files_aligned_{prog_id}.pickle'), 'rb') as f:
        select_files = pickle.load(f)
    with open(os.path.join(VEC_DIR, f'all_type_aligned_{prog_id}.pickle'), 'rb') as f:
        select_type = pickle.load(f)

    print('generate pivot data ...')
    select_additional_data = {}
    select_pivot_data, _ = get_pivot_value(select_data, select_type, select_values, num_pivot=num_pivot, process_char=True, method='even')
    select_additional_data[f'pivot_{num_pivot}'] = select_pivot_data

    # randomly split data into training and test datasets based on filename
    for split_method in ['all', 'program', 'input']:
        select_filenames = []
        for f in select_files:
            if split_method == 'all':
                f = f
            elif split_method == 'program':
                f = f.split('_')[0] # by programs
            elif split_method == 'input':
                f = f.split('.')[0].split('_')[1] # by inputs
            select_filenames.append(f)
        distinct_filenames = list(set(select_filenames))
        print(f'generating training data for split_{split_method} ...')
        for random_i in tqdm(range(1, num_random_split+1)):
            split_train = 0.8
            random.shuffle(distinct_filenames)
            split_index = int(0.8*len(distinct_filenames))

            train_filenames = distinct_filenames[:split_index]
            train_index = [i for i in range(len(select_filenames)) if select_filenames[i] in train_filenames]
            test_filenames = distinct_filenames[split_index:]
            test_index = [i for i in range(len(select_filenames)) if select_filenames[i] in test_filenames]

            train_data = [list(select_data[i]) for i in train_index]
            train_label = [select_label[i] for i in train_index]
            train_additional_data = {}
            for key in select_additional_data:
                train_additional_data[key] = [list(select_additional_data[key][i]) for i in train_index]

            test_data = [list(select_data[i]) for i in test_index]
            test_label = [select_label[i] for i in test_index]
            test_additional_data = {}
            for key in select_additional_data:
                test_additional_data[key] = [list(select_additional_data[key][i]) for i in test_index]
            
            #remove test_data that already in train_data
            if split_method == 'all':
                keep_index = []
                for i in range(len(test_data)):
                    keep = False
                    if test_data[i] not in train_data:
                        keep = True
                    for key in test_additional_data:
                        if test_additional_data[key][i] not in train_data:
                            keep = True
                            break
                    if keep:
                        keep_index.append(i)

                test_data = [test_data[i] for i in keep_index]
                test_label = [test_label[i] for i in keep_index]
                for key in test_additional_data:
                    test_additional_data[key] = [test_additional_data[key][i] for i in keep_index]

            with open(os.path.join(Train_DIR, f'train_label_{key}_{prog_id}_splitBy{split_method}_{random_i}.pickle'), 'wb') as f:
                pickle.dump(train_label, f)
            with open(os.path.join(Train_DIR, f'test_label_{key}_{prog_id}_splitBy{split_method}_{random_i}.pickle'), 'wb') as f:
                pickle.dump(test_label, f)
            for key in test_additional_data:
                with open(os.path.join(Train_DIR, f'train_{key}_{prog_id}_splitBy{split_method}_{random_i}.pickle'), 'wb') as f:
                    pickle.dump(train_additional_data[key], f)
                with open(os.path.join(Train_DIR, f'test_{key}_{prog_id}_splitBy{split_method}_{random_i}.pickle'), 'wb') as f:
                    pickle.dump(test_additional_data[key], f)


if __name__ == "__main__":

    Train_DIR = os.path.join(curr_dir_path, '../Data/TrainData')
    if not os.path.exists(Train_DIR):
        os.mkdir(Train_DIR)
    
    parser = argparse.ArgumentParser(description='...')
    parser.add_argument('-p', '--prog_id', type=int, required=True, help='problem_id')
    parser.add_argument('-n', '--num_pivot', type=int, required=True, help='number of pivot values for each variable')
    parser.add_argument('-random', '--random', type=int, required=False, default=1, help='number of random split for training, default=1')
    args = parser.parse_args()

    prog_id = str(args.prog_id)
    num_pivot = int(args.num_pivot)
    num_random_split = int(args.random)
    parse_trace(prog_id, num_pivot)

