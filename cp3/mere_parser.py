#CP2
#Thomas Franceschi
#Kyle Williams

import sys
from nfa import *

class baseParser:
	def __init__(self, expression, length, counter):
		self.expression = expression 				#String being parsed
		self.length = length 						#Max range for token
		self.counter = counter 						#Token
		self.M = ''									#Output

	def parseRegexp(self):
		self.M = self.parseUnion()
		if self.counter == self.length:
			return self.M
		else:
			print('regex error, count: ' + str(self.counter) + ' length: ' + str(self.length))
			return 1 #ERROR

	def parseUnion(self):
		self.M = self.parseConcat()
		if self.counter == self.length:
			return self.M
		if self.expression[self.counter] == '|': 			#If next token is |
			self.counter = self.counter + 1 				#'read' |
			self.M = self.union(self.M, self.parseConcat())
		return self.M

	def parseConcat(self):
		if self.counter == self.length:
			return self.epsilon()
		if self.expression[self.counter] == '|' or self.expression[self.counter] == ')':
			return self.epsilon()
		else:
			self.M = self.parseUnary()
			while self.counter < self.length and self.expression[self.counter] != '|' and self.expression[self.counter] != ')':
				self.M = self.concat(self.M, self.parseUnary())
			return self.M

	def parseUnary(self):
		self.M = self.parsePrimary()
		if self.counter == self.length:
			return self.M
		if self.expression[self.counter] == '*':	
			self.counter = self.counter + 1;		#read *
			return self.star(self.M)
		else:
			return self.M

	def parsePrimary(self):
		if self.expression[self.counter] == '(':
			self.counter = self.counter + 1		#read (
			self.M = self.parseUnion()
			self.counter = self.counter + 1		#read )
			return self.M
		elif self.expression[self.counter] == '@':
			self.counter = self.counter + 1		#read @
			return self.emptyset()
		elif self.expression[self.counter] != '(' and self.expression[self.counter] != ')' and self.expression[self.counter] != '*' and self.expression[self.counter] != '|':
			a = self.expression[self.counter]
			self.counter = self.counter + 1
			return self.symbol(a)
		else:
			print('parse primary error')
			return 1 #Error

	def emptyset(self):
		myNfa = NFA()
		myNfa.set_start(0)
		return myNfa

	def epsilon(self):
		myNfa = NFA()
		myNfa.set_start(0)
		myNfa.add_accept(1)
		myNfa.add_transition(0, '&', 1)
		return myNfa

	def symbol(self, a):
		myNfa = NFA()
		myNfa.set_start(0)
		myNfa.add_accept(1)
		myNfa.add_transition(0, a, 1)
		return myNfa

	def union(self, M1, M2):
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
		for trans in NFA2.transitions:
			transit = uNFA.Transition( trans[0] + offset, trans[1], trans[2] + offset )
			uNFA.add(transit)

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

	def concat(self, M1, M2):
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

	def star(self, M):
		starNFA = NFA()
		NFA1 = M

		#copy in states
		for state in NFA1.states:
			starNFA.states.add( state + 1 )

		#copy in transitions
		for trans in NFA1.transitions:
			transit = starNFA.Transition( trans[0] + 1, trans[1], trans[2] + 1 )
			starNFA.add(transit)
			
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

