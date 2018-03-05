VERSION=$(shell sed -n -E '/version = /s/.*"(.*)".*/\1/p' merge_users.py)

default:

tag:
	git tag -s -m "editcp v$(VERSION)" v$(VERSION)

