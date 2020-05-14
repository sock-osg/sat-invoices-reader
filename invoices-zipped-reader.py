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

def extract(filename):
  z = zipfile.ZipFile(filename)
  zippedFiles = z.namelist()
  zippedXmlFiles = [file for file in zippedFiles if 'xml' in file]

  for zippedXmlFile in zippedXmlFiles:
    content = io.BytesIO(z.read(zippedXmlFile))

    contentDecoded = content.getvalue().decode('utf-8', 'ignore')
    contentDecodedLower = contentDecoded.lower()

    root = ET.fromstring(contentDecodedLower)
    readXml(filename, root)

def readInvoices(sourcesPath):
  printHeaders()
  for filename in Path(sourcesPath).glob('**/*.zip'):
    try:
      extract(filename)
    except:
      print(sys.exc_info())
      print('Error with file ' + filename.name + ', skipping...')

def main(argv):
  sourcesPath = ''
  try:
    opts, args = getopt.getopt(argv, "hp:", ["sourcesPath="])
  except getopt.GetoptError:
    print('invoices-zipped-reader.py -p <sourcesPath>')
    sys.exit(2)
  for opt, arg in opts:
    if opt == '-h':
      print('./invoices-zipped-reader.py -p <sourcesPath>\n')
      print('\t-p\tCould be a root folder with subfolders which contain xml zipped files.')
      sys.exit()
    elif opt in ("-p", "--sourcesPath"):
      sourcesPath = arg

  readInvoices(sourcesPath)

if __name__ == "__main__":
  main(sys.argv[1:])
