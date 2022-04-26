#!/usr/bin/env python3

from classes.reader.InvoiceFileReader import InvoiceFileReader
from pathlib import Path

import zipfile
import unittest

class InvoiceFileReaderTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.file_reader = InvoiceFileReader()

    def test_list_xml_files(self):
        
        path = str(Path(__file__).parent)+"/resources/payroll/one_file"
        records = []
        callback = lambda filename: self.__fault_file_callback(filename, records)
        #  False by default
        # self.file_reader.read_ziped_files(False) 
        self.file_reader.do_in_list(path, callback)
        self.assertEquals(len(records), 1)
        

    def test_list_zip_files(self):
        path = str(Path(__file__).parent)+"/resources/payroll/zip_file"
        
        records = []
        callback = lambda filename, zip_file: self.__fault_zip_callback(filename, zip_file, records)

        self.file_reader.read_zipped_files(True)
        self.file_reader.do_in_list(path, callback)
        self.assertEquals(len(records), 2)

    def __fault_file_callback(self, filename:str, result: list):
        """ Append to List readed file names"""
        result.append(filename)
        
    def __fault_zip_callback(self, filename:str, zip_file:zipfile.ZipFile,  result: list):
        """ Append to List readed file names in zip """
        result.append(filename)
        