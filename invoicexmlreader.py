#!/usr/bin/python3

cfdiPrintedRegistry = []

def readPayrollXml(fileName, xmlRoot):
  complement = xmlRoot.findall('{http://www.sat.gob.mx/cfd/3}complemento/{http://www.sat.gob.mx/timbrefiscaldigital}timbrefiscaldigital')[0]
  cfdiUuid = complement.get('uuid')

  if cfdiUuid not in cfdiPrintedRegistry:
    cfdiPrintedRegistry.append(cfdiUuid)

    emisor = xmlRoot.find('{http://www.sat.gob.mx/cfd/3}emisor')
    #receipt = xmlRoot.find('{http://www.sat.gob.mx/cfd/3}receptor')

    concept = xmlRoot.find('{http://www.sat.gob.mx/cfd/3}conceptos').find('{http://www.sat.gob.mx/cfd/3}concepto')

    _nomina = xmlRoot.findall('{http://www.sat.gob.mx/cfd/3}complemento/{http://www.sat.gob.mx/nomina}nomina')
    _nomina12 = xmlRoot.findall('{http://www.sat.gob.mx/cfd/3}complemento/{http://www.sat.gob.mx/nomina12}nomina')

    nomina = (_nomina or _nomina12)[0]

    _deducciones = nomina.findall('{http://www.sat.gob.mx/nomina}deducciones/{http://www.sat.gob.mx/nomina}deduccion')
    _deducciones12 = nomina.findall('{http://www.sat.gob.mx/nomina12}deducciones/{http://www.sat.gob.mx/nomina12}deduccion')

    deducciones = _deducciones or _deducciones12

    paidTax = ''
    for deduccion in deducciones:
      if deduccion.get('tipodeduccion') == '002':
        paidTax = deduccion.get('importe') or deduccion.get('importegravado')

    print(fileName, xmlRoot.get('version'), cfdiUuid.upper(), xmlRoot.get('fecha').upper(), concept.get('descripcion'), nomina.get('fechainicialpago'), nomina.get('fechafinalpago'), emisor.get('nombre').upper(), emisor.get('rfc').upper(), xmlRoot.get('subtotal'), paidTax, xmlRoot.get('total'), sep='|')

def readDeductionsXml(fileName, xmlRoot):
  complement = xmlRoot.findall('{http://www.sat.gob.mx/cfd/3}complemento/{http://www.sat.gob.mx/timbrefiscaldigital}timbrefiscaldigital')[0]
  cfdiUuid = complement.get('uuid')

  if cfdiUuid not in cfdiPrintedRegistry:
    cfdiPrintedRegistry.append(cfdiUuid)

    emisor = xmlRoot.find('{http://www.sat.gob.mx/cfd/3}emisor')
    #receipt = xmlRoot.find('{http://www.sat.gob.mx/cfd/3}receptor')

    concept = xmlRoot.find('{http://www.sat.gob.mx/cfd/3}conceptos').find('{http://www.sat.gob.mx/cfd/3}concepto')

    print(fileName, xmlRoot.get('version'), cfdiUuid.upper(), xmlRoot.get('fecha').upper(), concept.get('descripcion'), emisor.get('nombre').upper(), emisor.get('rfc').upper(), xmlRoot.get('subtotal'), xmlRoot.get('total'), sep='|')

def printPayrollHeaders():
  print('archivo', 'xml version', 'cfdiUuid', 'fecha', 'descripcion', 'fechainicialpago', 'fechafinalpago', 'nombre emisor', 'rfc emisor', 'totalGravado', 'impuestoRetenido', 'saldoNeto', sep='|')

def printDeductionsHeaders():
  print('archivo', 'xml version', 'cfdiUuid', 'fecha', 'descripcion', 'nombre emisor', 'rfc emisor', 'totalGravado', 'saldoNeto', sep='|')
