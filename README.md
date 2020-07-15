# Specification-free Faulty Execution Detection

This repository contains all the code and data for the paper "Specification-free Faulty Execution Detection".

## Requirements
On Ubuntu:
* Python3 (>=3.6).
* numpy (>=1.17.2)
* scikit-learn (>=0.21.3)

## Quickstart
### Step 0: Cloning this repository
```
git clone https://github.com/faultdetection/anonymous
cd anonymous
```

### Step 1: Downloading dataset
One can use the dataset to reproduce all experimental results in the paper.
* If you don't want to download the dataset, you can jump to [Step 3](#Step-3:-Transforming-execution-traces-into-representations) directly as we already put necessary data in the current 'Data' directory.
* Download compressed dataset <b>anonymous_data.tar.gz</b> from anonymous Google Drive: https://drive.google.com/file/d/10C25olTSKxnYERPwW6UW0l2Stf1Kr5cZ/view?usp=sharing
* Uncompress dataset with
```
tar -xvf anonymous_data.tar.gz
```
* Move all subdirs in 'anonymous_data/Data/*' into current 'Data/' directory.

#### Dataset structure:

* <b>ProgramData_ORI</b> : Sourcecode
* <b>ProgramData_COM_ORI</b> : executable files of sourcecode.
* <b>ProgramData_COM_INS</b> : executable files of sourcecode after instrumentation (for execution trace logging).
* <b>ProgramData_INPUT</b> : pre-generated 100 inputs for each program class.
* <b>ProgramData_Trace</b>: execution traces, used to obtain representations.

### Step 2: Collecting execution traces
This step is to collect execution traces from raw outputs of original and intrumented codes.
All traces collected in this step are already avaiable in the dataset.
You can jump to [Step 3](#Step-3:-Transforming-execution-traces-into-representations) to utilize these traces.
In the following, we take program class 21 as an example, you can always use '-h' for help information.

(<b>optional</b>)If you want to generate new inputs instead of using pre-generated 100 inputs, run:
'''
cd generate_input/
python generate_input_21.py
'''

* Rhange working dir:
```
cd trace_collect/
```

* Run all original programs on 100 inputs in a program class:
```
python 1.auto_run_ori.py -p 21
```
* Run all instrumented programs on 100 inputs in a program class:
```
python 2.auto_run_ins.py -p 21
```
* Postprocessing to fix unexpected formats in raw outputs of instrumented programs.
```
python 3.post.py -p 21
```
* Compare outputs from original and instrumented programs, remove outputs that are inconsistent in these two kind of programs.
```
python 4.compare_out.py -p 21 --auto-remove True
```
* Parse raw outputs of instrumented progarms into full execution traces, then label them as faulty not not.
```
python 5.parse_out.py -p 21
```
Now, full execution traces and their labels are parsed into 'Data/ProgramData_Trace/'

### Step 3: Transforming execution traces into representations
* change working dir:
```
cd trace2representation/
```
In the following, we take program class 21 as an example, 
you can always use '-h' for help information.
* Align all traces from programs in the same program class.
```
python trace_align.py -p 21
```
* Transforming execution traces into mutation-based representations.
```
python trace2mutation.py -p 21
```
* Transforming execution traces into behavioral representations.
```
python trace2behavioral.py -p 21
```
* Transforming execution traces into pivot representations with the number of pivot values set to 20.
```
python trace2pivot.py -p 21 -n 20
```

The resulting representations will be saved into 'Data/TrainData'.

### Step 4: Detecting faulty executions with representations
* Change working dir:
```
cd detection
```
* Use Random Forest to learn mutation-based representations from one program class on split_all Training set, then detect faulty executions on Test set.
```
python detection_random_forest.py -p 21 -s all -rep mutation
```
Use '-h' to find out meaning of parameters.
* Use PCA to learn mutation-based representations for each program, then detect faulty executions. 
* Note that, the output precision and recall are progams from the same program class.
* '-t' specifies the anomaly threshold.
```
python detection_pca.py -p 21 -t 3.0 -rep mutation
```
Use '-h' to find out meaning of parameters.
