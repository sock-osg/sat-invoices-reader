#!/usr/bin/env python3

import abc

from classes.dto.Comprobante import CFDI


class InvoiceParserInterface(metaclass=abc.ABCMeta):

    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'parse') and
                callable(subclass.parse))

    @abc.abstractmethod
    def parse(self, file_name: str, file) -> CFDI:
        """Read data from file"""
        raise NotImplementedError
