from classes.InvoiceZipReader import InvoiceZipReader
import unittest

from classes.InvoiceReader import InvoiceReader
from classes.InvoiceZipReader import InvoiceZipReader
from pathlib import Path

class InvoceReaderTest(unittest.TestCase):

    sourcesPath=str(Path(__file__).parent)+"/resources/"

    def test_read_xml(self):
        
        reader = InvoiceReader()
        reader.readInvoices( self.sourcesPath,'P')
        #self.assertTrue(1)

    def test_read_zip(self):
        
        reader = InvoiceZipReader()
        reader.readInvoices( self.sourcesPath,'P')
        #self.assertTrue(1)