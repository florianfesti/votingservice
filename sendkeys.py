#!/bin/python

import sys, random, string, hashlib

# XXX remove before use
random.seed(0)

def genkey(l):
    return "".join((random.choice(string.letters) for i in xrange(l)))

def mixparts(parts):
    l = len(parts[0])
    order = range(l)
    random.shuffle(order)
    result = []
    for p in parts:
        pnew = []
        for n in order:
            pnew.append(p[n])
        result.append(pnew)
    return result

def sendpart(part, address):
    print address
    print "\n".join(part)
    print

if len(sys.argv) != 2:
    print "Usage sendkeys.py emailfile"

m = """
TEXT

%s

"""

parts = [[],[],[]]
for line in open(sys.argv[1]):
    key = ""
    for p in parts:
        keypart = genkey(8)
        p.append(keypart)
        key += keypart
    print line, key

parts = mixparts(parts)

for p in parts:
    sendpart(p, "foo@example.com")
