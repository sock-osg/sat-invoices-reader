#!/usr/bin/python3
import sys, getopt
import os
import os.path
import io
import zipfile
from pathlib import Path
import xml.etree.ElementTree as ET
from decimal import Decimal
from invoicexmlreader import readPayrollXml, readDeductionsXml, printPayrollHeaders, printDeductionsHeaders

def read(filename, _type):
  xmlcontent = open(filename).read()

  contentDecoded = xmlcontent
  contentDecodedLower = contentDecoded.lower()

  root = ET.fromstring(contentDecodedLower)

  if _type == 'D':
    readDeductionsXml(filename, root)
  else:
    readPayrollXml(filename, root)

def readInvoices(sourcesPath, _type):
  if _type == 'D':
    printDeductionsHeaders()
  else:
    printPayrollHeaders()

  for filename in Path(sourcesPath).glob('**/*.xml'):
    try:
      read(filename, _type)
    except:
      print(sys.exc_info())
      print('Error with file ' + filename.name + ', skipping...')

def main(argv):
  sourcesPath = ''
  _type = 'P' # P ( Payroll ), D ( Deductions )
  try:
    opts, args = getopt.getopt(argv, "hp:t:", ["sourcesPath=", "type="])
  except getopt.GetoptError:
    print('invoices-reader.py -p <sourcesPath>')
    sys.exit(2)
  for opt, arg in opts:
    if opt == '-h':
      print('./invoices-reader.py -p <sourcesPath>\n')
      print('\t-p\tCould be a root folder with subfolders which contain xml files.')
      print('\t-t\tInvoice type, could be P(default) for payroll or D for deductions.')
      sys.exit()
    if opt in ("-p", "--sourcesPath"):
      sourcesPath = arg
    if opt in ('-t', '--type'):
      _type = arg

  readInvoices(sourcesPath, _type)

if __name__ == "__main__":
  main(sys.argv[1:])
