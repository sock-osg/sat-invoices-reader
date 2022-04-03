# sat-invoices-reader
Sat invoices reader, the ones used in Mexico

## Requriments

- python > 3.X

## Description

Use option -h for help.

    $ main.py -h


output:
```
usage: main.py [-h] -p path [-t [P,D]] [-x] [-e fileEncoding]

Process to read invoce files from a specified directory (xml or zipped files)

options:
  -h, --help            show this help message and exit
  -p path, --sourcesPath path
                        Path to directory with files, the nestted directories are included in the processing.
  -t [P,D], --type [P,D]
                        Invoice type, P for payroll (by default) or D for deductions.
  -x, --extract         Extract xml from zipped files.
  -e fileEncoding, --encoding fileEncoding
                        Set file encoding to read files, by default 'utf-8'

This are an examples to execute the command:

    # read xml files from directory
        ./main.py -p <sourcesPath>

    # read zipped xml files from directory
        ./main.py -p <sourcesPath> -x

    # read zipped xml files from directory using encoding 'iso-8859-1'
        ./main.py -p <sourcesPath> -x -e iso-8859-1
```