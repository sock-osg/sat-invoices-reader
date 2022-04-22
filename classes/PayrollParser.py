#!/usr/bin/env python3

from classes.InvoceParserInterface import InvoceParserInterface

class PayrollParser(InvoceParserInterface):

  cfdiPrintedRegistry = []

  def print_headers(self):
    print('archivo', 'xml version', 'cfdiUuid', 'fecha', 'descripcion', 'fechainicialpago', 'fechafinalpago', 'nombre emisor',
          'rfc emisor', 'totalGravado', 'impuestoRetenido', 'saldoNeto', sep='|')

  def read_file(self, fileName, file):
    complement = file.findall('{http://www.sat.gob.mx/cfd/3}complemento/{http://www.sat.gob.mx/timbrefiscaldigital}timbrefiscaldigital')[0]
    cfdiUuid = complement.get('uuid')

    if cfdiUuid not in self.cfdiPrintedRegistry:
      self.cfdiPrintedRegistry.append(cfdiUuid)

      emisor = file.find('{http://www.sat.gob.mx/cfd/3}emisor')

      concept = file.find('{http://www.sat.gob.mx/cfd/3}conceptos').find('{http://www.sat.gob.mx/cfd/3}concepto')

      _nomina = file.findall('{http://www.sat.gob.mx/cfd/3}complemento/{http://www.sat.gob.mx/nomina}nomina')
      _nomina12 = file.findall('{http://www.sat.gob.mx/cfd/3}complemento/{http://www.sat.gob.mx/nomina12}nomina')

      nomina = (_nomina or _nomina12)[0]

      _deducciones = nomina.findall('{http://www.sat.gob.mx/nomina}deducciones/{http://www.sat.gob.mx/nomina}deduccion')
      _deducciones12 = nomina.findall('{http://www.sat.gob.mx/nomina12}deducciones/{http://www.sat.gob.mx/nomina12}deduccion')

      deducciones = _deducciones or _deducciones12

      paidTax = ''
      for deduccion in deducciones:
        if deduccion.get('tipodeduccion') == '002':
          paidTax = deduccion.get('importe') or deduccion.get('importegravado')

      print(fileName, file.get('version'), cfdiUuid.upper(), file.get('fecha').upper(), concept.get('descripcion'),
            nomina.get('fechainicialpago'), nomina.get('fechafinalpago'), emisor.get('nombre').upper(), emisor.get('rfc').upper(),
            file.get('subtotal'), paidTax, file.get('total'), sep='|')
