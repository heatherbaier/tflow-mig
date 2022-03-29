#!/bin/tcsh
#PBS -N head_node
#PBS -l walltime=10:00:00
#PBS -j oe

# save the IP adress to a tesxt file for the TF_CONFIG
hostname -i > /sciclone/home20/hmbaier/tflow/ips/$NODE_NUM.txt

# wait until all jobs have started and saved an IP address to file before launching the training script
set size=`ls /sciclone/home20/hmbaier/tflow/ips/ | wc -l`
while ( $size != $WORLD_SIZE )
    set size=`ls /sciclone/home20/hmbaier/tflow/ips/ | wc -l`
    sleep 1
end

echo "$size"

# init conda within new shell for job
source "/usr/local/anaconda3-2021.05/etc/profile.d/conda.csh"
module load anaconda3/2021.05
unsetenv PYTHONPATH
conda activate tflow

# launch training script
python3 /sciclone/home20/hmbaier/tflow/run.py $NODE_NUM $WORLD_SIZE > "/sciclone/home20/hmbaier/tflow/logs/log${NODE_NUM}.txt"