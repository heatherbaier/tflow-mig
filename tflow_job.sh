#!/bin/tcsh
#PBS -N head_node
#PBS -l walltime=01:00:00
#PBS -j oe

/sciclone/home20/hmbaier/tflow/ips.sh

# init conda within new shell for job
source "/usr/local/anaconda3-2021.05/etc/profile.d/conda.csh"
module load anaconda3/2021.05
unsetenv PYTHONPATH
conda activate tflow

python3 /sciclone/home20/hmbaier/tflow/worker.py $NODE_NUM > "/sciclone/home20/hmbaier/tflow/log${NODE_NUM}.txt"