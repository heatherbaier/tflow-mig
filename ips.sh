#!/bin/bash

hostname -i > /sciclone/home20/hmbaier/tflow/ips/$NODE_NUM.txt

size=$(ls /sciclone/home20/hmbaier/tflow/ips/ | wc -l)

while [ $size != $NUM_NODES ]
do
    size=$(ls /sciclone/home20/hmbaier/tflow/ips/ | wc -l)
    sleep 1
done

echo "$size"
