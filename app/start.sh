#!/bin/bash

# Start the servers in the background
start_sh_server
start_code_server

# Run both Python scripts in parallel
python ./memory/memory_management.py &
python ./ignite.py &
python ./memory_api.py &

# Keep the script running to maintain the processes
while true; do
    sleep 1
done
