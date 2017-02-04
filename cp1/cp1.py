#!/usr/bin/env python2.7

# Kyle Williams and Thomas Franceschi

# -----------------------------------------------------------------------------------
class NFA(object):

	def __init__(self, states, alphabet, start, accept, transitions):
		self.states = states
		self.alphabet = alphabet
		self.start = start
		self.accept = accept
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
		nfa = nf.read()
	nf.closed

	# separate nfa components
	nfa = nfa.split('\n')

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
	transitions = {}
	for i in range(4, len(nfa) - 1):
		transitionList.append(nfa[i])

	for transition in transitionList:
		transition = transition.split(" ")

		# transitions[(start state, input symbol)] = end state
		transitions[(transition[0], transition[1])] = transition[2]

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
			nf.write(transition[0] + " " + transition[1] + " " + nfa.transitions[transition])
			nf.write("\n")

	nf.closed

# -----------------------------------------------------------------------------------
def singleton(w):
	# create alphabet from input string
	alphabet = list(w)

	# create list of states
	states =[]
	for i in range(len(alphabet) + 1):
		q = "q" + str(i)
		states.append(q)

	# start state
	start = states[0]

	# accept state
	accept = states[len(states) - 1]

	# create transitions from alphabet and states
	transitions = {}
	for i in range(len(alphabet)):
		transitions[(states[i], alphabet[i])] = states[i+1]

	# create nfa from input string
	nfa = NFA(states, alphabet, start, accept, transitions)
	return nfa;

if __name__ == "__main__":

	nfa = singleton("010")
	write_NFA(nfa, "./test.nfa")

	# nfa = read_NFA('../examples/empty2.nfa')

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
