# CP3
# Thomas Franceschi
# Kyle Williams

class baseParser:
	def __init__(self, expression, length, counter):
		self.expression = expression 				#String being parsed
		self.length = length 						#Max range for token
		self.counter = counter 						#Token
		self.M = ''									#Output

	def parseRegexp(self):
		self.M = self.parseTransduce()
		if self.counter == self.length:
			return self.M
		else:
			print('regex error, count: ' + str(self.counter) + ' length: ' + str(self.length))
			print(self.M)
			return 1 #ERROR

	# Parse transduction
	def parseTransduce(self):
		self.M = self.parseUnion()
		if self.counter == self.length:
			return self.M
		if self.expression[self.counter] == ':':
			self.counter = self.counter + 1
			self.M = self.transduce(self.M, self.parseUnion())
		return self.M

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
		if self.expression[self.counter] == '|' or self.expression[self.counter] == ')' or self.expression[self.counter] == ':':
			return self.epsilon()
		else:
			self.M = self.parseUnary()
			while self.counter < self.length and self.expression[self.counter] != '|' and self.expression[self.counter] != ')' and self.expression[self.counter] != ':':
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
			self.M = self.parseTransduce()
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

	# CP3 Additions
	def transduce(self, M1, M2):
		return 'transduce(' + str(M1) + ',' + str(M2) + ')'

if __name__ == "__main__":
	
	#expression = '(ab|a)*'
	length = len(expression)
	counter = 0
	parser = baseParser(expression, length, counter)
	M = parser.parseRegexp()

	print(M)