#Thomas Franceschi
#Kyle Williams

from nfa import *
import sys

def emptyset():
	myNfa = NFA()
	myNfa.set_start('q1')
	return myNfa

def epsilon():
	myNfa = NFA()
	myNfa.set_start('q1')
	myNfa.add_accept('q2')
	myNfa.add_transition('q1', '&', 'q2')
	#myNfa.write(sys.stdout)
	return myNfa

def symbol(a):
	myNfa = NFA()
	myNfa.set_start('q1')
	myNfa.add_accept('q2')
	myNfa.add_transition( 'q1', a, 'q2')
	myNfa.write(sys.stdout)
	return myNfa

def union(M1, M2):
	uNFA = M1
	NFA2 = M2
	
	#copy in states
	for state in M2.states:
		uNFA.states.add( 'r' + str(state) )

	#copy in transitions
	for trans in M2.transitions:
		uNFA.add_transition( 'r' + str(trans[0]), trans[1], 'r' + str(trans[2]))

	#copy in accept states
	for state in M2.accept:
		uNFA.add_accept('r' + str(state))
	#add new start state
	uNFA.states.add('s')

	#add epsilon transitions to old start states
	uNFA.add_transition('s', '&', uNFA.start)
	uNFA.add_transition('s', '&', 'r' + str(NFA2.start))
	uNFA.set_start('s')

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