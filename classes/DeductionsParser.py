#!/usr/bin/env python3

from classes.InvoceParserInterface import InvoceParserInterface

class DeductionsParser(InvoceParserInterface):

    def print_headers(self):
        print('archivo', 'xml version', 'cfdiUuid', 'fecha', 'descripcion', 'fechainicialpago', 'fechafinalpago', 'nombre emisor', 'rfc emisor', 'totalGravado', 'impuestoRetenido', 'saldoNeto', sep='|')

    def read_file(self,fileName, file):
        complement = file.findall('{http://www.sat.gob.mx/cfd/3}complemento/{http://www.sat.gob.mx/timbrefiscaldigital}timbrefiscaldigital')[0]
        cfdiUuid = complement.get('uuid')

        cfdiPrintedRegistry = []

        if cfdiUuid not in cfdiPrintedRegistry:
            cfdiPrintedRegistry.append(cfdiUuid)

            emisor = file.find('{http://www.sat.gob.mx/cfd/3}emisor')
            #receipt = file.find('{http://www.sat.gob.mx/cfd/3}receptor')

            concept = file.find('{http://www.sat.gob.mx/cfd/3}conceptos').find('{http://www.sat.gob.mx/cfd/3}concepto')

            print(fileName, file.get('version'), cfdiUuid.upper(), file.get('fecha').upper(), concept.get('descripcion'), emisor.get('nombre').upper(), emisor.get('rfc').upper(), file.get('subtotal'), file.get('total'), sep='|')