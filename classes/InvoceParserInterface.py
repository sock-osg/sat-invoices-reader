#!/usr/bin/env python3

import abc

class InvoceParserInterface(metaclass=abc.ABCMeta):

    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'print_headers') and 
                callable(subclass.print_headers) and 
                hasattr(subclass, 'read_file') and 
                callable(subclass.read_file))
    
    @abc.abstractmethod
    def print_headers(self):
        """Load header labels"""
        raise NotImplementedError

    @abc.abstractmethod
    def read_file(self,filename:str, file):
        """Extract text from file"""
        raise NotImplementedError