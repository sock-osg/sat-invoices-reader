#!/usr/bin/env python3

from classes.dto.Comprobante import Comprobante, Concept, Issuer, TimbreFiscalDigital
from classes.parser.CustomElement import CustomElement
from classes.parser.InvoiceParserInterface import InvoiceParserInterface
from lxml.etree import _ElementTree as ET


class DeductionsParser(InvoiceParserInterface):

    def parse(self, file_name, file: ET) -> Comprobante:

        cfdi = Comprobante()

        root: CustomElement = file.find('.')
        root.setNamespaces(cfdi._ns)

        cfdi.setFilename(file_name)
        cfdi.setVersion(root.get('version'))
        cfdi.setDate(root.get('fecha'))
        cfdi.setSubtotal(root.get('subtotal'))
        cfdi.setTotal(root.get('total'))

        _tfd = root.getElement('complemento/timbrefiscaldigital')
        if _tfd is not None:
            cfdi.setTfd(TimbreFiscalDigital(_tfd.get('uuid')))

        _issuer = root.getElement('emisor')
        issuer = Issuer()
        issuer.setName(_issuer.get('nombre'))
        issuer.setRfc(_issuer.get('rfc'))
        cfdi.setIssuer(issuer)

        _concept = root.getElement('conceptos/concepto')

        if(_concept is not None):
            _concept = _concept[0] if isinstance(_concept, list) else _concept
            concept = Concept(_concept.get('descripcion'))
            cfdi.setConcepts([concept])

        return cfdi
