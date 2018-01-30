## Programs that manipulate the user database files used by the md380-tools firmware.

It currently contains only one program: merge_users.py.

### merge_users.py
merge_users.py takes a list of userdb files and merges them together.
Fields for each DMR ID found in later files take precedence.
In other words, as each file is processed, a field for a DMR ID is
updated only if that new field is non-empty.

Optionally, several other fixups are performed.  See the options early
in the source for merge_users.py

Examples:
	merge_users.py -o AbbrevCountries -o AbbrevStates myusers.csv marc.csv

	merge_users.py myusers.csv marc.csv --verbatim override.csv

A file given with the --verbatim option will have fields applied after
any fixups are performed.  In other words its fields will be placed in
the output without alteration.  This option is rarely, if ever, used.
