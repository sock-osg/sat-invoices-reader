#!/usr/bin/env python3

import sys
import io
import zipfile
import xml.etree.ElementTree as ET

from pathlib import Path
from classes.PayrollParser import PayrollParser
from classes.DeductionsParser import DeductionsParser

class InvoiceZipReader(object):

  DEF_FILE_ENCODING = 'utf-8'
  fileEncoding = None

  def extract(self, filename, _instance):

    if(self.fileEncoding == None):
      self.fileEncoding = self.DEF_FILE_ENCODING

    z = zipfile.ZipFile(filename)
    zippedFiles = z.namelist()
    zippedXmlFiles = [file for file in zippedFiles if 'xml' in file]

    for zippedXmlFile in zippedXmlFiles:
      content = io.BytesIO(z.read(zippedXmlFile))

      contentDecoded = content.getvalue().decode(self.fileEncoding, 'ignore')
      contentDecodedLower = contentDecoded.lower()

      file = ET.fromstring(contentDecodedLower)
      _instance.read_file(filename, file)

  def readInvoices(self, sourcesPath, _type):
    print('reading zipped files')
    
    reader = None
    if _type == 'D':
      reader = DeductionsParser()
    else:
      reader = PayrollParser()
        
    if (reader != None):
      self.readFiles(reader, sourcesPath)

  def readFiles(self, _instance, sourcesPath):

    _instance.print_headers()

    for filename in sorted(Path(sourcesPath).glob('**/*.zip')):
      try:
        self.extract(filename, _instance)
      except:
        print(sys.exc_info())
        print('Error with file ' + filename.name + ', skipping...')
