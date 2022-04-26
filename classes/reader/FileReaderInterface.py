#!/usr/bin/env python3

import abc
import typing


class FileReaderInterface(metaclass=abc.ABCMeta):

    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'do_in_list') and
                callable(subclass.do_in_list))

    @abc.abstractmethod
    def do_in_list(self, path: str, _callback: typing.Any):
        """List files and execute a custom operation during looping"""
        raise NotImplementedError
