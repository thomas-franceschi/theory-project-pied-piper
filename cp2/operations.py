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
		transit = uNFA.Transition( trans[0] + 1, trans[1], trans[2] + 1 )
		uNFA.add(transit)
		#uNFA.add_transition( trans[0] + 1, trans[1], trans[2] + 1 )
	for trans in NFA2.transitions:
		transit = uNFA.Transition( trans[0] + offset, trans[1], trans[2] + offset )
		uNFA.add(transit)
		#uNFA.add_transition( trans[0] + offset, trans[1], trans[2] + offset )

	#copy in accept states
	for state in NFA1.accept:
		uNFA.add_accept( state + 1)
	for state in NFA2.accept:
		uNFA.add_accept( state + offset)
	#add new start state
	uNFA.states.add( 0 )

	#add epsilon transitions to old start states
	uNFA.add_transition( 0, '&', NFA1.start + 1)
	uNFA.add_transition( 0, '&', NFA2.start + offset)
	uNFA.set_start(0)

	return uNFA

def concat(M1, M2):
	cNFA = NFA()
	NFA1 = M1
	NFA2 = M2
	offset = len(NFA1.states)

	#copy in states
	for state in NFA1.states:
		cNFA.states.add( state )
	for state in NFA2.states:
		cNFA.states.add( state + offset )

	#copy in transitions
	for trans in NFA1.transitions:
		transit = cNFA.Transition( trans[0], trans[1], trans[2] )
		cNFA.add(transit)
	for trans in NFA2.transitions:
		transit = cNFA.Transition( trans[0] + offset, trans[1], trans[2] + offset )
		cNFA.add(transit)

	#connect accept states to second start state
	for state in NFA1.accept:
		cNFA.add_transition( state, '&', NFA2.start + offset)

	#set accept state
	for state in NFA2.accept:
		cNFA.add_accept(state + offset)

	#set start state
	cNFA.set_start(NFA1.start)

	cNFA.set_start(M1.start)
	for state in M1.accept:
		cNFA.add_transition( state, '&', NFA2.start + offset)
	return cNFA

def star(M):
	starNFA = NFA()
	NFA1 = M

	#copy in states
	for state in NFA1.states:
		starNFA.states.add( state + 1 )

	#copy in transitions
	for trans in NFA1.transitions:
		transit = starNFA.Transition( trans[0] + 1, trans[1], trans[2] + 1 )
		starNFA.add(transit)
		#starNFA.add_transition( trans[0] + 1, trans[1], trans[2] + 1 )

	#copy in accept states
	for state in NFA1.accept:
		starNFA.add_accept( state + 1)
	
	#add new start state
	starNFA.states.add( 0 )

	#add epsilon transitions from accept to new start
	for state in starNFA.accept:
		starNFA.add_transition( state, '&', 1)

	#add transition to old start
	starNFA.add_transition( 0, '&', 1)
	starNFA.set_start( 0 )
	starNFA.add_accept( 0 )

	return starNFA

if __name__ == '__main__':
	#epsilon()
	m1 = NFA.read(open(sys.argv[1]))
	m2 = NFA.read(open(sys.argv[2]))
	mc = concat(m1, m2)
	mc.write(sys.stdout)

	#m = NFA.read(open(sys.argv[1]))
	#ms = star(m)
	#ms.write(sys.stdout)