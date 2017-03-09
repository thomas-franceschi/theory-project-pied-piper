#Thomas Franceschi
#Kyle Williams

from nfa import *
import sys

def emptyset():
	myNfa = NFA()
	myNfa.set_start('0')
	return myNfa

def epsilon():
	myNfa = NFA()
	myNfa.set_start('0')
	myNfa.add_accept('1')
	myNfa.add_transition('0', '&', '1')
	#myNfa.write(sys.stdout)
	return myNfa

def symbol(a):
	myNfa = NFA()
	myNfa.set_start('0')
	myNfa.add_accept('1')
	myNfa.add_transition( '0', a, '1')
	myNfa.write(sys.stdout)
	return myNfa

def union(M1, M2):
	uNFA = NFA()
	NFA1 = M1
	NFA2 = M2
	offset = len(NFA1.states) + 1
	
	#copy in states
	for state in NFA1.states:
		uNFA.states.add( state + 1 )
	for state in NFA2.states:
		uNFA.states.add( state + offset )

	#copy in transitions
	for trans in NFA1.transitions:
		uNFA.add_transition( trans[0] + 1, trans[1], trans[2] + 1 )
	for trans in NFA2.transitions:
		uNFA.add_transition( trans[0] + offset + 1, trans[1], trans[2] + offset + 1 )

	#copy in accept states
	for state in NFA1.accept:
		uNFA.add_accept( state + 1)
	for state in NFA2.accept:
		uNFA.add_accept( state + offset + 1)
	#add new start state
	uNFA.states.add( 0 )

	#add epsilon transitions to old start states
	uNFA.add_transition( 0, '&', NFA1.start + 1)
	uNFA.add_transition( 0, '&', NFA2.start + offset + 1)
	uNFA.set_start(0)

	uNFA.write(sys.stdout)
	return uNFA

def concat(M1, M2):
	cNFA = NFA1
	NFA2 = M2
	cNFA.set_start(M1.start)
	for state in M1.accept:
		cNFA.add_transition( state, '&', NFA2.start)
	return cNFA

def star(M):
	starNFA = M
	starNFA.states.add('newStart')
	for state in starNFA.accept:
		starNFA.add_transition(state, '&', starNFA.start)
	starNFA.add_transition('newStart', '&', starNFA.start)
	starNFA.set_start('newStart')
	return starNFA

if __name__ == '__main__':
	#epsilon()
	m1 = NFA.read(open(sys.argv[1]))
	m2 = NFA.read(open(sys.argv[2]))
	union(m1, m2)