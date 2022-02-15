import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--path", help="trace path from accel-sim-framework/util/tracer_nvbit", required=True)
args = parser.parse_args()

TRACE_PATH=args.path

START=None

def parse_kernel_number(l):
  return int(l.split("-")[1].split(".")[0])

# start, end
r = []
skip = True # skip first interval
with open(f"./{TRACE_PATH}/stats.csv") as f:
  lines = f.readlines()

  for i, l in enumerate(lines):
    if i == 0:
      continue

    l = l.split(",")

    n = parse_kernel_number(l[0].strip())
    name = l[1].strip()

    if name.find("forward_kernel_cuda_start") != -1:
      if skip:
        skip = False
        continue

      START = n

    if START is not None and name.find("forward_kernel_cuda_end") != -1:
      r.append((START, n))

intv = r[0][1] - r[0][0]
for s, t in r:
  assert intv == t - s

assert len(r) == 9

print(r[2][0], r[4][1])
