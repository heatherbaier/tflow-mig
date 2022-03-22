rm -R /sciclone/home20/hmbaier/tflow/ips/
mkdir /sciclone/home20/hmbaier/tflow/ips/

for ((i = 1; i <= $1; i++))
do
	qsub /sciclone/home20/hmbaier/tflow/tflow_job.sh -l nodes=1:meltemi:ppn=1 -v NODE_NUM=$i,NUM_NODES=$1
done


