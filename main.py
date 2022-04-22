#!/usr/bin/env python3

import sys
import argparse
from classes.InvoiceReader import InvoiceReader
from classes.InvoiceZipReader import InvoiceZipReader

_epilog='''
This are an examples to execute the command:\n
    # read xml files from directory
    \t./main.py -p <sourcesPath>

    # read zipped xml files from directory
    \t./main.py -p <sourcesPath> -x

    # read zipped xml files from directory using encoding 'iso-8859-1'
    \t./main.py -p <sourcesPath> -e iso-8859-1 -x
'''

def main(argv):

  parser = argparse.ArgumentParser(description='Process to read invoce files from a specified directory (xml or zipped files)',
                                  formatter_class=argparse.RawDescriptionHelpFormatter,
                                  epilog=_epilog)
  parser.add_argument('-p','--sourcesPath',required=True, type=str, metavar="path"
                      , help='Path to directory with files, the nestted directories are included in the processing.')
  parser.add_argument('-t','--type', type=str, nargs='?',metavar='P,D', default='P'
                      , help='Invoice type,  P for payroll (by default) or D for deductions.')
  parser.add_argument('-x','--extract', action='store_true', help='Extract xml from zipped files.')
  parser.add_argument('-e','--encoding', metavar='fileEncoding', type=str, default='utf-8'
                      , help=''' Set file encoding to read files, by default 'utf-8' ''')

  args = parser.parse_args()

  reader = None

  if(args.extract):
    reader = InvoiceZipReader()
  else:
    reader = InvoiceReader()

  reader.fileEncoding=args.encoding

  print(args)
  if(reader != None):
    reader.readInvoices(args.sourcesPath, args.type)

if __name__ == "__main__":
  main(sys.argv[1:])
