#!/usr/bin/env python3

from classes.parser.DeductionsParser import DeductionsParser
from classes.parser.PayrollParser import PayrollParser
from classes.reader.InvoiceFileReader import InvoiceFileReader
from classes.reader.TextConsoleReader import TextConsoleReader
from pathlib import Path

import unittest


class TextConsoleReaderTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.path = str(Path(__file__).parent)+"/resources/payroll"
        cls.reader = TextConsoleReader()
        cls.reader.setDeductuctionParser(DeductionsParser())
        cls.reader.setPayrollParser(PayrollParser())
        cls.reader.setFileReader(InvoiceFileReader())

    def test_read_payroll_invoce(self):

        self.reader.read(self.path, 'P')
        self.assertIsNotNone(self.reader.callback_result)

    def test_read_payroll_zip_invoce(self):
        
        self.reader.file_reader.read_zipped_files(True)
        self.reader.read(self.path, 'P')
        self.assertIsNotNone(self.reader.callback_result)

    def test_read_deductions_invoce(self):
        
        self.reader.read(self.path, 'D')
        self.assertIsNotNone(self.reader.callback_result)
    
    def test_read_deductions_zip_invoce(self):
        
        self.reader.file_reader.read_zipped_files(True)
        self.reader.read(self.path, 'D')
        self.assertIsNotNone(self.reader.callback_result)