#!/usr/bin/env python3

from pathlib import Path
import traceback
from classes.reader.FileReaderInterface import FileReaderInterface

import sys
import typing
import zipfile


class InvoiceFileReader(FileReaderInterface):

    def __init__(self, _is_zipped_file: bool = False) -> None:
        self._is_zipped_file = _is_zipped_file

    @property
    def is_zipped_file(self) -> bool:
        return self._is_zipped_file

    def read_zipped_files(self, read_zip: bool):
        self._is_zipped_file = read_zip

    def do_in_list(self, path: str, _callback: typing.Any):

        if self._is_zipped_file:
            self.__read_zip_files(path, _callback)
        else:
            self.__read_xml_files(path, _callback)

    def __read_xml_files(self, source_path: str, _callback: typing.Any):

        for filename in Path(source_path).glob('**/*.xml'):
            try:
                _callback(filename)
            except Exception:
                print(sys.exc_info())
                print(traceback.format_exc())
                print('Error with file {0} , skipping...'.format(filename))

    def __read_zip_files(self, source_path: str, _callback: typing.Any):

        for filename in Path(source_path).glob('**/*.zip'):
            try:
                self.__read_zip_content(filename, _callback)
            except BaseException:
                print(sys.exc_info())
                print(traceback.format_exc())
                print('Error with file {0} , skipping...'.format(filename.name))

    def __read_zip_content(self, filename, _callback):

        zip_file = zipfile.ZipFile(filename)
        zippedFiles = zip_file.namelist()
        file_names = [file for file in zippedFiles if 'xml' in file]

        for filename in file_names:
            _callback(filename, zip_file)
