#!/usr/bin/env python2.7

import nft
import sys

m1 = nft.NFT.read(open(sys.argv[1]))
m2 = nft.NFT.read(open(sys.argv[2]))
mc = nft.NFT.compose(m1, m2)
mc.write(sys.stdout)

