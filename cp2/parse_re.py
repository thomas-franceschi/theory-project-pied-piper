#!/usr/bin/env python3

from parser import *
import sys

regex = sys.argv[1]
length = len(regex)
counter = 0
parser = baseParser(regex, length, counter)
M = parser.parseRegexp()

print(M)