import sys
import re
from parser import *

def stripper( data ):
	cleandata = ''
	#strip all whitespace
	for line in data:
		cleanline = line.split("//")
		cleandata = cleandata + cleanline[0]

	cleandata = re.sub('[\s+]','',cleandata)
	#print(cleandata)
	return(cleandata)


if __name__ == "__main__":
	if len(sys.argv) == 3:
		file = sys.argv[2]
		#read in file as single line
		with open(file, 'r') as myfile:
			data = myfile.readlines()

	if len(sys.argv) == 2:
		data = sys.argv[1]

	expression = stripper(data)

	length = len(expression)
	counter = 0
	parser = baseParser(expression, length, counter)
	M = parser.parseRegexp()

	print(M)

