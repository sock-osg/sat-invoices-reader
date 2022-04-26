#!/usr/bin/env python3

from typing import List


class Issuer:

    @property
    def name(self) -> str:
        return self._name

    def setName(self, _name: str):
        self._name = _name

    @property
    def rfc(self) -> str:
        return self._rfc

    def setRfc(self, _rfc: str):
        self._rfc = _rfc


class Concept:

    def __init__(self, _desc: str) -> None:
        self._desc = _desc

    @property
    def description(self) -> str:
        return self._desc

    def setDescription(self, _desc: str):
        self._desc = _desc


class TimbreFiscalDigital:

    def __init__(self, _uuid: str) -> None:
        self._uuid = _uuid

    @property
    def uuid(self) -> str:
        return self._uuid

    def setUuid(self, _uuid):
        self._uuid = _uuid


class Payroll:

    @property
    def start_payment_date(self) -> str:
        return self._start_payment_date

    def setStartPaymentDate(self, _start_payment_date: str):
        self._start_payment_date = _start_payment_date

    @property
    def end_payment_date(self) -> str:
        return self._end_payment_date

    def setEndPaymentDate(self, _end_payment_date: str):
        self._end_payment_date = _end_payment_date

    @property
    def paid_tax(self) -> str:
        return self._paid_tax

    def setPaidTax(self, _paid_tax: str):
        self._paid_tax = _paid_tax

    # total_percepts: str
    # total_deductions: str
    # total_other: str


class CFDI:
    _ns = {"re": "http://exslt.org/regular-expressions",
           'cfdi': 'http://www.sat.gob.mx/cfd/3',
           'tfd': 'http://www.sat.gob.mx/timbrefiscaldigital',
           'nom': 'http://www.sat.gob.mx/nomina',
           'nom12': 'http://www.sat.gob.mx/nomina12'
           }


class Comprobante (CFDI):

    @property
    def cfdi_type(self):
        return self._type

    def setType(self, _type):
        self._type = _type

    @property
    def file_name(self) -> str:
        return self._file_name

    def setFilename(self, _file_name):
        self._file_name = _file_name

    @property
    def version(self) -> str:
        return self._version

    def setVersion(self, _version):
        self._version = _version

    @property
    def tfd(self) -> TimbreFiscalDigital:
        return self._tfd

    def setTfd(self, _tfd):
        self._tfd = _tfd

    @property
    def doc_date(self) -> str:
        return self._date

    def setDate(self, _date: str):
        self._date = _date

    @property
    def issuer(self) -> Issuer:
        return self._issuer

    def setIssuer(self, _issuer: Issuer):
        self._issuer = _issuer

    @property
    def total(self) -> str:
        return self._total

    def setTotal(self, _total: str):
        self._total = _total

    @property
    def subtotal(self) -> str:
        return self._subtotal

    def setSubtotal(self, _subtotal: str):
        self._subtotal = _subtotal

    @property
    def payroll(self) -> Payroll:
        return self._payroll

    def setPayroll(self, _payroll: Payroll):
        self._payroll = _payroll

    @property
    def concepts(self) -> List[Concept]:
        return self._concepts

    def setConcepts(self, _concepts: List[Concept]):
        self._concepts = _concepts
