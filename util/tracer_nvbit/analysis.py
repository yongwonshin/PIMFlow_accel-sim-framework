import argparse
import string

parser = argparse.ArgumentParser()
parser.add_argument("--post-process", action="store_true", help="only check for trace validity", default=False)
parser.add_argument("--path", help="trace path from accel-sim-framework/util/tracer_nvbit", required=True)
parser.add_argument("--skip", help="skip first N forward_kernel_cuda_start", type=int, default=4)
parser.add_argument("--post-process-only-overhead", action="store_true", help="only check for trace validity", default=False)
args = parser.parse_args()

TRACE_PATH=args.path

START=None
END=None

def parse_kernel_number(l):
  return int(l.split("-")[1].split(".")[0])

# start, end
skip = 0
with open(f"./{TRACE_PATH}/stats.csv") as f:
  lines = f.readlines()

  for i, l in enumerate(lines):
    if i == 0:
      continue

    l = l.split(",")

    n = parse_kernel_number(l[0].strip())
    name = l[1].strip()

    if name.find("forward_kernel_cuda_start") != -1:
      if skip <= args.skip:
        skip += 1
      else:
        START = n

    if START is not None and name.find("forward_kernel_cuda_end") != -1:
      END = n
      break

assert START is not None
assert END is not None

r1 = []
r2 = []
sincos = []
start = START
skip_from = None
with open(f"./{TRACE_PATH}/stats.csv") as f:
  lines = f.readlines()

  for i, l in enumerate(lines):
    if i == 0:
      continue

    l = l.split(",")

    n = parse_kernel_number(l[0].strip())
    if n < START:
      continue

    name = l[1].strip()

    if name.find("Sin") != -1:
      sincos.append(n)
      assert skip_from is None
      skip_from = n

      assert start <= n - 1
      r1.append((start, n - 1))

    if name.find("Cos") != -1:
      sincos.append(n)
      assert skip_from is not None
      r2.append((skip_from, n))
      skip_from = None
      start = n + 1

    if n == END:
      assert skip_from is None
      r1.append((start, n))
      break

print(len(r1))
print(r1)

print(len(r2))
print(r2)

with open(f"./{TRACE_PATH}/kernelslist.g") as f, open(f"./{TRACE_PATH}/kernelslist.g.unprocessed", "w") as g:
  lines = f.readlines()
  for i, l in enumerate(lines):
    if l.startswith("MemcpyHtoD"):
      g.write(l)
      continue

    n = parse_kernel_number(l.split(",")[0].strip())

    if START <= n and n <= END:
      g.write(l)

if args.post_process:
  with open(f"./{TRACE_PATH}/kernelslist.g") as f, open(f"./{TRACE_PATH}/kernelslist.g.processed", "w") as g:
    lines = f.readlines()
    for i, l in enumerate(lines):
      if l.startswith("MemcpyHtoD"):
        g.write(l)
        continue

      n = parse_kernel_number(l.split(",")[0].strip())

      for intv in r1:
        if intv[0] <= n and n <= intv[1]:
          g.write(l)
          break

if args.post_process_only_overhead:
  with open(f"./{TRACE_PATH}/kernelslist.g") as f, open(f"./{TRACE_PATH}/kernelslist.g.processed.overhead", "w") as g:
    lines = f.readlines()
    for i, l in enumerate(lines):
      if l.startswith("MemcpyHtoD"):
        g.write(l)
        continue

      n = parse_kernel_number(l.split(",")[0].strip())

      if n < START:
        continue

      if n > END:
        break

      if n not in sincos:
        g.write(l)

