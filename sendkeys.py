#!/bin/python

import sys, random, string, hashlib

# XXX remove before use
random.seed(0)

def genkey(l):
    return "".join((random.choice(string.letters) for i in xrange(l)))

def mixhashes(hashes):
    l = len(hashes)
    order = range(l)
    random.shuffle(order)
    result = []
    for n in order:
        result.append(hashes[n])
    return result

def sendhashes(hashes, address):
    print address
    print "\n".join(hashes)
    print

if len(sys.argv) != 2:
    print "Usage sendkeys.py emailfile"

m = """
TEXT

%s

"""
hashes = []
for line in open(sys.argv[1]):
    key = genkey(32)
    hash = hashlib.sha1(key).hexdigest()
    hashes.append(hash)
    hashes.append('\n')
    print line, key, hash

mixhashes(hashes)
f = open("hashes.txt", "w")
f.writelines(hashes)
f.close()
