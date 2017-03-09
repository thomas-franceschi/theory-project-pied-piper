#CP2
#Thomas Franceschi
#Kyle Williams

#import sys

class baseParser:
	def __init__(self, expression, length, counter):
		self.expression = expression 				#String being parsed
		self.length = length 						#Max range for token
		self.counter = counter 						#Token
		self.M = ''									#Output

	def parseRegexp(self):
		print('parseRegexp()')
		self.M = self.parseUnion()
		if self.counter + 1 == self.length:
			return self.M
		else:
			print('error in parseRegexp()')
			return self.M #ERROR

	def parseUnion(self):
		print('parseUnion()')
		self.M = self.parseConcat()
		if self.expression[self.counter + 1] == '|': 	#If next token is |
			print('found a |')
			self.counter = self.counter + 1 			#'read' |
			self.M = self.union(self.M, self.parseConcat())
		return self.M

	def parseConcat(self):
		print('parseConcat()')
		if self.counter + 1 == self.length or self.expression[self.counter + 1] == '|' or self.expression[self.counter + 1] == ')':
			print('found a ' + self.expression[self.counter+1])
			return self.epsilon()
		else:
			self.M = self.parseUnary()
			if self.counter < self.length and self.expression[self.counter + 1] != '|' and self.expression[self.counter + 1] != ')':
				self.M = self.concat(self.M, self.parseUnary())
			return self.M

	def parseUnary(self):
		print('parseUnary()')
		self.M = self.parsePrimary()
		if self.expression[self.counter+1] == '*':
			print('found a star')
			self.counter = self.counter + 1;		#read *
			return self.star(self.M)
		else:
			return self.M

	def parsePrimary(self):
		print('parsePrimary()')
		if self.expression[self.counter + 1] == '(':
			print('found a (')
			self.counter = self.counter + 1		#read (
			self.M = self.parseUnion()
			self.counter = self.counter + 1		#read )
			print('found a )')
			return self.M
		elif self.expression[self.counter + 1] == '@':
			print('found a @')
			self.counter = self.counter + 1		#read @
			return self.emptyset()
		elif self.expression[self.counter + 1] != '(' and self.expression[self.counter+1] != ')' and self.expression[self.counter + 1] != '*' and self.expression[self.counter + 1] != '|':
			self.counter = self.counter + 1		#read a
			a = self.expression[self.counter]
			print('found a: ' + a)
			return self.symbol(a)
		else:
			print('Error in parsePrimary()')
			return self.M #Error

	#Placeholders

	def emptyset(self):
		return 'emptyset()'

	def epsilon(self):
		return 'epsilon()'

	def symbol(self, a):
		return 'symbol(' + str(a) + ')'

	def union(self, M1, M2):
		return 'union(' + str(M1) + ',' + str(M2) + ')'

	def concat(self, M1,M2):
		return 'concat(' + str(M1) + ',' + str(M2) + ')'

	def star(self, M):
		return 'star(' + M + ')'

if __name__ == "__main__":
	
	expression = '(ab|a)*'
	length = len(expression)
	counter = 0
	parser = baseParser(expression, length, counter)
	M = parser.parseRegexp()

	print(M)