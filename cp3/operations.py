#!/usr/bin/env python2.7

# CP3
# Kyle Williams
# Thomas Franceschi

from nft import *
import sys

def emptyset():
	myNFT = NFT()
	myNFT.set_start('0')
	return myNFT

def epsilon():
	myNFT = NFT()
	myNFT.set_start('0')
	myNFT.add_accept('1')
	myNFT.add_transition('0', '&', '&', '1')
	return myNFT

def symbol(a):
	myNFT = NFT()
	myNFT.set_start('0')
	myNFT.add_accept('1')
	myNFT.add_transition( '0', a, a, '1')
	myNFT.write(sys.stdout)
	return myNFT

def union(M1, M2):
	uNFT = NFT()
	NFT1 = M1
	NFT2 = M2
	offset = len(NFT1.states) + 1
	
	#copy in states
	for state in NFT1.states:
		uNFT.states.add( state + 1 )
	for state in NFT2.states:
		uNFT.states.add( state + offset )

	#copy in transitions
	for trans in NFT1.transitions:
		transit = uNFT.Transition( trans[0] + 1, trans[1], trans[2], trans[3] + 1 )
		uNFT.add(transit)
		#uNFT.add_transition( trans[0] + 1, trans[1], trans[2] + 1 )
	for trans in NFT2.transitions:
		transit = uNFT.Transition( trans[0] + offset, trans[1], trans[2], trans[3] + offset )
		uNFT.add(transit)
		#uNFT.add_transition( trans[0] + offset, trans[1], trans[2] + offset )

	#copy in accept states
	for state in NFT1.accept:
		uNFT.add_accept( state + 1)
	for state in NFT2.accept:
		uNFT.add_accept( state + offset)
	#add new start state
	uNFT.states.add( 0 )

	#add epsilon transitions to old start states
	uNFT.add_transition( 0, '&', '&', NFT1.start + 1)
	uNFT.add_transition( 0, '&', '&', NFT2.start + offset)
	uNFT.set_start(0)

	return uNFT

def concat(M1, M2):
	cNFT = NFT()
	NFT1 = M1
	NFT2 = M2
	offset = len(NFT1.states)

	#copy in states
	for state in NFT1.states:
		cNFT.states.add( state )
	for state in NFT2.states:
		cNFT.states.add( state + offset )

	#copy in transitions
	for trans in NFT1.transitions:
		transit = cNFT.Transition( trans[0], trans[1], trans[2], trans[3] )
		cNFT.add(transit)
	for trans in NFT2.transitions:
		transit = cNFT.Transition( trans[0] + offset, trans[1], trans[2], trans[3] + offset )
		cNFT.add(transit)

	#connect accept states to second start state
	for state in NFT1.accept:
		cNFT.add_transition( state, '&', '&', NFT2.start + offset)

	#set accept state
	for state in NFT2.accept:
		cNFT.add_accept(state + offset)

	#set start state
	cNFT.set_start(NFT1.start)

	cNFT.set_start(M1.start)
	for state in M1.accept:
		cNFT.add_transition( state, '&', '&', NFT2.start + offset)
	return cNFT

def star(M):
	starNFT = NFT()
	NFT1 = M

	#copy in states
	for state in NFT1.states:
		starNFT.states.add( state + 1 )

	#copy in transitions
	for trans in NFT1.transitions:
		transit = starNFT.Transition( trans[0] + 1, trans[1], trans[2], trans[3] + 1 )
		starNFT.add(transit)
		#starNFT.add_transition( trans[0] + 1, trans[1], trans[2] + 1 )

	#copy in accept states
	for state in NFT1.accept:
		starNFT.add_accept( state + 1)
	
	#add new start state
	starNFT.states.add( 0 )

	#add epsilon transitions from accept to new start
	for state in starNFT.accept:
		starNFT.add_transition( state, '&', '&', 1)

	#add transition to old start
	starNFT.add_transition( 0, '&', '&', 1)
	starNFT.set_start( 0 )
	starNFT.add_accept( 0 )

	return starNFT

def transduce(M1, M2):
	tNFT = NFT()
	NFT1 = M1
	NFT2 = M2
	offset = len(NFT1.states)

	#copy in states
	for state in NFT1.states:
		tNFT.states.add( state )
	for state in NFT2.states:
		tNFT.states.add( state + offset )

	#copy in transitions
	for trans in NFT1.transitions:
		transit = tNFT.Transition( trans[0], trans[1], '&', trans[3] )
		tNFT.add(transit)
	for trans in NFT2.transitions:
		transit = tNFT.Transition( trans[0] + offset, '&', trans[2], trans[3] + offset )
		tNFT.add(transit)

	#connect accept states to second start state
	for state in NFT1.accept:
		tNFT.add_transition( state, '&', '&', NFT2.start + offset)

	#set accept state
	for state in NFT2.accept:
		tNFT.add_accept(state + offset)

	#set start state
	tNFT.set_start(NFT1.start)

	tNFT.set_start(M1.start)
	for state in M1.accept:
		tNFT.add_transition( state, '&', '&', NFT2.start + offset)
	return tNFT


if __name__ == '__main__':
	#epsilon()
	m1 = NFT.read(open(sys.argv[1]))
	m2 = NFT.read(open(sys.argv[2]))
	mc = concat(m1, m2)
	mc.write(sys.stdout)

	#m = NFT.read(open(sys.argv[1]))
	#ms = star(m)
	#ms.write(sys.stdout)