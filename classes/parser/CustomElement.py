#!/usr/bin/env python3

from lxml import etree
from re import Match

import typing
import re


class CustomElement(etree.ElementBase):

    __NS_MAP = {"re": "http://exslt.org/regular-expressions"}
    __XPATH_GET_ATTR = "(./@*[re:test(local-name(), '^{0}$','i')])[1]"
    __XPATH_SET_ATTR = "name(./@*[re:test(local-name(), '^{0}$','i')])"
    __XPATH_FIND_NESTED_EL = "/*[re:test(local-name(), '^{0}$','i')]"
    __NESTED_PATH_PATTERN = r"^(([*]?:?\w)+(/)+([*]?:?\w)+)+$"  # identify nested path

    @property
    def namespaces(self):
        return self._namespaces

    def setNamespaces(self, ns):
        self._namespaces = ns

    def get(self, key) -> typing.Any:
        """ Get a property from the node element """

        el = etree.XPath(self.__XPATH_GET_ATTR.format(key),
                         namespaces=self.__NS_MAP)(self)

        if(el and isinstance(el, list)):
            return el[0]
        else:
            return None

    def set(self, key, value) -> typing.Any:
        """ Set a property in the node element """

        match: str = super().xpath(self.__XPATH_SET_ATTR.format(key),
                                   namespaces=self.__NS_MAP)

        return super().set(match, value) if match else super().set(key, value)

    def find(self, path: str, namespaces=None) -> typing.Any:
        """ find only one node element from a file, match only the first result if that have many nodes"""

        ns = self.__getNamespaces(namespaces)
        return super().find(path, namespaces=ns)

    def findall(self, path: str, namespaces=None) -> typing.Any:
        """ find all element nodes from a file, an empty list is returned xml don't have nodes """

        ns = self.__getNamespaces(namespaces)
        return super().findall(path, namespaces=ns)

    def xpath(self, path, **_variables) -> typing.Any:
        """ execute a pecific xpath string on file"""

        ns = _variables.get('namespaces')
        if not ns:
            _variables['namespaces'] = self.__getNamespaces(ns)
        return super().xpath(path, **_variables)

    def getElement(self, path: str, namespaces=None) -> typing.Any:
        """ Retrive a node element from xml file, an empty list is returned xml don't have the node"""

        match = self.isNestedPath(path)
        ns = self.__getNamespaces(namespaces)

        if match and isinstance(match, Match):
            path = self.getXpath(path.split('/'))
            el = super().xpath('.'+path, namespaces=ns)
        else:
            path = self.getXpath([path])
            el = super().xpath('.'+path, namespaces=ns)

        return self.__empty_filter(el)

    def __getNamespaces(self, namespaces: list) -> dict:
        """ Validate if namespaces are setted or assing one, if none assigned default is used"""

        if not namespaces:
            # print(self._namespaces)
            return self._namespaces if hasattr(self, 'namespaces') else self.__NS_MAP
        else:
            return namespaces

    def getXpath(self, elements: list) -> str:
        """ Build the xpath string from a list of elements """

        path = ''
        for e in elements:
            path += self.__XPATH_FIND_NESTED_EL.format(e)

        return path

    @classmethod
    def isNestedPath(cls, path: str) -> re.Match:
        """ Identify if path is a nested route to read xml, examples:\n

                Parent/Child/Grandchild
                a:Parent/b:Child/c:Grandchild
                *:Parent/*:Child/*:Grandchild
            """
        return re.search(cls.__NESTED_PATH_PATTERN, path)

    def __empty_filter(self, el):
        if(isinstance(el, list)):
            return el[0] if (len(el) == 1) else el
        else:
            return None
