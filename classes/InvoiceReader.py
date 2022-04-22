#!/usr/bin/env python3

import sys
import xml.etree.ElementTree as ET

from pathlib import Path
from classes.PayrollParser import PayrollParser
from classes.DeductionsParser import DeductionsParser

class InvoiceReader(object):

  DEF_FILE_ENCODING='utf-8'
  fileEncoding = None

  def read(self,filename):
    if(self.fileEncoding == None):
      self.fileEncoding = self.DEF_FILE_ENCODING

    xmlcontent = open(filename,encoding=self.fileEncoding).read()

    contentDecoded = xmlcontent
    contentDecodedLower = contentDecoded.lower()

    return ET.fromstring(contentDecodedLower)

  def readInvoices(self,sourcesPath, _type):
    reader= None
    if _type == 'D':
      reader=DeductionsParser()
    else:
      reader= PayrollParser()

    if(reader!= None):
      self.readFiles(reader, sourcesPath)      

  def readFiles(self,_instance,sourcesPath):
    _instance.print_headers()

    for filename in sorted(Path(sourcesPath).glob('**/*.xml')):
      try:
        file=self.read(filename)
        _instance.read_file(filename,file)
      except:
        print(sys.exc_info())
        print('Error with file ' + filename.name + ', skipping...')
