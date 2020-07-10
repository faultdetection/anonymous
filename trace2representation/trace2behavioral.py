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

def get_behavioral(select_data, select_type, select_values):
    # get behavioral data, for each variable of type int (excl. int arrays)
    select_behavioral = []
    for data_i in range(len(select_data)):
        vec_behavioral = []
        for vec_i in range(len(select_data[data_i])):
            if 'int' in select_type[data_i][vec_i] or 'float' in select_type[data_i][vec_i]:
                behavioral = [0, 0, 0] # three behavioral for an int variable, i.e., [INCREASE, DECREASE, REMAIN]
                prev_value = select_values[data_i][vec_i][0]
                for next_value in select_values[data_i][vec_i][1:]:
                    try:
                        next_value = int(next_value)
                    except:
                        try:
                            next_value = float(next_value)
                        except:
                            next_value = -1
                    try:
                        prev_value = int(prev_value)
                    except:
                        try:
                            prev_value = float(prev_value)
                        except:
                            prev_value = -1
                    if next_value > prev_value:
                        behavioral[0] += 1
                    elif next_value < prev_value:
                        behavioral[1] += 1
                    else:
                        behavioral[2] += 1
                    prev_value = next_value
                # vec_behavioral.append(select_data[data_i][vec_i])
                vec_behavioral.extend(behavioral)
            else:
                vec_behavioral.append(select_data[data_i][vec_i])
        select_behavioral.append(vec_behavioral.copy())
    return select_behavioral

def parse_trace(prog_id, split_method='all', align_var=True):

    with open(os.path.join(VEC_DIR, f'all_mutation_aligned_{prog_id}.pickle'), 'rb') as f:
        select_data = pickle.load(f)
    with open(os.path.join(VEC_DIR, f'all_traces_aligned_{prog_id}.pickle'), 'rb') as f:
        select_values = pickle.load(f)
    with open(os.path.join(VEC_DIR, f'all_label_aligned_{prog_id}.pickle'), 'rb') as f:
        select_label = pickle.load(f)
    with open(os.path.join(VEC_DIR, f'all_files_aligned_{prog_id}.pickle'), 'rb') as f:
        select_files = pickle.load(f)
    with open(os.path.join(VEC_DIR, f'all_type_aligned_{prog_id}.pickle'), 'rb') as f:
        select_type = pickle.load(f)


    select_additional_data = {
        'behavioral': get_behavioral(select_data, select_type, select_values),
    }

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
    parser.add_argument('-random', '--random', type=int, required=False, default=1, help='number of random split for training, default=1')
    args = parser.parse_args()

    prog_id = str(args.prog_id)
    num_random_split = int(args.random)

    parse_trace(prog_id)

