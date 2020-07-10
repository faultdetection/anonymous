# Specification-free Faulty Execution Detection

This repository contains all the code and data for the paper "Specification-free Faulty Execution Detection".

## Requirements
On Ubuntu:
    * Python3 (>=3.6).
    * numpy
    * scikit-learn

## Quickstart
### Step 0: Cloning this repository
```
git clone https://github.com/faultdetection/anonymous
cd anonymous
```

### Step 1: Downloading dataset
One can use the dataset to reproduce all experimental results in the paper.
```
TODO: add link.
```
* Move all subdirs in downloaded dataset into 'Data' directory.
* If you don't want to download the dataset, you can jump to [Step 3](#Step 3) directly as we already put necessary data in the 'Data'.

#### Dataset structure:

* ProgramData_ORI : Sourcecode
* ProgramData_COM_ORI : executable files of sourcecode.
* ProgramData_COM_INS : executable files of sourcecode after instrumentation (for execution trace logging).
* ProgramData_INPUT : pre-generated 100 inputs for each program class.
* ProgramData_Trace: execution traces, used to obtain representations.

### Step 2: Collecting execution traces
This step is to collect execution traces from raw outputs of original and intrumented codes.
All traces collected in this step are already avaiable in the dataset.

If you want to generate new inputs instead of using pre-generated 100 inputs:
> cd generate_input
> python generate_input_21.py

* working dir:
```
cd trace_collect
```
In the following, we use program class 21 for example, you can always use '-h' for help.
* run all original programs on 100 inputs in a program class:
```
python 1.auto_run_ori.py -p 21
```
* run all instrumented programs on 100 inputs in a program class:
```
python 2.auto_run_ins.py -p 21
```
* postprocessing to fix unexpected formats in raw outputs of instrumented programs.
```
python 3.post.py -p 21
```
* compare outputs from original and instrumented programs, remove outputs that are inconsistent in these two kind of programs.
```
python 4.compare_out.py -p 21 --auto-remove True
```
* parse raw outputs of instrumented progarms into full execution traces, then label them as faulty not not.
```
python 5.parse_out.py -p 21
```
Now, full execution traces and their labels are parsed into 'Data/ProgramData_Trace/'

### Step 3: Transforming execution traces into representations
* working dir:
```
cd trace2representation
```
In the following, we take program class 21 as an example, 
you can always use '-h' for help.
* align traces in the same program class.
```
python trace_align.py -p 21
```
* transforming execution traces into mutation-based representations.
```
python trace2mutation.py -p 21
```
* transforming execution traces into behavioral representations.
```
python trace2behavioral.py -p 21
```
* transforming execution traces into pivot representations with the number of pivot values set to 20.
```
python trace2mutation.py -p 21 -n 20
```

The resulting representations will be saved into 'Data/TrainData'.

### Step 4: Detecting faulty executions with representations
* working dir:
```
cd detection
```
* use Random Forest to learn mutation-based representations from one program class on split_all Training set, then detect faulty executions on Test set.
```
python detection_random_forest.py -p 21 -s all -rep mutation
```
Use '-h' to find out meaning of parameters.
* use PCA to learn mutation-based representations for each program, then detect faulty executions. 
* Note that, the output precision and recall are progams from the same program class.
* '-t' specifies the anomaly threshold.
```
python detection_pca.py -p 21 -t 3.0 -rep mutation
```
Use '-h' to find out meaning of parameters.
