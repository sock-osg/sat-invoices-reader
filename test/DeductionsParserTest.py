#!/usr/bin/env python3

from classes.dto.Comprobante import Comprobante
from classes.parser.CustomElement import CustomElement
from classes.parser.DeductionsParser import DeductionsParser

from lxml import etree

import unittest

class DeductionsParserTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        _FILE = "./test/resources/payroll/one_file/dummy-invoice.xml"
        parser_lookup = etree.ElementDefaultClassLookup(element=CustomElement)
        parser = etree.XMLParser()
        parser.set_element_class_lookup(parser_lookup)
        cls.file: etree._ElementTree = etree.parse(_FILE, parser)

    def test_parse(self):
        
        parser = DeductionsParser()
        com : Comprobante = parser.parse('dummy-filename-invoice.xml', self.file)

        self.assertIsNotNone(com.issuer)
        self.assertEquals(com.issuer.rfc, 'ABC123456T5')
        self.assertIsNotNone(com.concepts[0])
        self.assertEquals(com.total, '1000.0')
        
