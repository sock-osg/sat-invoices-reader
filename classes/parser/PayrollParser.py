#!/usr/bin/env python3

from classes.dto.Comprobante import Comprobante, Concept, Issuer, Payroll, TimbreFiscalDigital
from classes.parser.CustomElement import CustomElement
from classes.parser.InvoiceParserInterface import InvoiceParserInterface
from lxml.etree import _ElementTree as ET


class PayrollParser(InvoiceParserInterface):

    def parse(self, file_name, file: ET) -> Comprobante:

        cfdi = Comprobante()

        root: CustomElement = file.find('.')
        root.setNamespaces(cfdi._ns)

        _type = root.get('tipodecomprobante')

        if( _type is not None and _type != 'N'):
            return

        cfdi.setFilename(file_name)
        cfdi.setType(_type)
        cfdi.setVersion(root.get('version'))
        cfdi.setDate(root.get('fecha'))
        cfdi.setSubtotal(root.get('subtotal'))
        cfdi.setTotal(root.get('total'))

        _tfd = root.getElement('complemento/timbrefiscaldigital')
        if _tfd is not None:
            cfdi.setTfd(TimbreFiscalDigital(_tfd.get('uuid')))

        _issuer = root.getElement('emisor')

        if _issuer is not None:
            issuer = Issuer()
            issuer.setName(_issuer.get('nombre'))
            issuer.setRfc(_issuer.get('rfc'))
            cfdi.setIssuer(issuer)

        _concept = root.getElement('conceptos/concepto')

        if(_concept is not None):
            _concept = _concept[0] if isinstance(_concept, list) else _concept
            concept = Concept(_concept.get('descripcion'))
            cfdi.setConcepts([concept])

        _payroll = root.getElement('complemento/nomina')

        if _payroll is not None:
            payroll = Payroll()
            payroll.setStartPaymentDate(_payroll.get('fechainicialpago'))
            payroll.setEndPaymentDate(_payroll.get('fechafinalpago'))

            _deductions = root.getElement(
                'complemento/nomina/deducciones/deduccion')

            cfdi.setPayroll(payroll)

            if isinstance(_deductions, list):

                for _deduc in _deductions:
                    paidTax = self.get_paid_tax_deduction(_deduc)
                    cfdi.payroll.setPaidTax(paidTax)

            elif _deductions is not None:
                    paidTax = self.get_paid_tax_deduction(_deductions)
                    cfdi.payroll.setPaidTax(paidTax)

        return cfdi
    

    def get_paid_tax_deduction(self, _deduc):
        if _deduc.get('tipodeduccion') == '002':
            return _deduc.get('importe') or _deduc.get('importegravado')
                