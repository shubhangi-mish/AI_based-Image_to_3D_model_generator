#!/bin/bash

start_sh_server
start_code_server

python ./memory/memory_management.py &
python ./ignite.py &
python ./memory_api.py &

while true; do
    sleep 1
done
