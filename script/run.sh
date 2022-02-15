#!/bin/bash
BASE_PATH="/root/accel-sim-framework"

source "$BASE_PATH/gpu-simulator/setup_environment.sh"

function run {
  #nohup "$BASE_PATH/gpu-simulator/bin/release/accel-sim.out" -trace "$BASE_PATH/util/tracer_nvbit/$1/$2" -config "$BASE_PATH/gpu-simulator/configs/tested-cfgs/SM75_RTX2060/trace.config" -config "$BASE_PATH/gpu-simulator/gpgpu-sim/configs/tested-cfgs/SM75_RTX2060/gpgpusim.config" &> $1.$2.txt &!
  $BASE_PATH/gpu-simulator/bin/release/accel-sim.out -trace "$BASE_PATH/util/tracer_nvbit/$1/$2" -config "$BASE_PATH/gpu-simulator/configs/tested-cfgs/SM75_RTX2060/trace.config" -config "$BASE_PATH/gpu-simulator/gpgpu-sim/configs/tested-cfgs/SM75_RTX2060/gpgpusim.config$3" &> $1.$2.txt
}

# example: run traces kernelslist.g
# example: run traces kernelslist.g.processed
run $1 $2