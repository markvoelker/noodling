#!/usr/bin/python3
import radix
import os
from resource import *
import time

# Config...where should we get addresses?
ipset_file = 'firehol_level1.netset'

# Make a radix tree.
rtree = radix.Radix()

# Open up an ipset file and add it's entries to the tree.
subnet_count = 0
with open(ipset_file) as fh:
    while True:
        line = fh.readline()
        if not line:
            # End of file
            break
        if line.startswith('#'):
            # Ignore comments
            continue
        else:
            # Add this entry as a node.
            rnode = rtree.add(line.rstrip())
            subnet_count += 1

            # Print a note so we can see how RSS grows as the tree grows.
            print("Loaded %d subnets using %d KB of memory" % 
                    (subnet_count, getrusage(RUSAGE_SELF)[2]))

# Mind your P's and Q's, and always close your filehandles.
fh.close()

# We now have a fully populated tree.  What's our final memory footprint?
print("\nCOMPLETE!  Loaded %d subnets using %d KB of memory\n" %
        (subnet_count, getrusage(RUSAGE_SELF)[2]))

# Some IP addresses to look up...some of these should be blocked, some not.
test_ips = ('8.8.8.8', '192.168.111.161', '1.2.3.4', '224.0.0.1', 
        '13.224.208.3', '0.0.0.128', '3.90.198.217')

# Iterate over the test list, track how much time it takes to get
# an answer from our radix tree.
for ip in test_ips:
    # This is a nanosecond timer in Python3
    start = time.perf_counter_ns()

    rnode = rtree.search_best(ip)
    
    stop = time.perf_counter_ns()
    
    # If we get a null back, the address wasn't found in any of the subnets
    # in the tree, so it's allowed.  Otherwise, it's blocked.
    if rnode:
        print(f"%s BLOCKED in {stop - start:d} ns!" % ip)
    else:
        print(f"%s allowed in {stop - start:d} ns." % ip)
