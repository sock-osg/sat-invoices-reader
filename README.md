
# sat-invoices-reader
Sat invoices reader, the ones used in Mexico

## Requirements

- python > 3.X

Additional packages:

```bash
python -m pip install lxml pyyaml coverage coveralls autopep8
```

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

These are an examples to execute the command:

    # read xml files from directory
        ./main.py -p <sourcesPath>

    # read zipped xml files from directory
        ./main.py -p <sourcesPath> -x

    # read zipped xml files from directory using encoding 'iso-8859-1'
        ./main.py -p <sourcesPath> -x -e iso-8859-1
```

## Testing and code coverage

### Running unit tests

    $ python -m unittest discover -s ./test -p "*Test.py"

### Code coverage

```sh
# Clean coverage data
python -m coverage erase

# Create coverage report executing unit tests
python -m coverage run --source=classes -m unittest discover -s ./test -p "*Test.py"

# Create coverage report for coveralls
python -m coverage lcov -o ./coverage/lcov.info

# Show coverage report in terminal (text output)
python -m coverage report

# Create coverage report in html format
python -m coverage html

# help
python -m coverage help

```

### Coveralls report

Publish report on coverralls.io:

    $ python -m coveralls

# Enforcement style guide

```sh
# Show issues and statistics on sepecific path
python -m flake8 path/to/sources --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics

# Show issues and statistics on sepecific file, showing source code
python -m flake8 path/to/file.py --count --show-source  --statistics

```
For more deteil of errors and violations, see here [violation codes](https://flake8.pycqa.org/en/latest/user/error-codes.html) and [error codes](https://pycodestyle.pycqa.org/en/latest/intro.html#error-codes)

## Format code to conform style guide

Some issues can be automatically fixed using the module autopep8 style guide:

```sh
# Show list fix codes
python -m autopep8 --list-fixes

# Fix blank a few white spaces
python -m autopep8 -i <filename>

# Select subset of fixes
python -m autopep8 --select=E225,E231,E301,E302,E303,E265 <filename>

# Fix issues in aggresive level 1
python -m autopep8 --in-place --aggressive <filename>

# Show help
python -m autopep8 -h

```

See also **autopep8** docs [here](https://pypi.org/project/autopep8/) to get more detailed instructions and error codes description.
    