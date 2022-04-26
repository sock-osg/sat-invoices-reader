#!/usr/bin/env python3

from classes.dto.Comprobante import CFDI, Comprobante
from classes.parser.CustomElement import CustomElement
from classes.parser.PayrollParser import PayrollParser

from lxml import etree

import unittest

class PayrollParserTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        _FILE="./test/resources/payroll/one_file/dummy-invoice.xml"
        parser_lookup = etree.ElementDefaultClassLookup(element=CustomElement)
        parser = etree.XMLParser()
        parser.set_element_class_lookup(parser_lookup)
        cls.file: etree._ElementTree = etree.parse(_FILE, parser)

    def test_parse(self):
        
        parser = PayrollParser()
        com : Comprobante = parser.parse('dummy-filename-invoice.xml', self.file)

        self.assertIsNotNone(com.issuer)
        self.assertEquals(com.issuer.rfc, 'ABC123456T5')
        self.assertIsNotNone(com.payroll)
        self.assertIsNotNone(com.concepts[0])
        
