import argparse
import json
import os


def make_config(rank,  direc, port):

    # {"cluster": {"worker": ["128.239.59.1:12345", "128.239.59.2:12345"]}, "task": {"index": 1, "type": "worker"}}

    ips = []
    for file in os.listdir(direc):
        with open(direc + file, "r") as f:
            ips.append(f"{f.read().splitlines()[0]}:{port}")

    config = {"cluster": {"worker": ips}, "task": {"index": int(rank), "type": "worker"}}

    print(config)
 
    return json.dumps(config)

