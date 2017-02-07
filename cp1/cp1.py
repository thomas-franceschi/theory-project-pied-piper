#!/usr/bin/env python2.7

# Kyle Williams and Thomas Franceschi

# TODO

# source ~lsyers/Pub/.cshrc

	# test scripts for singleton, emptiness, and intersection

# Questions

	# empty language for "empty1.nfa"

import re
import Queue

# -----------------------------------------------------------------------------------
class NFA(object):
	def __init__(self, states, alphabet, start, accept, transitions):
		self.states = states
		self.alphabet = alphabet
		self.start = start
		self.accept = accept

		# check for valid transitions before adding transitions dict to nfa object
		for transition in transitions:
			if transition[0] not in self.states:
				print("Error: " + transition[0] + " not a valid state")
				raise ValueError
			if transition[2] not in self.states:
				print("Error: " + transition[2] + " not a valid state")
				raise ValueError
			if transition[1] not in self.alphabet and transition[1] is not "&":
				print("Error: " + transition[1] + " not a valid symbol")
				raise ValueError

		self.transitions = transitions

	# add new transition
	def addTransition(self, q, a, r):
		if q not in self.states:
			print("Error: " + q + " not a valid state")
			return
		if r not in self.states:
			print("Error: " + r + " not a valid state")
			return
		if a not in self.alphabet:
			print("Error: " + a + " not a valid symbol")
			return
		self.transitions[(q, a)] = r;

	# iterate over all states
	def showStates(self):
		for state in self.states:
			print state

	# iterate over all input symbols
	def showInputSymbols(self):
		for symbol in self.alphabet:
			print symbol

	# iterate over transitions out of state q
	def showTransitionsQ(self, q):
		for transition in self.transitions:
			if q == transition[0]:
				print transition

	# iterate over transitions on input symbol a
	def showTransitionsA(self, a):
		for transition in self.transitions:
			if a == transition[1]:
				print transition

# -----------------------------------------------------------------------------------
def read_NFA(filename):
	with open(filename, 'r') as nf:
		raw_nfa = nf.read()
	nf.closed

	# separate nfa components
	raw_nfa = raw_nfa.split('\n')

	# sanitize nfa of comments
	nfa = []
	for line in raw_nfa:
		line = re.sub('\s*//.*', '', line)
		nfa.append(line)

	# parse states
	states = nfa[0].split(" ")

	# parse alphabet
	alphabet = nfa[1].split(" ")

	# parse start state
	start = nfa[2]

	# parse accept states
	accepts = nfa[3].split(" ")

	# parse transitions
	transitionList = []
	transitions = []
	for i in range(4, len(nfa) - 1):
		transitionList.append(nfa[i])

	for transition in transitionList:
		transition = transition.split(" ")
		transitions.append((transition[0], transition[1], transition[2]))

	nfa = NFA(states, alphabet, start, accepts, transitions)
	return nfa;

def write_NFA(nfa, filename):
	with open(filename, 'w') as nf:
	
		# write list of states
		for state in nfa.states:
			nf.write(state + " ")

		nf.write("\n")

		# write symbols in alphabet
		for symbol in nfa.alphabet:
			nf.write(symbol + " ")

		nf.write("\n")

		# write start state
		nf.write(nfa.start)

		nf.write("\n")

		# write list of accept states
		for accept in nfa.accept:
			nf.write(accept + " ")

		nf.write("\n")

		# write transitions
		for transition in nfa.transitions:
			# current state + input symbol + next state
			nf.write(transition[0] + " " + transition[1] + " " + transition[2])
			nf.write("\n")

	nf.closed

# -----------------------------------------------------------------------------------
def singleton(w):
	# create alphabet from input string
	alphabet = list(w)

	# create list of states
	states = []
	for i in range(len(alphabet) + 1):
		q = "q" + str(i)
		states.append(q)

	# start state
	start = states[0]

	# accept state
	accept = []
	accept.append(states[len(states) - 1])

	# create transitions from alphabet and states
	transitions = []
	for i in range(len(alphabet)):
		transitions.append((states[i], alphabet[i], states[i+1]))

	# create nfa from input string
	nfa = NFA(states, alphabet, start, accept, transitions)
	return nfa;

# -----------------------------------------------------------------------------------
def emptiness(nfa):
	# check to see if the nfa has any accept states
	if " " in nfa.accept:
		return True

	frontier = Queue.Queue()
	marked = []

	# add start state to queue
	frontier.put(nfa.start)

	while not frontier.empty():
		# get current state
		v = frontier.get()

		# check if algorithm has already been in current state 
		if v in marked:
			continue
		
		# check if current state is an accept state
		if v in nfa.accept:
			return False

		# add current state to marked
		marked.append(v)

		# iterate through other transitions to add to queue
		for transition in nfa.transitions:
			frontier.put(transition[2])

	return True

# -----------------------------------------------------------------------------------
def intersection(nfa1, nfa2):
	# cross product of states
	states = []
	for q in nfa1.states:
		for r in nfa2.states:
			states.append((q, r))

	# intersection of alphabets
	alphabet = []
	for symbol in nfa1.alphabet:
		if symbol in nfa2.alphabet:
			alphabet.append(symbol)

	# start state tuple
	start = (nfa1.start, nfa2.start)

	# cross product of accept states
	accept = []
	for state in states:
		# if either state is an accept state in either list
		if state[0] in nfa1.accept or state[1] in nfa2.accept:
			accept.append(state)

	# determine transitions
	

	print states
	print alphabet
	print start
	print accept

if __name__ == "__main__":

	nfa1 = read_NFA("./test.nfa")
	nfa2 = read_NFA("./test2.nfa") 

	intersection(nfa1, nfa2)

	# nfa = read_NFA("../examples/sipser-n1.nfa")
	# write_NFA(nfa, "./test-com.nfa")

	# nfa = singleton("010")
	# write_NFA(nfa, "./test-singleton.nfa")

	# nfa = read_NFA("../examples/empty2.nfa")
	# print emptiness(nfa)

	# nfa = read_NFA('../examples/empty2.nfa')

	# nfa = read_NFA('./test.nfa')

	# print("states")
	# nfa.showStates()

	# print("symbols")
	# nfa.showInputSymbols()

	# print("transitions q")
	# nfa.showTransitionsQ("q1")

	# print("transitions a")
	# nfa.showTransitionsA("a")

	# print("add transition q")
	# nfa.addTransition("q1", "a", "q2")	
	# print("transition q")
	# nfa.showTransitionsQ("q1")

	# print("transition a")

	# nfa.showTransitionsA("a")

	# write_NFA(nfa, "./test.nfa")
