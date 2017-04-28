#!/usr/bin/env python3

import sys
import re
from more_parser import *
from nft import *
from collections import deque
import parser

def file_stripper( data ):
	cleandata = ''
	#strip all whitespace
	for line in data:
		cleanline = line.split('//')
		cleandata = cleandata + cleanline[0]

	cleandata = re.sub('[\s+]','',cleandata)
	#print(cleandata)
	return(cleandata)

def string_stripper( data ):
	cleandata = ''
	cleanline = data.split('//')
	cleandata = cleandata + cleanline[0]

	cleandata = re.sub('[\s+]','',cleandata)
	#print(cleandata)
	return(cleandata)

def good_parser(expression):
	isLoop = False
	if len(expression) > 0:
		if expression[0] == '{':
			isLoop = True
			expression = expression.replace('{','')
			expression = expression.replace('}','')

	length = len(expression)
	counter = 0
	parser = baseParser(expression, length, counter)
	M = parser.parseRegexp()

	return( M,isLoop )

def dummy_parser(expression):
	isLoop = False
	if len(expression) > 0:
		if expression[0] == '{':
			isLoop = True
			expression = expression.replace('{','')
			expression = expression.replace('}','')

	length = len(expression)
	counter = 0
	myparser = parser.baseParser(expression, length, counter)
	M = myparser.parseRegexp()
	if isLoop:
		print('loop(' + M + ')')
	else:
		print(M)

	return( M,isLoop )

def run(program, w):
	
	A = deque([])
	Mw = NFT.singleton(w)
	A.append((Mw, 0))

	while len(A) > 0:
		M, i = A.popleft()
		#print(i)
		if NFT.any_path(M):
			if i == len(program):
				transitions = NFT.any_path(M)
				output = ''

				for t in transitions:
					if t.b is not '&':
						output = output + t.b

				print (output)
				return M
			elif program[i][1] == True: #islooping == true
				#print("looping")
				A.append((M, i+1))
				A.append((NFT.compose(M, program[i][0]), i))
			else:
				A.append((NFT.compose(M, program[i][0]), i+1))
	#return emptyset
	#print('emptyset')
	myNFT = NFT()
	myNFT.set_start('0')
	return myNFT

if __name__ == "__main__":
	if len(sys.argv) == 3:
		file = sys.argv[2]
		#read in file as single line
		with open(file, 'r') as myfile:
			data = myfile.readlines()
		expressions = file_stripper(data)

	if len(sys.argv) == 2:
		data = sys.argv[1]
		expressions = string_stripper(data)
	
	expressions = expressions.split(';')
	program = []

	for expression in expressions:
		program.append(good_parser(expression))

	while True:
		w = input()
		#print len(program)
		myNFT = run(program, w)
		#myNFT.write(sys.stdout)


