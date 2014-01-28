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

def sendhashes(hashes, address):
    print address
    print "\n".join(hashes)
    print

if len(sys.argv) != 2:
    print "Usage sendkeys.py emailfile"
    sys.exit(1)

m = """
TEXT

%s

"""
hashes = []
for line in open(sys.argv[1]):
    key = genkey(32)
    hash = hashlib.sha1(key).hexdigest()
    hashes.append(hash)
    print line, key, hash

random.shuffle(hashes)

f = open("hashes.txt", "w")
for h in hashes:
    f.write(h + '\n')
f.close()
