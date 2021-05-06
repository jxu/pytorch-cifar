# crappy parsing

import sys
import re

logfile = sys.argv[1]


def parse_line(line):
    p = re.compile(r"Loss: (.+) \| Acc: (.+)%")
    m = p.search(line)
    loss = float(m.group(1))
    acc = float(m.group(2))
    return loss, acc

with open(logfile) as f:
    rawlines = f.readlines()

lines = [l.strip() for l in rawlines if "Loss" in l]
assert len(lines) == 400

outfile = logfile.replace(".log", ".csv")

with open(outfile, 'w') as f:
    f.write("epoch,train_loss,train_acc,test_loss,test_acc\n")


    for i in range(200):
        train_loss, train_acc = parse_line(lines[2*i])
        test_loss, test_acc = parse_line(lines[2*i+1])
        f.write(f"{i},{train_loss},{train_acc},{test_loss},{test_acc}\n")