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


def parse_trace(prog_id, split_method='all'):
    with open(os.path.join(VEC_DIR, f'all_mutation_aligned_{prog_id}.pickle'), 'rb') as f:
        select_data = pickle.load(f)
    with open(os.path.join(VEC_DIR, f'all_label_aligned_{prog_id}.pickle'), 'rb') as f:
        select_label = pickle.load(f)
    with open(os.path.join(VEC_DIR, f'all_files_aligned_{prog_id}.pickle'), 'rb') as f:
        select_files = pickle.load(f)



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

            test_data = [list(select_data[i]) for i in test_index]
            test_label = [select_label[i] for i in test_index]
            

            with open(os.path.join(Train_DIR, f'train_mutation_{prog_id}_splitBy{split_method}_{random_i}.pickle'), 'wb') as f:
                pickle.dump(train_data, f)
            with open(os.path.join(Train_DIR, f'train_label_mutation_{prog_id}_splitBy{split_method}_{random_i}.pickle'), 'wb') as f:
                pickle.dump(train_label, f)
            with open(os.path.join(Train_DIR, f'test_mutation_{prog_id}_splitBy{split_method}_{random_i}.pickle'), 'wb') as f:
                pickle.dump(test_data, f)
            with open(os.path.join(Train_DIR, f'test_label_mutation_{prog_id}_splitBy{split_method}_{random_i}.pickle'), 'wb') as f:
                pickle.dump(test_label, f)


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
