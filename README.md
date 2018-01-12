## Programs that manipulate the user database files used by the md380-tools firmware.

It currently contains only one program: merge_users.py.

### merge_users.py
merge_users.py takes a list of userdb files and merges them together.
Fields for each DMR ID found in earlier files take precedence.
In other words, as each file is processed, a field for a DMR ID is
updated only if that field has not been set by a previous file.

Optionally, several other fixups are performed.  See the options early
in the source for merge_users.py
