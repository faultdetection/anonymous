import os
import numpy as np
from glob import glob
import pickle
from sklearn.metrics import precision_recall_fscore_support, pairwise
from sklearn.model_selection import GridSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import AdaBoostClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn import preprocessing
import argparse
import json

curr_dir_path = os.path.dirname(os.path.realpath(__file__))
MODEL_DIR = os.path.join(curr_dir_path, '../Data/ProgramData_Model')

# load train and test data
def load_data(data_path, seq_len=50, data_type='data'):
    if not os.path.exists(data_path):
        print(f'Unknown representation: {data_type}')
        exit(0)
    with open(data_path, 'rb') as f:
        all_data = pickle.load(f)
    with open(data_path.replace(f'_{data_type}_', f'_label_{data_type}_'), 'rb') as f:
        all_label = pickle.load(f)
    
    data = []
    label = []
    for i in range(len(all_data)):
        seq = all_data[i].copy()
        if len(all_data[i]) <= 0:
            continue
        if seq_len is not None:
            if len(all_data[i]) < seq_len:
                seq.extend([0]*(seq_len-len(seq)))
            elif len(all_data[i]) > seq_len:
                seq = seq[:seq_len]
        # normalize
        seq = np.array(seq) #/ np.linalg.norm(np.array(seq))
        data.append(seq)
        label.append(all_label[i])
    # normalize along the same feature
    # data = preprocessing.normalize(data)

    return np.array(data), np.array(label)

def random_forest(split_method, representation='mutation', num_random_split=1):
    seq_len = None
    select_data_types = [
        representation
    ]

    test_results = {}
    for data_type in select_data_types:
        test_acc = 0.0
        prec_b = 0.0
        reca_b = 0.0
        supp_b = 0.0
        prec_n = 0.0
        reca_n = 0.0
        supp_n = 0.0
        for i_split in range(1, num_random_split+1):
            train_data, train_label = load_data(os.path.join(curr_dir_path, Train_Dir, f'train_{data_type}_{prog_id}_splitBy{split_method}_{i_split}.pickle'), seq_len, data_type)
            test_data, test_label = load_data(os.path.join(curr_dir_path, Train_Dir, f'test_{data_type}_{prog_id}_splitBy{split_method}_{i_split}.pickle'), seq_len, data_type)
            if len(train_data) == 0:
                num_random_split -= 1
                continue

            neigh = RandomForestClassifier(n_estimators=200, random_state=0, n_jobs=4)

            neigh.fit(train_data, train_label)

            # with open(os.path.join(MODEL_DIR, f'rf_{data_type}_{prog_id}_splitBy{split_method}_{i_split}.model'), 'wb') as f:
                # pickle.dump(neigh, f)

            test_output = neigh.predict(np.array(test_data))

            test_metric = precision_recall_fscore_support(np.array(test_label), test_output, average=None, labels=[0, 1])

            test_acc += sum(test_output == np.array(test_label)) / len(test_label)
            prec_b += test_metric[0][1]
            reca_b += test_metric[1][1]
            supp_b += test_metric[3][1]
            prec_n += test_metric[0][0]
            reca_n += test_metric[1][0]
            supp_n += test_metric[3][0]

        print(data_type)
        print('-- lenOfTrain: {}, lenOfTest: {}, test_acc: {:.3f}, prec_faulty: {:.3f}, reca_faulty: {:.3f}'.format(
            len(train_data),
            len(test_data),
            test_acc / num_random_split,
            prec_b / num_random_split,
            reca_b / num_random_split,
        ))


if __name__ == "__main__":

    Train_Dir = '../Data/TrainData/'

    parser = argparse.ArgumentParser(description='...')
    parser.add_argument('-p', '--prog_id', type=int, required=True, help='problem_id')
    parser.add_argument('-s', '--split_method', type=str, required=True, help='split method (all, program, input)')
    parser.add_argument('-rep', '--representation', type=str, required=True, help='representation (mutation, behavioral, pivot_xx)')
    parser.add_argument('-random', '--random', type=int, required=False, default=1, help='number of random split for training, default=1')
    args = parser.parse_args()

    prog_id = str(args.prog_id)
    num_random_split = int(args.random)

    random_forest(args.split_method, args.representation, num_random_split)
