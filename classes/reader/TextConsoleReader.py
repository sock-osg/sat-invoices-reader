#!/usr/bin/env python3

from typing import List
from xml.dom import NotSupportedErr
import zipfile
from classes.dto.Comprobante import Comprobante
from classes.parser.CustomElement import CustomElement
from classes.parser.InvoiceParserInterface import InvoiceParserInterface
from lxml import etree
import io

from classes.reader.InvoiceFileReader import InvoiceFileReader


class TextConsoleReader:

    @property
    def deductionParser(self) -> InvoiceParserInterface:
        return self._deduct_parser

    def setDeductuctionParser(self, _deduct_parser: InvoiceParserInterface):
        self._deduct_parser = _deduct_parser

    @property
    def payrollParser(self) -> InvoiceParserInterface:
        return self._payroll_parser

    def setPayrollParser(self, _payroll_parser: InvoiceParserInterface):
        self._payroll_parser = _payroll_parser

    @property
    def file_reader(self) -> InvoiceFileReader:
        return self._file_reader

    def setFileReader(self, _reader: InvoiceFileReader):
        self._file_reader = _reader

    @property
    def callback_result(self) -> dict:
        return self._calback_res

    def read(self, path: str, _type: str):

        if _type == 'D':
            self.read_deductions(path)
        elif _type == 'P':
            self.read_payroll(path)
        else:
            raise NotSupportedErr('Invoce type not supported %(name)s' % _type)

    def read_payroll(self, path: str):

        # print headers
        print(
            'archivo',
            'xml version',
            'cfdiUuid',
            'fecha',
            'descripcion',
            'fechainicialpago',
            'fechafinalpago',
            'nombre emisor',
            'rfc emisor',
            'totalGravado',
            'impuestoRetenido',
            'saldoNeto',
            sep='|')

        callback = None
        self._calback_res = []
        custom_parser = self.__get_tree_parser()

        if self.file_reader.is_zipped_file:
            # read file into zip
            callback = lambda filename, zip_file: self.__read_payroll_zip_file(
                filename,
                custom_parser,
                zip_file)
        else:
            # read file
            callback = lambda filename: self.__read_payroll_file(filename, custom_parser)

        self._file_reader.do_in_list(path, callback)

    def read_deductions(self, path: str):

        print(
            'archivo',
            'xml version',
            'cfdiUuid',
            'fecha',
            'descripcion',
            'fechainicialpago',
            'fechafinalpago',
            'nombre emisor',
            'rfc emisor',
            'totalGravado',
            'impuestoRetenido',
            'saldoNeto',
            sep='|')

        callback = None
        self._calback_res = []
        custom_parser = self.__get_tree_parser()

        if self.file_reader.is_zipped_file:
            # read file into zip
            callback = lambda filename, zip_file: self.__read_deduction_zip_file(
                filename,
                custom_parser,
                zip_file)
        else:
            # read file
            callback = lambda filename: self.__read_deduction_file(filename, custom_parser)

        self._file_reader.do_in_list(path, callback)

    def __read_payroll_zip_file(
            self, filename: str, custom_parser: etree.XMLParser, zip_file: zipfile.ZipFile) -> List:
        content = io.BytesIO(zip_file.read(filename))
        contentDecoded = content.getvalue().decode('utf-8', 'ignore')
        file = etree.fromstring(contentDecoded, custom_parser)
        invoice = self.payrollParser.parse(filename, file)

        if invoice is not None:
            self.__print_payroll_record(invoice)
            self.callback_result.append(filename)

    def __read_payroll_file(self, filename: str,
                            custom_parser: etree.XMLParser) -> List:
#        file.attrib['{{{pre}}}schemaLocation'.format(pre='http://www.host.org/2001/XMLSchema-instance')]
        file = etree.parse(filename, custom_parser)
        invoice = self.payrollParser.parse(filename.name, file)

        if invoice is not None:
            self.__print_payroll_record(invoice)
            self.callback_result.append(filename.name)

    def __print_payroll_record(self, invoice: Comprobante):
        print(
            invoice.file_name,
            invoice.version,
            invoice.tfd.uuid,
            invoice.doc_date,
            invoice.concepts[0].description,
            invoice.payroll.start_payment_date,
            invoice.payroll.end_payment_date,
            invoice.issuer.name,
            invoice.issuer.rfc,
            invoice.subtotal,
            invoice.payroll.paid_tax,
            invoice.total,
            sep='|')

    def __read_deduction_file(self, filename: str,
                              custom_parser: etree.XMLParser) -> List:
        file = etree.parse(filename, custom_parser)
        self.__print_deduction_record(
            self.deductionParser.parse(
                filename, file))
        self.callback_result.append(filename)

    def __read_deduction_zip_file(
            self, filename: str, custom_parser: etree.XMLParser, zip_file: zipfile.ZipFile) -> List:
        content = io.BytesIO(zip_file.read(filename))
        contentDecoded = content.getvalue().decode('utf-8', 'ignore')
        file = etree.fromstring(contentDecoded, custom_parser)
        self.__print_deduction_record(self.payrollParser.parse(filename, file))
        self.callback_result.append(filename)

    def __print_deduction_record(self, invoice: Comprobante):
        print(
            invoice.file_name,
            invoice.version,
            invoice.tfd.uuid,
            invoice.doc_date,
            invoice.concepts[0].description,
            invoice.issuer.name,
            invoice.issuer.rfc,
            invoice.subtotal,
            invoice.total,
            sep='|')

    def __get_tree_parser(self) -> etree.XMLParser:
        parser_lookup = etree.ElementDefaultClassLookup(element=CustomElement)
        parser = etree.XMLParser(recover= True)
        parser.set_element_class_lookup(parser_lookup)

        return parser
