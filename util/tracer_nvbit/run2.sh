#!/bin/bash
#export DYNAMIC_KERNEL_LIMIT_START=53
#export DYNAMIC_KERNEL_LIMIT_END=82

#export CUDA_VISIBLE_DEVICES=0
LD_PRELOAD=./tracer_tool/tracer_tool.so python3 /root/pact2022/$1/$2.py "${@:3}"



