#!/usr/bin/env python2
# -*- coding: utf-8 -*-

# This program takes a list of userdb files and merges them together.
# Fields for each DMR ID found in earlier files take precedence.
# In other words, as each file is processed, a field for a DMR ID is
# updated only if that field has not been set by a previous file.

# Optionally, several other fixups are performed.  See the options below.

# Author: Dale Farnsworth dale@farnsworth.org

# MIT License
#
# Copyright 2018 Dale Farnsworth
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from __future__ import print_function

import sys
import argparse

users = {}

options = {
	"MiscChanges":		True,
	"RemoveDupSurnames":	True,
	"RemoveMatchingNick":	True,
	"RemoveRepeats":	True,
	"TitleCase":		True,
	"RemoveCallFromNick":	True,
	"FixRomanNumerals":	True,
	"FixStateCountries":	True,

	"AbbrevCountries":	False,
	"AbbrevDirections":	False,
	"AbbrevStates":		False,
	"RemoveNames":		False,
}

countryAbbrevs = {
	"Andorra":			"AD",
	"Argentina":			"AR",
	"Argentina Republic":		"AR",
	"Australia":			"AU",
	"Austria":			"AT",
	"Barbados":			"BB",
	"Belgium":			"BE",
	"Belize":			"BZ",
	"Bosnia and Hercegovi":		"BA",
	"Bosnia and Hercegovina":	"BA",
	"Brazil":			"BR",
	"Bulgaria":			"BG",
	"Canada":			"CA",
	"Chile":			"CL",
	"China":			"CN",
	"Colombia":			"CO",
	"Costa Rica":			"CR",
	"Croatia":			"HR",
	"Cyprus":			"CY",
	"Czech Republic":		"CZ",
	"Denmark":			"DK",
	"Dominica":			"DM",
	"Dominican Republic":		"DO",
	"Ecuador":			"EC",
	"Estonia":			"EE",
	"Finland":			"FI",
	"France":			"FR",
	"Germany":			"DE",
	"Greece":			"GR",
	"Guatemala":			"GT",
	"Haiti":			"HT",
	"Hong Kong":			"HK",
	"Hungary":			"HU",
	"India":			"IN",
	"Indonesia":			"ID",
	"Ireland":			"IE",
	"Israel":			"IL",
	"Italy":			"IT",
	"Japan":			"JP",
	"Korea":			"KR",
	"Korea S":			"KR",
	"Kuwait":			"KW",
	"Latvia":			"LV",
	"Liechtenstein":		"LI",
	"Luxembourg":			"LU",
	"Luxemburg":			"LU",
	"Macedonia":			"MK",
	"Malaysia":			"MY",
	"Malta":			"MT",
	"Mexico":			"MX",
	"Montenegro":			"ME",
	"Netherlands Antilles":		"AN",
	"Netherlands":			"NL",
	"New Zealand":			"NZ",
	"Norway":			"NO",
	"Panama":			"PA",
	"Paraguay":			"PY",
	"Philippines":			"PH",
	"Poland":			"PL",
	"Portugal":			"PT",
	"Qatar":			"QA",
	"Reunion":			"RE",
	"Romania":			"RO",
	"Russia":			"RU",
	"Serbia":			"RS",
	"Singapore":			"SG",
	"Slovakia":			"SK",
	"Slovenia":			"SI",
	"South Africa":			"ZA",
	"Spain":			"ES",
	"Sweden":			"SE",
	"Switzerland":			"CH",
	"Taiwan":			"TW",
	"Thailand":			"TH",
	"Trinidad and Tobago":		"TT",
	"Turkey":			"TR",
	"Ukraine":			"UA",
	"United Kingdom":		"UK",
	"United States":		"US",
	"Uruguay":			"UY",
	"Venezuela":			"VE",
}

stateAbbrevsByCountry = {
	"United States": {
		"Alabama":		"AL",
		"Alaska":		"AK",
		"Arizona":		"AZ",
		"Arkansas":		"AR",
		"California":		"CA",
		"Colorado":		"CO",
		"Connecticut":		"CT",
		"Delaware":		"DE",
		"District of Columbia": "DC",
		"Florida":		"FL",
		"Georgia":		"GA",
		"Hawaii":		"HI",
		"Idaho":		"ID",
		"Illinois":		"IL",
		"Indiana":		"IN",
		"Iowa":			"IA",
		"Kansas":		"KS",
		"Kentucky":		"KY",
		"Louisiana":		"LA",
		"Maine":		"ME",
		"Maryland":		"MD",
		"Massachusetts":	"MA",
		"Michigan":		"MI",
		"Minnesota":		"MN",
		"Mississippi":		"MS",
		"Missouri":		"MO",
		"Montana":		"MT",
		"Nebraska":		"NE",
		"Nevada":		"NV",
		"New Hampshire":	"NH",
		"New Jersey":		"NJ",
		"New Mexico":		"NM",
		"New York":		"NY",
		"North Carolina":	"NC",
		"North Dakota":		"ND",
		"Ohio":			"OH",
		"Oklahoma":		"OK",
		"Oregon":		"OR",
		"Pennsylvania":		"PA",
		"Puerto Rico":		"PR",
		"Rhode Island":		"RI",
		"South Carolina":	"SC",
		"South Dakota":		"SD",
		"Tennessee":		"TN",
		"Texas":		"TX",
		"Utah":			"UT",
		"Vermont":		"VT",
		"Virginia":		"VA",
		"Washington":		"WA",
		"West Virginia":	"WV",
		"Wisconsin":		"WI",
	},
	"Canada": {
		"Alberta":		"AB",
		"British Columbia":	"BC",
		"Manitoba":		"MB",
		"New Brunswick":	"NB",
		"Newfoundland":		"NL",
		"Nova Scotia":		"NS",
		"Ontario":		"ON",
		"Prince Edward Island":	"PE",
		"Quebec":		"QC",
		"Saskatchewan":		"SK",
		"Yukon":		"YT",
	},
	"Australia": {
		"Australian Capital Territory": "ACT",
		"New South Wales":		"NSW",
		"Northern Territory":		"NT",
		"Queensland":			"QLD",
		"South Australia":		"SA",
		"Tasmania":			"TAS",
		"Victoria":			"VIC",
		"Western Australia":		"WAU",
	},
}

directionAbbrevs = {
	"North":		"N.",
	"South":		"S.",
	"East":			"E.",
	"West":			"W.",
}

enable_options = [x for x in sorted(options)]
disable_options = ["No" + x for x in enable_options]

def cleanup_blanks(field):
	# remove leading and trailing blanks
	field = field.strip()

	# squeeze repeated blanks into a single blank
	while "  " in field:
		field = field.replace("  ", " ")

	return field

# Remove duplicated surnames
def removeDupSurnames(field):
	words = field.split()
	if len(words) > 2 and words[-2] == words[-1]:
		field = " ".join(words[:-1])

	return field

# if the entire field is repeated, eliminate the redundant repitition
def removeRepeats(field):
	words = field.split()
	if len(words) < 4 or len(words) % 2 != 0:
		return field

	hlen = len(words) / 2
	for i in range(hlen):
		if words[i] != words[i+hlen]:
			return field

	return " ".join(words[:hlen])

# If a word is all caps, only capitalize the first letter
def titleCase(field):
	words = field.split()
	for i, word in enumerate(words):
		if len(word) < 4:
			continue

		all_upper = True
		for char in word:
			if char not in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
				all_upper = False
				break

		if all_upper:
			words[i] = word.capitalize()

	return " ".join(words)

# Abbreviate the cardinal directions
def abbrevDirections(field):
	words = field.split(" ")

	abbrev = directionAbbrevs.get(words[0], "")
	if abbrev != "":
		words[0] = abbrev

	return " ".join(words)

def removeSubstr(field, subfield):
	index = field.upper().find(subfield.upper())
	if index >= 0:
		field = field[:index] + field[index+len(subfield):]

	return field

def fixRomanNumerals(field):
	if len(field) < 3:
		return field

	if field[-1] == "i":
		if field.endswith(" Ii"):
			field = field[:-1] + "I"
		elif field.endswith(" Iii"):
			field = field[:-2] + "II"
	elif field[-1] == "v":
		if field.endswith(" Iv"):
			field = field[:-1] + "V"

	return field

def fixStateCountries(user):
	for country, abbrevStates in stateAbbrevsByCountry.iteritems():
		for state in abbrevStates:
			if user["country"] == state:
				if user["state"] == "":
					user["state"] = state
				user["country"] = country
	return user

def massage_users():
	stateAbbrevs = {}
	for _, abbrevStates in stateAbbrevsByCountry.iteritems():
		stateAbbrevs.update(abbrevStates)

	for dmr_id, user in users.iteritems():
		# remove blanks from within callsigns
		user["call"] = user["call"].replace(" ", "")

		if options["RemoveDupSurnames"]:
			user["name"] = removeDupSurnames(user["name"])

		if options["RemoveRepeats"]:
			for key, val in user.iteritems():
				user[key] = removeRepeats(val)

		if options["TitleCase"]:
			user["name"] = titleCase(user["name"])
			user["city"] = titleCase(user["city"])
			user["state"] = titleCase(user["state"])
			user["nick"] = titleCase(user["nick"])
			user["country"] = titleCase(user["country"])

		if options["RemoveMatchingNick"]:
			first = user["name"].split(" ", 2)[0]
			if first == user["nick"]:
				user["nick"] = ""

		if options["RemoveNames"]:
			user["name"] = ""
			user["nick"] = ""

		if options["FixStateCountries"]:
			user = fixStateCountries(user)

		if options["AbbrevCountries"]:
			abbrev = countryAbbrevs.get(user["country"], "")
			if abbrev != "":
				user["country"] = abbrev

		if options["AbbrevStates"]:
			abbrev = stateAbbrevs.get(user["state"], "")
			if abbrev != "":
				user["state"] = abbrev

		if options["AbbrevDirections"]:
			user["city"] = abbrevDirections(user["city"])
			user["state"] = abbrevDirections(user["state"])

		if options["RemoveCallFromNick"]:
			user["nick"] = removeSubstr(user["nick"], user["call"])

		if options["MiscChanges"]:
			field = user["city"]
			if field.endswith(" (B,"):
				user["city"] = field[:-len(" (B")]

		if options["FixRomanNumerals"]:
			user["name"] = fixRomanNumerals(user["name"])

		for key, val in user.iteritems():
			user[key] = cleanup_blanks(val)

		users[dmr_id] = user

def read_user_line(file, i, line):
	if i == 1 and "," not in line:
		try:
			int(line)
			return
		except ValueError:
			pass

	line = line.strip("\n")

	if line == "":
		print("{0}:{1} Empty line.".format(file.name, i),
			file=sys.stderr)
		return

	fields = line.split(",")

	try:
		int(fields[0])
	except ValueError:
		print("{0}:{1} Non-numeric first value (DMR ID): {2}".format(
			file.name, i, line), file=sys.stderr)
		return

	if len(fields) != 7:
		if len(fields) < 7:
			err = "{0}:{1} Too few values ({2}): {3}".format(
				file.name, i, len(fields), line)
			fields += ["", "", "", "", "", "", ""]
		else:
			err = "{0}:{1} Too many values ({2}): {3}".format(
				file.name, i, len(fields), line)

		fields = fields[:7]
		print(err, file=sys.stderr)

	dmr_id, call, name, city, state, nick, country = fields

	new_user = {
		"call": call,
		"name": name,
		"city": city,
		"state": state,
		"nick": nick,
		"country": country,
	}

	blank_user = {
		"id": dmr_id,
		"call": "",
		"name": "",
		"city": "",
		"state": "",
		"nick": "",
		"country": "",
	}

	user = users.get(dmr_id, blank_user)

	for key, val in new_user.iteritems():
		if val != "":
			user[key] = val

	users[dmr_id] = user

def process_args():
	parser = argparse.ArgumentParser(description="Merge userdb files")
	parser.add_argument("-o", nargs=1, dest="options",
		action="append", choices=enable_options + disable_options)

	parser.add_argument("--verbatim", nargs=1, dest="verbatim",
		action="append", type=argparse.FileType("r"),
		help="a filename to be merged without modification")

	parser.add_argument("files", metavar="filename", nargs="*",
		type=argparse.FileType("r"), help="a filename to be merged")

	args = parser.parse_args()

	if args.options != None:
		for opts in args.options:
			for opt in opts:
				if opt in enable_options:
					options[opt] = True
				elif opt in disable_options:
					options[opt[2:]] = False

	verbatim = []
	if args.verbatim != None:
		for files in args.verbatim:
			verbatim += files
	args.verbatim = verbatim


	return args

def read_user_files(files):
	for file in files:
		i = 1
		for line in file:
			read_user_line(file, i, line)
			i += 1

def output_users():
	for i, u in sorted([(int(i), u) for i, u in users.iteritems()]):
		line = "{0},{1},{2},{3},{4},{5},{6}".format(
			u["id"], u["call"], u["name"], u["city"], u["state"],
			u["nick"], u["country"])

		print(line)

def main():
	args = process_args()
	read_user_files(args.files)
	massage_users()
	read_user_files(args.verbatim)
	output_users()

if __name__ == '__main__':
	main()
