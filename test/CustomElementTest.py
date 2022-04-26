#!/usr/bin/env python3

from classes.dto.Comprobante import CFDI
from classes.parser.CustomElement import CustomElement
from lxml import etree
from xml.etree import ElementTree as ET

import unittest


class CustomElementTest(unittest.TestCase):

    _ns = CFDI._ns

    _tagRoot = str(ET.QName(_ns.get('cfdi'), 'Comprobante'))
    _tagEmisor = str(ET.QName(_ns.get('cfdi'), 'Emisor'))
    _tagConcepto = str(ET.QName(_ns.get('cfdi'), 'Concepto'))

    @classmethod
    def setUpClass(cls):
        _FILE = "./test/resources/payroll/one_file/dummy-invoice.xml"
        parser_lookup = etree.ElementDefaultClassLookup(element=CustomElement)
        parser = etree.XMLParser()
        parser.set_element_class_lookup(parser_lookup)
        cls.file: etree._ElementTree = etree.parse(_FILE, parser)

    def test_tree_find(self):

        tree: etree._ElementTree = self.file

        # case sensitive
        # support absolute paths (start with '/' or '//')
        paths = {
            '{*}Emisor',
            "/{*}Emisor",
            '//{*}Emisor',
            "./{*}Emisor",
            'cfdi:Emisor',
            '/cfdi:Emisor',
            '//cfdi:Emisor',
            './cfdi:Emisor',
            './/cfdi:Emisor',
            self._tagEmisor
        }

        for p in paths:
            el = tree.find(p, self._ns)  # setting namespaces required
            self.assertEqual(el.tag, self._tagEmisor)
            self.assertEqual(3, len(el.attrib))

        # nested elements

        paths = {
            './cfdi:Conceptos/cfdi:Concepto',
            './{*}Conceptos/{*}Concepto'
        }

        self.assertFindTagWithNs(paths, tree, self._tagConcepto)

    def test_tree_findall(self):

        tree: etree._ElementTree = self.file

        paths = {
            './{*}Complemento/{*}Nomina/{*}Percepciones/{*}Percepcion',
            './cfdi:Complemento/nom12:Nomina/{*}Percepciones/{*}Percepcion'
        }

        for p in paths:
            el = tree.findall(p, self._ns)
            self.assertEquals(3, len(el))

        # empty
        self.assertEquals(
            0, len(
                tree.findall(
                    './cfdi:dummy/{*}:dummies', self._ns)))

    def test_element_find(self):

        root: CustomElement = self.file.getroot()
        root.setNamespaces(self._ns)  # setting namespaces at root level

        self.assertIsInstance(root, CustomElement)
        self.assertEqual(root.tag, self._tagRoot)
        self.assertEquals(len(root.attrib), 16)

        # case sensitive
        # not support absolute paths (start with '/' or '//')
        paths = {
            '{*}Emisor',
            "./{*}Emisor",
            'cfdi:Emisor',
            './cfdi:Emisor',
            './/cfdi:Emisor',
            self._tagEmisor
        }

        self.assertFindTagWithNs(paths, root, self._tagEmisor)
        self.assertFindTagWithoutNs(paths, root, self._tagEmisor)

        paths = {
            './cfdi:Conceptos/cfdi:Concepto',
            './{*}Conceptos/{*}Concepto'
        }

        self.assertFindTagWithNs(paths, root, self._tagConcepto)

        # exceptions
        self.assertIsNone(root.find('Emisor'))

        with self.assertRaises(SyntaxError):
            root.find('x:Emisor')

    def assertFindTagWithNs(self, paths: dict, root, tag):
        for p in paths:
            el = root.find(p, self._ns)  # namespaces setted at element level
            self.assertEqual(el.tag, tag)

    def assertFindTagWithoutNs(self, paths: dict, root, tag):
        for p in paths:
            el = root.find(p)  # namespaces setted at root level
            self.assertEqual(el.tag, tag)

    def test_element_findall(self):

        root: CustomElement = self.file.getroot()
        root.setNamespaces(self._ns)

        paths = {
            './{*}Complemento/{*}Nomina/{*}Percepciones/{*}Percepcion',
            './cfdi:Complemento/nom12:Nomina/{*}Percepciones/{*}Percepcion'
        }

        for p in paths:
            el = root.findall(p)  # namespaces setted at root level
            self.assertEquals(3, len(el))

        # empty
        self.assertEquals(0, len(root.findall('./cfdi:dummy/{*}:dummies')))

    def test_element_get_attr(self):

        el: etree.ElementBase = self.file.getroot()
        self.assertTrue(isinstance(el, CustomElement))
        self.assertIsNone(el.get('formapagox'))
        self.assertIsNotNone(el.get('fOrMaPago'))
        self.assertEquals(el.get('formapago'), '99')

    def test_element_set_attr(self):

        el: etree.ElementBase = self.file.getroot()
        self.assertTrue(isinstance(el, CustomElement))

        self.assertEquals(el.get('formaPago'), '99')

        el.set('FormaPago', '000')
        self.assertEquals(el.get('formapago'), '000')

        el.set('newProperty', 'AbC')
        self.assertEquals(el.get('newproperty'), 'AbC')

    def test_get_element(self):

        el: CustomElement = self.file.getroot()

        emisor = el.getElement('emisor')
        self.assertEqual(emisor.tag, self._tagEmisor)

        # /*[re:test(local-name(), '^complemento$','i')]/*[re:test(local-name(), '^nomina$','i')]
        emisor = el.getElement('cfdi:emisor')
        self.assertEquals(0, len(emisor))

        emisor = el.getElement('emisorX/dummy')
        self.assertEquals(0, len(emisor))

        conceptos = el.getElement('conceptos/concepto')
        self.assertEquals(2, len(conceptos))

        percepciones = el.getElement(
            'comPlemento/nOMiNa/Percepciones/percepcion')
        self.assertEquals(3, len(percepciones))

        nom = el.getElement('complemento/nomina')
        # print(nom)

    
    @unittest.skip
    def test_regex_nested_paths(self):

        valid_paths = {
            'Emisor/abc',
            'Emisor/abc/d',
            'Emisor/*:abc/d',
            'Emisor/*:abc/x:d',
            'cfdi:Emisor/acd:aaaa/asdad',
            'cfdi:Emisor/acd:aaaa/aaa:asdad',
            '*:Emisor/*:aaaa/*:asdad',
            '*:Emisor/cfdi:aaaa/nom:asdad',
        }

        for p in valid_paths:
            self.assertIsNotNone(CustomElement.isNestedPath(p))

        invalid_paths = {
            "./{*}Emisor",
            './/{*}Emisor',
            './/{http://www.sat.gob.mx/cfd/3}Emisor',
            'cfdi:Emisor',
            '/cfdi:Emisor',
            '//cfdi:Emisor',
            '.cfdi:Emisor',
            './cfdi:Emisor',
            './/cfdi:Emisor',
            'cfdi:Emisor/',
            '.cfdi:Emisor',
            ':cfdi:Emisor',
            ':cfdi:Emisor/',
            'cfdi:Emisor/.',
            '/cfdi:Emisor',
            './cfdi:Emisor',
            './cfdi:Emisor',
            '/cfdi:Emisor/',
            '/cfdi:Emisor/',
            '/cfdi:*[local-name()="Emisor"]',
            './cfdi:*[local-name()="Emisor"]',
            ':/cfdi:*[local-name()="Emisor"]',
            '/*[local-name()="Emisor"]',
            './*[local-name()="Emisor"]',
            ':/*[local-name()="Emisor"]',
            '//cfdi:*[local-name()="Emisor"]',
            './/cfdi:*[local-name()="Emisor"]',
            '://cfdi:*[local-name()="Emisor"]',
            '//*[local-name()="Emisor"]',
            './/*[local-name()="Emisor"]',
            '://*[local-name()="Emisor"]',
            ':/*[local-name()="Emisor"]/cfdi:*[local-name()="Emisor"]',

        }

        for p in invalid_paths:
            self.assertIsNone(CustomElement.isNestedPath(p))

    def test_element_xpath(self):

        el: CustomElement = self.file.getroot()
        el.setNamespaces(self._ns)  # namespaces setted at root level

        paths = {
            '//cfdi:*[local-name()="Emisor"]',
            './cfdi:*[local-name()="Emisor"]',
            "//cfdi:*[re:test(local-name(), '^emIsor$','i')]",
            "./cfdi:*[re:test(local-name(), '^emisor$','i')]",
            "./*[re:test(local-name(), '^emisor$','i')]",
            "//*[re:test(local-name(), '(?i)emisor')]",
            "./*[re:test(local-name(), '^{0}$','i')]".format('emisor'),
            "./*[re:test(local-name(), '(?i)emisor')]"
        }

        for p in paths:
            # print(p)
            emisor = el.xpath(p)
            self.assertEqual(emisor[0].tag, self._tagEmisor)

        emisor = el.xpath(
            "//*[local-name() = $name]",
            name='Emisor',
            namespaces=self._ns)
        self.assertEqual(emisor[0].tag, self._tagEmisor)

        rfcTest = 'ABC123456T5'

        rfc = el.xpath("//cfdi:Emisor/@Rfc", namespaces=self._ns)
        self.assertEqual(rfc[0], rfcTest)

        rfc = el.xpath(
            "//cfdi:Emisor/@*[re:test(local-name(), '^{0}$','i')]".format(
                'rfc'),
            namespaces=self._ns)
        self.assertEqual(rfc[0], rfcTest)

        conceptos = el.xpath(
            "./*[re:test(local-name(), '^conceptos$' ,'i')]/*[re:test(local-name(), '^concepto$' ,'i')]",
            namespaces=self._ns)
        self.assertEquals(2, len(conceptos))

    def test_tree_xpath(self):

        el = self.file

        paths = {
            '//cfdi:*[local-name()="Emisor"]',
            './cfdi:*[local-name()="Emisor"]',
            "//cfdi:*[re:test(local-name(), '^emIsor$','i')]",
            "./cfdi:*[re:test(local-name(), '^emisor$','i')]",
            "./*[re:test(local-name(), '^emisor$','i')]",
            "//*[re:test(local-name(), '(?i)emisor')]",
            "./*[re:test(local-name(), '^{0}$','i')]".format('emisor'),
            "./*[re:test(local-name(), '(?i)emisor')]"
        }

        for p in paths:
            emisor = el.xpath(p, namespaces=self._ns)
            self.assertEqual(emisor[0].tag, self._tagEmisor)

        emisor = el.xpath("//*[local-name() = $name]", name='Emisor')
        self.assertEqual(emisor[0].tag, self._tagEmisor)

        rfcTest = 'ABC123456T5'

        rfc = el.xpath("//cfdi:Emisor/@Rfc", namespaces=self._ns)
        self.assertEqual(rfc[0], rfcTest)

        rfc = el.xpath(
            "//cfdi:Emisor/@*[re:test(local-name(), '^{0}$','i')]".format(
                'rfc'),
            namespaces=self._ns)
        self.assertEqual(rfc[0], rfcTest)

        conceptos = el.xpath(
            "./*[re:test(local-name(), '^conceptos$' ,'i')]/*[re:test(local-name(), '^concepto$' ,'i')]",
            namespaces=self._ns)
        self.assertEquals(2, len(conceptos))

    def test_invalid_file(self):

        _FILE = "./test/resources/others/invalid-invoice.xml"
        parser_lookup = etree.ElementDefaultClassLookup(element=CustomElement)
        parser = etree.XMLParser(dtd_validation= False, recover= True)
        parser.set_element_class_lookup(parser_lookup)
        file: etree._ElementTree = etree.parse(_FILE, parser)
        self.assertIsNotNone(file)
