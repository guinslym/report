import json
import datetime
from dateutil import parser


lines = [line.rstrip('\n') for line in open('downtime.csv')]

content =[]
for line in lines:
	line = line.split(',')
	line = line[1]
	#dt = parser.parse("line")
	print(line)
