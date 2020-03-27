#!/usr/bin/python
# perform daily incremental backup
import Tape, sys

age = 1.25 # days
if len(sys.argv) > 1:
    age = float(sys.argv[1])

t = Tape.Tape(debug=True, age=age)
t.backup_to_file()
