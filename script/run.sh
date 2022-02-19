#!/bin/bash
BASE_PATH="/root/accel-sim-framework"

source "$BASE_PATH/gpu-simulator/setup_environment.sh"

function run {
  $BASE_PATH/gpu-simulator/bin/release/accel-sim.out -trace "$BASE_PATH/util/tracer_nvbit/$1/$2" -config "$BASE_PATH/gpu-simulator/configs/tested-cfgs/$3/trace.config" -config "$BASE_PATH/gpu-simulator/gpgpu-sim/configs/tested-cfgs/$3/gpgpusim.config$4" &> $1.$2.txt
}

# example: run traces kernelslist.g
# example: run traces kernelslist.g.processed
run $1 $2 $3 $5
