#!/bin/python

import sys, string, hashlib
import random as _random
# XXX set to False before use
DEBUG=True

if DEBUG:
    random = _random
    random.seed(0)
    print "###################\nWARNING: DEBUG=True\n###################"
else:
    random = _random.SystemRandom()

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
