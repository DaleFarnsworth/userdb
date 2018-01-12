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
        "AbbrevStandard":	True,
	"MiscChanges":		True,
        "RemoveDupSurnames":	True,
        "RemoveMatchingNicks":	True,
        "RemoveRepeats":	True,
        "TitleCase":		True,

        "AbbrevCountries":	False,
        "AbbrevDirections":	False,
        "AbbrevStates":		False,
	"RemoveNames":		False,
}

standardAbbrevs = {
	"United States":	"US",
	"United Kingdom":	"UK",
	"Germany":		"DEU",
	"Australia":		"AUS",
	"Canada":		"CAN",
	"Italy":		"ITA",
	"Netherlands":		"NLD",
	"Belgium":		"BEL",
	"France":		"FRA",
	"Spain":		"ESP",
	"China":		"CN",
}

countryAbbrevs = {
	"Switzerland":		"CHE",
	"Austria":		"AUT",
	"Denmark":		"DNK",
	"Sweden":		"SWE",
	"Russia":		"RUS",
	"Poland":		"POL",
	"Luxembourg":		"LUX",
	"Portugal":		"PRT",
	"Ireland":		"IRL",
	"Greece":		"GRC",
	"Hungary":		"HUN",
	"Bosnia and Hercegovi":	"BIH",
	"Czech Republic":	"CZE",
	"Slovakia":		"SVK",
	"Norway":		"NOR",
	"Finland":		"FIN",
	"Taiwan":		"TAI",
	"Malaysia":		"MYS",
	"New Zealand":		"NZL",
	"Brazil":		"BRA",
}

stateAbbrevs = {
	"Alabama":		"AL",
	"Alaska":		"AK",
	"Arizona":		"AZ",
	"Arkansas":		"AR",
	"California":		"CA",
	"Colorado":		"CO",
	"Connecticut":		"CT",
	"Delaware":		"DE",
	"Florida":		"FL",
	"Georgia":		"GA",
	"Hawaii":		"HI",
	"Idaho":		"ID",
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
	"District of Columbia":	"DC",
	"Puerto Rico":		"PR",
}

directionAbbrevs = {
	"North":		"N.",
	"South":		"S.",
	"East":			"E.",
	"West":			"W.",
}


enable_options = [x for x in sorted(options)]
disable_options = ["No" + x for x in enable_options]

def cleanup_blanks(s):
	# remove leading and trailing blanks
	s = s.strip()

	# squeeze repeated blanks into a single blank
	while "  " in s:
		s = s.replace("  ", " ")

	return s

# Remove duplicated surnames
def removeDupSurnames(name):
	names = name.split()
	if len(names) > 2 and names[-2] == names[-1]:
		name = " ".join(names[:-1])

	return name

# if the entire field is repeated, eliminate the redundant repitition
def removeRepeats(s):
	fields = s.split()
	if len(fields) < 4 or len(fields) % 2 != 0:
		return s

	hlen = len(fields) / 2
	for i in range(hlen):
		if fields[i] != fields[i+hlen]:
			return s

	return " ".join(fields[:hlen])

# If a word is all caps, only capitalize the first letter
def titleCase(s):
	fields = s.split()
	for i, field in enumerate(fields):
		if len(field) < 3:
			continue

		all_upper = True
		for char in field:
			if char not in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
				all_upper = False
				break
				
		if all_upper:
			fields[i] = field.capitalize()

	return " ".join(fields)

# Abbreviate the cardinal directions
def abbrevDirections(s):
	fields = s.split(" ")

	abbrev = directionAbbrevs.get(field[0], "")
	if abbrev != "":
		field[0] = abbrev

	return " ".join(fields)

def massage_users():
	for dmr_id, user in users.iteritems():
		for key, val in user.iteritems():
			user[key] = cleanup_blanks(val)

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
			user["country"] = titleCase(user["country"])

		if options["RemoveMatchingNicks"]:
			first = user["name"].split(" ", 2)[0]
			if first == user["nick"]:
				user["nick"] = ""

		if options["RemoveNames"]:
			user["name"] = ""
			user["nick"] = ""

		if options["AbbrevStandard"]:
			abbrev = standardAbbrevs.get(user["country"], "")
			if abbrev != "":
				user["country"] = abbrev

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

		if options["MiscChanges"]:
			s = user["city"]
			if s.endswith(" (B,"):
				user["city"] = s[:-len(" (B")]

		users[dmr_id] = user

def do_line(line):
	if "," not in line:
		return
	line = line.strip("\n")
	dmr_id, call, name, city, state, nick, country = line.split(",")

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
		if user[key] == "":
			user[key] = val

	users[dmr_id] = user

def do_file(file):
	for line in file:
		do_line(line)

def main():
	parser = argparse.ArgumentParser(description="Merge userdb files")
	parser.add_argument("-o", nargs=1, dest="options",
		action="append", choices=enable_options + disable_options)

	parser.add_argument("files", metavar="filename", nargs="*",
		type=argparse.FileType("r"), help="a filename to be merged")
	args = parser.parse_args()

	if args.options != None:
		for opt in args.options:
			for opt in opt:
				if opt in enable_options:
					options[opt] = True
				elif opt in disable_options:
					options[opt[2:]] = False

	for file in args.files:
		do_file(file)

	massage_users()

	for i, u in sorted([(int(i), u) for i, u in users.iteritems()]):
		line = "{0},{1},{2},{3},{4},{5},{6}".format(
			u["id"], u["call"], u["name"], u["city"], u["state"],
			u["nick"], u["country"])

		print(line)

if __name__ == '__main__':
	main()
