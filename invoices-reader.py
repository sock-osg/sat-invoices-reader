#!/usr/bin/python3
import sys, getopt
import os
import os.path
import io
import zipfile
from pathlib import Path
import xml.etree.ElementTree as ET
from decimal import Decimal
from invoicexmlreader import readXml, printHeaders

def read(filename):
  xmlcontent = open(filename).read()

  contentDecoded = xmlcontent
  contentDecodedLower = contentDecoded.lower()

  root = ET.fromstring(contentDecodedLower)

  readXml(filename, root)

def readInvoices(sourcesPath):
  printHeaders()
  for filename in Path(sourcesPath).glob('**/*.xml'):
    try:
      read(filename)
    except:
      print(sys.exc_info())
      print('Error with file ' + filename.name + ', skipping...')

def main(argv):
  sourcesPath = ''
  try:
    opts, args = getopt.getopt(argv, "hp:", ["sourcesPath="])
  except getopt.GetoptError:
    print('invoices-reader.py -p <sourcesPath>')
    sys.exit(2)
  for opt, arg in opts:
    if opt == '-h':
      print('./invoices-reader.py -p <sourcesPath>\n')
      print('\t-p\tCould be a root folder with subfolders which contain xml files.')
      sys.exit()
    elif opt in ("-p", "--sourcesPath"):
      sourcesPath = arg

  readInvoices(sourcesPath)

if __name__ == "__main__":
  main(sys.argv[1:])
