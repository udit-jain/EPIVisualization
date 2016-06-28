import os
import re

from os import listdir
from os.path import isfile, join
import glob, os



# lower_2007 is 3
# lower_2008 is 6
csv_files = []

for file in glob.glob("*.csv"):
    csv_files.append(file)

output = 'var AllData = {'

for file in csv_files:

	# remove the '.csv' from the end of the file name
	indicator = file[:-4]

	# "ACCESS" : {"Afghanistan_ACCESS" ... }
	output += '"' + indicator + '" : { '

	with open(file) as f:
	    content = f.readlines()

	# remove the first empty row
	content = content[1:]



	# process all the rows in one csv
	for line in content:
		line = line.strip('[\n,"]').split(',')

		# to catch the last line of every csv which is just empty
		if (line[1] == 0):
			continue

		output += '"' + str(line[3].strip('"')) + '_' + indicator + '" : {'

		output += '"code": ' + str(line[1].strip('"')) + ','
		output += '"iso": "' + str(line[2].strip('"')) + '",'
		output += '"country": "' + str(line[3].strip('"')) + '",'

		ranges = '"ranges":['
		i = 4
		year = 2007

		while i < 34:
			ranges += '[' + str(year) + ', ' + str(line[i]) + ', ' + str(line[i+2]) + '],'
			i += 3
			year += 1

		ranges = ranges[:-1]
		ranges += '],'
		output += ranges

		# "averages":[[2007, 21.5],[2008, 22.1]]}]

		averages = '"averages":['
		i = 5
		year = 2007
		while i < 33:
			averages += '[' + str(year) + ', ' + line[i] + '],'
			i += 3
			year += 1

		averages = averages[:-1]
		averages += ']'
		output += averages + '},'

	output = output[:-1] + ' }, '

	# print(output)
	# print('\n')
	# print(line)

output = output[:-2]
output += '};'

print(output)

