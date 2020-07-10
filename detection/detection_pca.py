import os
from glob import glob
import re
import random
import pickle
import json
import numpy as np
from tqdm import tqdm
import argparse
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.decomposition import PCA

curr_dir_path = os.path.dirname(os.path.realpath(__file__))
import sys
sys.path.append(curr_dir_path)
sys.path.append(os.path.join(curr_dir_path, '..'))
from trace2representation.trace2behavioral import get_behavioral
from trace2representation.trace2pivot import get_pivot_value

drop_var_in_for = False
align_var = True
reorganize_var = True

VEC_DIR = os.path.join(curr_dir_path, '../Data/ProgramData_Trace')
if not os.path.exists(VEC_DIR):
    os.mkdir(VEC_DIR)


def cal_prec_reca(test_label, test_error, pca_th):
    if test_error == 0 or test_label.count(1) == 0:
        return None, None
    test_label = np.array(test_label)
    test_error = np.array(list(map(float, test_error))) 
    pred_label = test_label[(test_error >= pca_th).nonzero()]
    precision = pred_label.tolist().count(1) / len(pred_label) if len(pred_label) != 0 else 1.0
    recall = pred_label.tolist().count(1) / test_label.tolist().count(1) if test_label.tolist().count(1) != 0 else 1.0
    return precision, recall

def align_data(select_data, select_values, select_type):
    '''align data for pca. This align is different from trace_align as PCA only deals with traces from one program.'''
    type_len = [len(each_type) for each_type in select_type]
    fix_type = select_type[np.argmax(type_len)]

    new_select_type = [fix_type]*len(select_data)
    new_select_data = []
    new_select_values = []
    for select_i in range(len(select_data)):
        if select_type[select_i] == fix_type:
            new_select_data.append(select_data[select_i])
            new_select_values.append(select_values[select_i])
        else:
            new_each_data = []
            new_each_values = []
            each_i_start = 0
            for fix_i in range(len(fix_type)):
                match = False
                for each_i in range(each_i_start, len(select_type[select_i])):
                    if fix_type[fix_i] == select_type[select_i][each_i]:
                        new_each_data.append(select_data[select_i][each_i])
                        new_each_values.append(select_values[select_i][each_i])
                        each_i_start += 1
                        match = True
                        break
                if not match:
                    new_each_data.append(0)
                    new_each_values.append(['0'])
            new_select_data.append(new_each_data)
            new_select_values.append(new_each_values)
    
    return new_select_data, new_select_values, new_select_type

def pca_analyzer(prog_vec, prog_label, pca_th=3.0):
    prog_vec, prog_label = np.array(prog_vec), np.array(prog_label)
    pos_vec = prog_vec[prog_label==1]
    neg_vec = prog_vec[prog_label==0]
    np.random.shuffle(neg_vec)
    np.random.shuffle(pos_vec)
    # pos_vec = pos_vec[:20]

    vec = neg_vec[:int(0.5*len(neg_vec))]
    test_vec = neg_vec[int(0.5*len(neg_vec)):]
    test_label = np.array([0]*len(test_vec))
    test_vec = np.concatenate((test_vec, pos_vec), axis=0)
    test_label = np.concatenate((test_label, np.array([1]*len(pos_vec))), axis=0)


    # pca analysis
    training_data = np.array(vec)
    if training_data.shape[0] <= training_data.shape[1]:
        return 0, 0, 0, 0, 0
    # normalize data
    standard_scaler = StandardScaler(with_std=True)
    # standard_scaler = MinMaxScaler()
    centered_training_data = standard_scaler.fit_transform(training_data)
    # train with PCA
    pca = PCA()
    pca.fit(centered_training_data)

    k = 0
    sum_variance_ratio = 0
    for i, variance_ratio in enumerate(pca.explained_variance_ratio_):
        sum_variance_ratio += variance_ratio
        if sum_variance_ratio > 0.95:
            k = i + 1
            break
    
    pca = PCA(n_components=k)
    pca.fit(centered_training_data)
    y = standard_scaler.transform(test_vec)
    new_y = pca.inverse_transform(pca.transform(y))

    error = np.sum((y-new_y) ** 2, 1)

    large_labels = test_label[(error >= pca_th).nonzero()]

    test_label = test_label.tolist()
    error = list(map(lambda x: f'{x:.2f}', error.tolist()))

    return len(centered_training_data), test_label.count(0), test_label.count(1), test_label, error

def pca(prog_id, pca_th=3.0, representation='mutation'):

    # load data
    with open(os.path.join(VEC_DIR, f'all_mutation_{prog_id}.pickle'), 'rb') as f:
        all_data = pickle.load(f)
    with open(os.path.join(VEC_DIR, f'all_label_{prog_id}.pickle'), 'rb') as f:
        all_label = pickle.load(f)
    with open(os.path.join(VEC_DIR, f'all_type_{prog_id}.pickle'), 'rb') as f:
        all_type = pickle.load(f)
    with open(os.path.join(VEC_DIR, f'all_traces_{prog_id}.pickle'), 'rb') as f:
        all_values = pickle.load(f)
    with open(os.path.join(VEC_DIR, f'all_files_{prog_id}.pickle'), 'rb') as f:
        all_files = pickle.load(f)

    all_progs = []
    all_progs_index = {}
    for f_i, f in enumerate(all_files):
        filename = f.split('/')[-1].split('_')[0]
        if filename not in all_progs:
            all_progs.append(filename)
            all_progs_index[filename] = [f_i]
        else:
            all_progs_index[filename].append(f_i)
    
    for prog_name in (all_progs):
        try:
            select_data = [all_data[prog_i] for prog_i in all_progs_index[prog_name]]
            select_label = [all_label[prog_i] for prog_i in all_progs_index[prog_name]]
            select_type = [all_type[prog_i] for prog_i in all_progs_index[prog_name]]
            select_values = [all_values[prog_i] for prog_i in all_progs_index[prog_name]]
            select_files = [all_files[prog_i] for prog_i in all_progs_index[prog_name]]

            if representation == 'mutation':
                select_data, select_values, select_type = align_data(select_data, select_values, select_type)
                train_neg, test_neg, test_pos, test_label, error = pca_analyzer(select_data, select_label, pca_th=pca_th)
                prec, reca = cal_prec_reca(test_label, error, pca_th)
                if prec != None:
                    print(f'Mutation -- program: {prog_name}, prec: {prec:.3f}, reca: {reca:.3f}')
            elif representation == 'behavioral':
                select_behavioral = get_behavioral(select_data, select_type, select_values)
                train_neg, test_neg, test_pos, test_label, error = pca_analyzer(select_behavioral, select_label, pca_th=pca_th)
                prec, reca = cal_prec_reca(test_label, error, pca_th)
                if prec != None:
                    print(f'Behavioral -- program: {prog_name}, prec: {prec:.3f}, reca: {reca:.3f}')
            elif 'pivot' in representation:
                try:
                    num_pivot = int(representation[representation.find('pivot_')+len('pivot_'):])
                except:
                    print(f'Unknown representation: {representation}')
                    exit(0)
                select_pivot_data, select_pivot_value = get_pivot_value(select_data, select_type, select_values, num_pivot=num_pivot)
                train_neg, test_neg, test_pos, test_label, error = pca_analyzer(select_pivot_data, select_label, pca_th=pca_th)
                prec, reca = cal_prec_reca(test_label, error, pca_th)
                if prec != None:
                    print(f'Pivot_{num_pivot} -- program: {prog_name}, prec: {prec:.3f}, reca: {reca:.3f}')
            else:
                print(f'Unknown representation: {representation}')
                exit(0)
        except:
            continue


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='...')
    parser.add_argument('-p', '--prog_id', type=int, required=True, help='problem_id')
    parser.add_argument('-t', '--pca_th', type=str, required=False, default='3.0', help='threshhold')
    parser.add_argument('-rep', '--representation', type=str, required=True, help='representation (mutation, behavioral, pivot_xx)')
    args = parser.parse_args()

    prog_id = str(args.prog_id)
    pca_th = float(args.pca_th)

    pca(prog_id, pca_th, args.representation)

