import os
import re

from os import listdir
from os.path import isfile, join
import glob, os

# Parse raw_country_code_data to generate mapping of
# countries to their two digit country codes
def TwoDigitCountryCodes():
	with open("raw_country_code_data.txt") as f:
		lines = f.readlines()
	lines = [l.strip('"\n\'') for l in lines]

	output = 'var CodeLookup = {'

	for line in lines:
		i = line.index('/')
		country = line[:re.search("\d", line).start()-1]
		code = line[i-3:i-1]

		output += '"' + country + '": ' + '"' + code + '", '

	output = output[:-2] + '};'
	print(output)

# Parse 2016EPI_Indicator_Key_KAI to generate HTML drop down menu of indicators
# Used by select2 for user input of countries
def GenerateIndicatorsHTML():
	with open('../RawData/2016EPI_Indicator_Key_KAI.csv') as f:
		lines = f.readlines()
	lines = [l.strip('"\n\'') for l in lines]
	lines = lines[1:]

	output = ''

	for line in lines:
		line = line.split(',')
		line[3] = line[3].replace('.', '_')
		# <option value="ACCESS">Access to Electricity</option>
		output += '<option value="' + line[3] + '">' + line[1] + '</option>\n'

	print(output)

# Parse 2016EPI_Indicator_Key_KAI to generate a JS variable
# that maps indicators to corresponding JS variables that contain 
# data for the world map
def GenerateMapLookupVariable():
	with open('../RawData/2016EPI_Indicator_Key_KAI.csv') as f:
		lines = f.readlines()
	lines = [l.strip('"\n\'') for l in lines]
	lines = lines[1:]

	output = 'var map_lookup = {'

	for line in lines:
		line = line.split(',')
		line[3] = line[3].replace('.', '_')
		# "ACCESS":ACCESS_MAP,
		output += '"' + line[3].replace('.', '_') + '":' + line[3] + '_MAP, '

	output = output[:-2] + '};'

	print(output)


# Generate HTML code for the drop down menu of countries
# Used by the Select2 drop down box to take user input of countries
def GenerateCountryCodeHTML():
	with open("../RawData/countrylist_EPI_2016.csv") as f:
		countries = f.readlines()

	# remove first value = 'x'
	countries = countries[1:]
	# countries is of the 180 countries that are in the EPI
	# only countries in this list should have their data output
	countries = [c.strip('"\n\'') for c in countries]

	# generate the select list for the html drop down menu
	select_output = ''

	for c in countries:
		# <option value="Afghanistan">Afghanistan</option>
		select_output += '<option value="' + c + '">'
		select_output += c + '</option>\n'
	print(select_output)


GenerateMapLookupVariable()
# GenerateIndicatorsHTML()
# GenerateCountryCodeHTML()
exit(0)


# lower_2007 is 3
# lower_2008 is 6
csv_files = []

for file in glob.glob("*.csv"):
    csv_files.append(file)

output = ''
# var line_lookup = {"ACCESS" : ACCESS, "CLIMATE" : CLIMATE};
line_lookup = 'var line_lookup = {'

# // var ACCESS = {"Afghanistan" : {}, "China" : {}};
# // var CLIMATE = {"Afghanistan" : {}, "China" : {}};



for file in csv_files:
	# counter for the number of countries that are rejected 
	# per indicator's csv
	reject_counter = 0

	# remove the '.csv' from the end of the file name
	indicator = file[:-4].replace('.', '_')

	# "ACCESS : ACCESS, "
	line_lookup += '"' + indicator + '" : ' + indicator + ', '

	# var ACCESS = {
	output += 'var ' + indicator + ' = { '

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

		if (line[3].strip('"') not in countries):
			reject_counter += 1
			continue

		# "Afghanistan : {"
		output += '"' + str(line[3].strip('"')) +'" : {'

		output += '"code": ' + str(line[1].strip('"')) + ','
		output += '"iso": "' + str(line[2].strip('"')) + '",'
		output += '"country": "' + str(line[3].strip('"')) + '",'

		ranges = '"ranges":['
		i = 4
		year = 2007
		# if all averages for the given line are NA, flag value is 1 after loop
		# if at least one valid average value, flag value is 0 after loop
		all_missing_flag = 1

		while i < 34:

			if line[i] == 'NA':
				i += 3
				continue

			ranges += '[' + str(year) + ', ' + str(line[i]) + ', ' + str(line[i+2]) + '],'
			i += 3
			year += 1
			all_missing_flag = 0

		if all_missing_flag == 0:
			ranges = ranges[:-1]

		ranges += '],'
		output += ranges

		# "averages":[[2007, 21.5],[2008, 22.1]]}]

		averages = '"averages":['
		i = 5
		year = 2007
		# if all averages for the given line are NA, flag value is 1 after loop
		# if at least one valid average value, flag value is 0 after loop
		all_missing_flag = 1

		while i < 33:

			if line[i] == 'NA':
				i += 3
				continue

			averages += '[' + str(year) + ', ' + line[i] + '],'
			i += 3
			year += 1
			all_missing_flag = 0

		# remove trailing ',' only if at least one value was added to averages
		if all_missing_flag == 0:
			averages = averages[:-1]

		averages += ']'
		output += averages + '},'
		# break

	output = output[:-1] + ' };\n'
	# print(output)
	# print('\n')
	# print(line)
	if (reject_counter != 54):
		print("error! more than 54 countries were rejected")
		break

line_lookup = line_lookup[:-2] + '};'

# output = output[:-2]
# output += '};'

print(output)
print(line_lookup)
