#!/usr/bin/python
import os
from resource import *

# Grabs addresses from a plaintext file containing one IPv4 address
# per line, stores it into a set.  Prints a message showing how
# many addresses it has added and the RSS size after every
# 10000 addresses.  
print_stats = 10000

# To generate a file, try a bash one-liner such as (16387064 addresses):
# for c in `seq 1 254`; do for b in `seq 1 254`; do for a in `seq 1 254`; do echo 1.$c.$b.$a >> ipset.list.small ; done; done; done
source_file = 'ipset.list.small'

blocklist = set()
with open(source_file) as fh:
    while True:
        line = fh.readline()
        if not line:
            break
        blocklist.add(line)
        if ((len(blocklist) % print_stats) == 0):
            print("%d items uses %d KB of memory" % (len(blocklist), getrusage(RUSAGE_SELF)[2]))
fh.close()

print("Loaded %d items using %d KB of memory" % (len(blocklist), getrusage(RUSAGE_SELF)[2]))

