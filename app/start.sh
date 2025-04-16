#!/bin/bash

start_sh_server
start_code_server

python ./ignite.py

while true; do sleep 1; done
