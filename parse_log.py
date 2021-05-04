# crappy parsing

import sys
import re

#logfile = sys.argv[1]
logfile = "res18_baseline.log"

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

print("epoch,train_loss,train_acc,test_loss,test_acc")

for i in range(200):
    train_loss, train_acc = parse_line(lines[i])
    test_loss, test_acc = parse_line(lines[i+1])
    print(f"{i},{train_loss},{train_acc},{test_loss},{test_acc}")