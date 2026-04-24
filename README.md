## How to access INPT HPC Cluster?

### For MacOS/Linux Users:

You can use the terminal shell and simply type:

```bash
ssh username@login1.inpt.ac.ma
```

Or

```bash
ssh username@login2.inpt.ac.ma
```

Then enter your account login password.

The credentials of your HPC account will be provided by its administrators

---

### For Windows Users:

PS : This section needs to be done in detail later with more examples

You need to install a SSH Client to be used.

MobaXterm is preferred. Download it from the link below:
[https://mobaxterm.mobatek.net](https://mobaxterm.mobatek.net)


---

### Download MobaXterm:

Choose **Home Edition** then press **Download now**.

***This is a picture** — a screenshot of the MobaXterm download page showing the Home Edition (Free) and Professional Edition ($69/49€ per user) options.*

---


- Click **Session** then choose **SSH**
- Fill **Remote Host** with one of the login nodes IP address or hostname
- Then you will be requested to enter your **username** and **login password**

***This is a picture** — a screenshot of MobaXterm's Session Settings dialog with SSH selected and the Remote Host field visible.*

---

## Quick Tour on your account



## Home Directory

Once you logged in, you will be in your home directory `/home/$USER`

`pwd` : command to show the current directory

```bash
[username@login1 ~]$ pwd
/home/username
[username@login1 ~]$
```

- 25GB storage quota
- Best use is to save your source codes, scripts, results etc.
- **Never run your program in login nodes**

---

## Application Settings (environment modules)

There are many programs and tools that can be used without downloading them again and occupying space in the user's dedicated storage

First: Access all the shared application modules:

```bash
[username@login1 ~]$ module use /app/common/modules
```

To list all available modules (compilers/software packages) we use the module avail command:

```bash
[username@login1 ~]$ module avail
------------------------- /app/common/modules -------------------------
advisor/2025.0                dpl/2022.7                  
advisor/latest                dpl/latest                  
anaconda3-2024.10             intel_ipp_intel64/2022.0    
ccl/2021.14.0                 intel_ipp_intel64/latest    
ccl/latest                    intel_ippcp_intel64/2025.0  
compiler-intel-llvm/2025.0.4  intel_ippcp_intel64/latest  
compiler-intel-llvm/latest    mkl/2025.0                  
compiler-rt/2025.0.4          mkl/latest                  
compiler-rt/latest            mpi/2021.14                 
compiler/2025.0.4             mpi/latest                  
compiler/latest               opencv-4.x                  
debugger/2025.0.0             openmpi/4.1.2               
debugger/latest               openmpi/5.0.0               
dev-utilities/2025.0.0        tbb/2022.0                  
dev-utilities/latest          tbb/latest                  
dnnl/3.6.1                    umf/0.9.1                   
dnnl/latest                   umf/latest                  
dpct/2025.0.0                 vtune/2025.0                
dpct/latest                   vtune/latest                

------------------- /usr/share/Modules/modulefiles --------------------
dot  module-git  module-info  modules  null  use.own  

Key:
modulepath  
[username@login1 ~]$ 

```

---

To load a module:

```bash
[username@login1 ~]$ module load <module name>
```

To list the current loaded modules:

```bash
[username@login1 ~]$ module list
```

```bash
[username@login1 ~]$ module load anaconda3-2024.10
[username@login1 ~]$ module list
Currently Loaded Modulefiles:
  1) anaconda3-2024.10
```

---

To unload a specific module:

```bash
[username@login1 ~]$ module unload <module name>
```

To unload all the loaded modules:

```bash
[username@login1 ~]$ module purge
```

```bash
[username@login1 ~]$ module purge
[username@login1 ~]$ module list
No Modulefiles Currently Loaded.
```

---

## Anaconda Virtual Environments

**Step 1) Login to one of the Login nodes and load anaconda module then inititlize it**

```bash
[ababou.hamza@login1 ~]$ module use /app/common/modules/
[ababou.hamza@login1 ~]$ module load anaconda3-2024.10 
[ababou.hamza@login1 ~]$ /app/common/anaconda3-2024.10/bin/conda init
no change     /app/common/anaconda3-2024.10/condabin/conda
no change     /app/common/anaconda3-2024.10/bin/conda
no change     /app/common/anaconda3-2024.10/bin/conda-env
no change     /app/common/anaconda3-2024.10/bin/activate
no change     /app/common/anaconda3-2024.10/bin/deactivate
no change     /app/common/anaconda3-2024.10/etc/profile.d/conda.sh
no change     /app/common/anaconda3-2024.10/etc/fish/conf.d/conda.fish
no change     /app/common/anaconda3-2024.10/shell/condabin/Conda.psm1
no change     /app/common/anaconda3-2024.10/shell/condabin/conda-hook.ps1
no change     /app/common/anaconda3-2024.10/lib/python3.12/site-packages/xontrib/conda.xsh
no change     /app/common/anaconda3-2024.10/etc/profile.d/conda.csh
modified      /home/ababou.hamza/.bashrc

==> For changes to take effect, close and re-open your current shell. <==

[ababou.hamza@login1 ~]$ source .bashrc
(base) [ababou.hamza@login1 ~]$ 
```
At this point, conda is initialized and will be available at later sessions without having to load its module every time

**Step 2) Create your environment and specify the python version**

```bash
conda create -n ENV_NAME python=3.x
```

**Step 3) Activate the environment**

```bash
source activate ENV_NAME
```

**Step 4) Install the packages you need for this environment (using conda or pip)**

```bash
conda install pandas
```

Or:

```bash
pip install pandas
```

---

## Best Practices

The jobs are running in batch mode, i.e. it will be submitted to one compute node and start working there. If the job fails, you have to correct the error and submit it again.

Before submitting your job:

- To avoid job failure due to any missing packages for your script, **write and run a small python script to make sure all the required packages are installed** before submitting your job.
- The compute nodes have no internet access. **Write and run a small script to download all the required datasets and models** before submitting your jobs.
- **Make sure in your PBS or python scripts, all the paths referring to data, models and/or other scripts are correct.**


#### DO NOT run any computing program on the login nodes

The Login nodes are used only to:

- Access the cluster and submit your jobs.
- Browse, upload, or download your files.
- Create anaconda environments and install required packages.

---

## Submitting your PBS Batch Job

**Template PBS script to run a python script**

```bash
#!/bin/bash
#PBS -N example01
#PBS -l select=1:ncpus=20:ngpus=1
#PBS -q gpu_1d

# Load required modules
module load /app/common/modules/anaconda3-2024.10

# Load this module fo cuda related workloads and check with administrators for available versions if necessary
module load cuda/12.4

# Activate your virtual environment
source activate ENV_NAME

# change to working directory
cd $PBS_O_WORKDIR

# run your python script
python script_name.py
```

---

## PBS Common Commands

**Command to submit your PBS job**

```bash
qsub <Name of the script>
```

**Command to view submitted jobs**

```bash
qstat
```

**Command to delete job**

```bash
qdel <job id>
```

---

## Example project

All the files related to this project will be in this repository

### Setting up the environment

To set up a conda environment, we need first to determine which versions of the libraries we use. In this project we are using mainly Tensorflow. To determine which versions we need to lookup in official documentation which versions are compatible whith the local versions of either the Nvidia drivers as well as the CUDA toolkit, not to be confused with the CUDA version installed in the execution nodes. In our case the version of the CUDA toolkit installed is 12.4 and the version of CUDA is 13.2 so we need to lookup compatible version with 12/4 and not 13.2, among them is Tensorflow 2.21.0 which is in turn compatible with python 3.11

```bash
(base) [ababou.hamza@login1 ~]$ conda create -n test-project-env python=3.11
```
Then we start installing the required packages

Note that installing tensorflow, or any other library that relies heavily on the hardware it run on, is recommended to be installed via `pip` over `conda` to avoid potential issue

```bash
(base) [ababou.hamza@login1 ~]$ conda activate test-project-env
(test-project-env) [ababou.hamza@login1 ~]$ pip install tensorflow==2.21.0 nbconvert nvidia-cudnn-cu12
```
We continue installing some other packages
```bash
(test-project-env) [ababou.hamza@login1 ~]$ conda install kagglehub jupyter
```
### Downloading the datasets

This step can be done in different ways and depending on the user's needs. Here it was done via the python library kagglehub. The process was done in a python script that downloads the data and creates a file that has the path to the dataset for when needed. The python script is saved in the `download-dataset.py` file that can be found in the github repository.

**Note that this script absolutely needs to be executed in the login node and not in the execution nodes**

### Checking imports

Checking the imports and whether all the dependencies is done by having a python scripts that imports all these dependencies then prints all the successful and failed ones. This operation needs to be done on the execution nodes because many times, some libraries are hardware reliant and will fail to be imported if done on the login nodes that don't have dedicated nvidia GPUs and/or some features found on the Intel Xeon CPUs.

So we need to run the script on the execution nodes, to do that, we need to write a PBS script where we describe the commands that will be executed in the execution node. Bellow is the one used for this specific example.

```bash
#!/bin/bash

#PBS -N testing
#PBS -l select=1:ncpus=20:ngpus=1
#PBS -q gpu_1d

# Load required modules, here it is the anaconda module and the cuda module
module load /app/common/modules/anaconda3-2024.10 
# For the exact name of the modules, check first in the 
module load cuda/12.4


# Activate your virtual environment
source activate test-project-env 

export LD_LIBRARY_PATH=$CONDA_PREFIX/lib:$LD_LIBRARY_PATH

# change to working directory
cd $PBS_O_WORKDIR
# run your python script
python check-imports.py
```

The first lines indicate to the scheduler what are our needs for the job we are about to submit and also a name for the job. In our case it is a job that requires 20 CPU cores and one GPU. We also indicate that we are intending to use in the queue reserved for job with a maximum of 1 day of compute in this line `#PBS -q gpu_1d`.

Then we load the modules we need, in this case, it is the anaconda module and the CUDA module.

The following line is sometimes required in order to tell the execution node to look for the conda packages in the activated conda enironment, otherwise it may look elsewhere, leading to errors.

Finally we change to the directory from where we submitted the job and execute the script. Then we submit the job with the following command

```bash
(test-project-env) [ababou.hamza@login1 test-project]$ qsub check-imports.pbs 
11193.head1
```

The output of the job is divided into two files that we can find after the job is done in the active directory. The files are titles *JOBNAME*.e*JOBID* that has error logs and *JOBNAME*.o*JOBID* that has the output generated by whatever we did in the job.

In our case this is the output of the job we did to check the imports

```bash
(test-project-env) [ababou.hamza@login1 test-project]$ cat testing.o11193 
==================================================
Checking required imports...
==================================================
  [OK]   kagglehub
  [OK]   tensorflow
  [OK]   tensorflow (keras.layers)
  [OK]   tensorflow (keras.models)
  [OK]   tensorflow (keras.applications VGG16)
  [OK]   tensorflow (vgg16 preprocess_input)
==================================================
All imports OK. Environment is ready.
```
### Running the main job

In our case, instead of having all of the opeations in a python script, we have them in a jupyter notebook. Since we cannot have an interaction with the execution nodes, we used nbconvert to be able to run a notebook in one go. For this before submitting a job we need to make sure that all the cells are correct and won't trigger an error because in such case the job will be interrupted and we will need to start again.

Submitting the job for the main operation is done the same way as the previous showcase when we were checking the imports. This is the PBS script used to submit the job

```bash
(test-project-env) [ababou.hamza@login1 test-project]$ cat main-job.pbs
#!/bin/bash

#PBS -N testing
#PBS -l select=1:ncpus=20:ngpus=1
#PBS -q gpu_1d

# Load required modules, here it is the anaconda module and the cuda module
module load /app/common/modules/anaconda3-2024.10 

# For the exact name of the cuda toolkit and available versions, check with the administration
module load cuda/12.4

# Activate your virtual environment
source activate test-project-env 

export LD_LIBRARY_PATH=$CONDA_PREFIX/lib:$LD_LIBRARY_PATH

# change to working directory
cd $PBS_O_WORKDIR
# run your python script

TIMESTAMP=$(date +"%Y%m%d_%H%M%S")

jupyter nbconvert \
    --to notebook \
    --execute main2.ipynb \
    --output outputs/executed_from_main_notebook_${TIMESTAMP}.ipynb \
    --ExecutePreprocessor.timeout=7200 \
    2>&1 | tee logs/run_${TIMESTAMP}.log

echo "Exit code :$?"
```

A successful execution of the job wil create a timestamped output jupyter notebook as well as timestamped models, all of these in an `outputs` directory and a `models` directory respectively

---

*Thanks*
