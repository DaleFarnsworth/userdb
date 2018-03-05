## Programs that manipulate the user database files used by the md380-tools firmware.

It currently contains only one program: merge_users.py.

### merge_users.py
merge_users.py takes a list of userdb files and merges them together.
Fields for each DMR ID found in later files take precedence.
In other words, as each file is processed, a field for a DMR ID is
updated only if that new field is non-empty.

Optionally, several other fixups are performed.  See the output of
merge_users.py.

```
merge_users.py [-h] [--abbrevCountries] [--noAbbrevCountries]
                      [--abbrevDirections] [--noAbbrevDirections]
                      [--abbrevStates] [--noAbbrevStates] [--fixRomanNumerals]
                      [--noFixRomanNumerals] [--fixStateCountries]
                      [--noFixStateCountries] [--miscChanges]
                      [--noMiscChanges] [--removeCallFromNick]
                      [--noRemoveCallFromNick] [--removeDupSurnames]
                      [--noRemoveDupSurnames] [--removeMatchingNick]
                      [--noRemoveMatchingNick] [--removeRepeats]
                      [--noRemoveRepeats] [--titleCase] [--noTitleCase]
                      [--header] [--noHeader] [--removeNames]
                      [--noRemoveNames] [--config configfilename]
                      [--verbatim filename [filename ...]] [-v] [--debug]
                      [--version] [--excludeID filename [id[-id] ...]]
                      [--includeID filename [id[-id] ...]]
                      [--excludeCountry filename [countryname ...]]
                      [--includeCountry filename [countryname ...]]
                      filename [filename ...]

positional arguments:
  filename              A filename to be merged. Files are merged in the order
                        that they are named in this list. Fields from later
                        files take precedence over (replace) those of previous
                        files.

optional arguments:
  -h, --help            show this help message and exit
  --abbrevCountries     Abbreviate country names.
  --noAbbrevCountries   Do not abbreviate country names.
  --abbrevDirections    Abbreviate directions.
  --noAbbrevDirections  Do not abbreviate directions.
  --abbrevStates        Abbreviate state and province names.
  --noAbbrevStates      Do not abbreviate state and province names.
  --fixRomanNumerals    Fix case on roman numerals. Changes mixed-case roman
                        numerals at the end of the name field into upper case.
  --noFixRomanNumerals  Do not fix case on roman numerals. Changes mixed-case
                        roman numerals at the end of the name field into upper
                        case.
  --fixStateCountries   Fix US state name found in country field.
  --noFixStateCountries
                        Do not fix US state name found in country field.
  --miscChanges         Do Miscellaneous cleanups.
  --noMiscChanges       Do not do Miscellaneous cleanups.
  --removeCallFromNick  Remove callsign from nickname field
  --noRemoveCallFromNick
                        Do not remove callsign from nickname field
  --removeDupSurnames   Remove duplicated surname found at the end of the name
                        field.
  --noRemoveDupSurnames
                        Do not remove duplicated surname found at the end of
                        the name field.
  --removeMatchingNick  Remove nicknames that are the same as the first name
                        in the name field.
  --noRemoveMatchingNick
                        Do not remove nicknames that are the same as the first
                        name in the name field.
  --removeRepeats       Remove duplicated phrase in a field. If a field
                        consists entirely of a duplicated phrase, one copy is
                        removed.
  --noRemoveRepeats     Do not remove duplicated phrase in a field. If a field
                        consists entirely of a duplicated phrase, one copy is
                        removed.
  --titleCase           Words consisting of all capital letters are examined
                        and converted to title case if appropriate.
  --noTitleCase         Do not words consisting of all capital letters are
                        examined and converted to title case if appropriate.
  --header              Prefix the list with its byte count. The first line of
                        the output file will contain a count of the remaining
                        bytes in the file.
  --noHeader            Do not prefix the list with its byte count. The first
                        line of the output file will contain a count of the
                        remaining bytes in the file.
  --removeNames         Remove personal names for privacy.
  --noRemoveNames       Do not remove personal names for privacy.
  --config configfilename
                        A file containing configuration flags and options
  --verbatim filename [filename ...], --verbatims filename [filename ...]
                        A filename whose fields are merged without
                        modification. These files are merged after field
                        fixups have been applied.
  -v, --verbose         Enable verbose output.
  --debug               Enable debugging output.
  --version             Output the current version.
  --excludeID filename [id[-id] ...], --excludeIDs filename [id[-id] ...]
  --includeID filename [id[-id] ...], --includeIDs filename [id[-id] ...]
  --excludeCountry filename [countryname ...], --excludeCountries filename [countryname ...]
  --includeCountry filename [countryname ...], --includeCountries filename [countryname ...]
```

Examples:

	merge_users.py -abbrevCountries --abbrevStates myusers.csv marcdb.csv

	merge_users.py myusers.csv marcdb.csv --verbatim override.csv
