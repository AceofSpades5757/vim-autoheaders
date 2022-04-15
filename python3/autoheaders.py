#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re
from pathlib import Path
from typing import Iterable
from typing import Optional
from typing import Union


# Authorship Information
__author__ = "Kyle L. Davis"
__copyright__ = "Copyright 2022, Kyle L. Davis"
__credits__ = ["Kyle L. Davis"]
__license__ = "MIT"
__version__ = "0.1.1"
__date__ = "2022 Apr 14"
__maintainer__ = "Kyle L. Davis"
__email__ = "AceofSpades5757.github@gmail.com"
__status__ = "Production"


class Header:
    """Represents a file header."""

    possible_author_values: list[str] = [
        'Author',
        'Maintainer',
    ]
    possible_version_values: list[str] = [
        'Version',
    ]

    start_line = r'^\s*"\s*'
    end_line = r'$'
    seperator = r'\s*:\s*'

    def __init__(self, path_or_lines: str):

        # Init
        try:
            if Path(path_or_lines).exists():
                self.content = open(path_or_lines).read()
            else:
                self.content = path_or_lines
        except OSError:  # Path too long
            self.content = path_or_lines
        self.lines = self.content.splitlines()
        self.range = (0, self.get_header_lines())

        # Clean
        self.lines = self.content.splitlines()[
            self.range[0] : self.range[1] - 1
        ]
        self.content = '\n'.join(self.lines)

        # Finish
        self.values = self.get_values()

    @property
    def author(self) -> Optional[str]:
        """Returns author, if available.

        Maintainer is an alias in this code."""
        possible_keys = self.possible_author_values
        return self[possible_keys]

    @property
    def version(self) -> Optional[str]:
        """Returns author, if available.

        Maintainer is an alias in this code."""
        possible_keys = self.possible_version_values
        return self[possible_keys]

    def value_regex(self, possible_keys: Union[Iterable, str]):

        start = self.start_line
        end = self.end_line
        seperator = self.seperator

        key: str
        if isinstance(possible_keys, (list, tuple)):
            key = '|'.join([key for key in possible_keys])
        elif isinstance(possible_keys, str):
            key = possible_keys
        else:
            raise TypeError("possible_keys of incorrect type.")

        value = r'.+'

        re_header = re.compile(
            start + fr'(?P<key>{key}){seperator}(?P<value>{value})' + end
        )

        return re_header

    def __setitem__(self, key, value) -> None:

        lines = self.lines
        re_target = self.value_regex(key)

        new_lines = []
        for line in lines:

            match = re_target.match(line)

            if match is not None:
                previous_value = match.group('value')
                new_line = line.replace(previous_value, value)
                new_lines.append(new_line)
                continue

            new_lines.append(line)

        self.lines = new_lines
        self.content = '\n'.join(new_lines)

    def increment_version(self):

        version = self.version

        versions = version.split('.')
        versions[2] = str(int(versions[2]) + 1)
        version = '.'.join(versions)

        return version

    def __getitem__(
        self, possible_keys: Union[Iterable, str]
    ) -> Optional[str]:
        """Returns value, if available.

        Maintainer is an alias in this code."""
        if isinstance(possible_keys, (list, tuple)):
            possible_values = [
                self.values[key]
                for key in possible_keys
                if self.values.get(key, None) is not None
            ]
            return possible_values[0] if possible_values else None
        elif isinstance(possible_keys, str):
            return self.values.get(possible_keys, None)
        else:
            raise TypeError("possible_keys of incorrect type.")

    def get_header_lines(self) -> int:
        """Get number of commented lines, or only whitespace, from
        beginning.
        """
        lines = self.lines

        re_commented = r'^\s*"\s*'
        re_empty = r'^\s*$'
        re_header_line = re.compile(fr'({re_commented}|{re_empty})')

        number_of_lines = 1
        line = lines[number_of_lines - 1]
        while re_header_line.match(line):
            try:  # Hotfix for header without any content
                number_of_lines += 1
                line = lines[number_of_lines - 1]
            except Exception:
                break

        return number_of_lines

    def get_values(self) -> dict:

        lines = self.lines

        start = r'^\s*"\s*'
        key = r'[^:]+'
        value = r'[^:]+'
        seperator = r'\s*:\s*'
        end = r'$'
        re_header = re.compile(
            start + fr'(?P<key>{key}){seperator}(?P<value>{value})' + end
        )

        matches = [
            re_header.match(line).groupdict()  # type: ignore
            for line in lines
            if re_header.match(line)
        ]
        values = {}
        for pair in matches:
            values[pair['key']] = pair['value']

        return values


def get_header_values(string: str) -> list:

    lines = string.splitlines()

    start = r'^\s*"\s*'
    key = r'[^:]+'
    value = r'[^:]+'
    seperator = r'\s*:\s*'
    end = r'$'
    re_header = re.compile(
        start + fr'(?P<key>{key}){seperator}(?P<value>{value})' + end
    )

    matches = [
        re_header.match(line).groupdict()  # type: ignore
        for line in lines
        if re_header.match(line)
    ]

    return matches


def get_header_lines(string: str) -> int:
    """Get number of lines that have comment, or whitespace, from beginning."""
    lines = string.splitlines()

    re_commented = r'^\s*"\s*'
    re_empty = r'^\s*$'
    re_header_line = re.compile(fr'({re_commented}|{re_empty})')

    number_of_lines = 1
    line = lines[number_of_lines - 1]
    while re_header_line.match(line):
        number_of_lines += 1
        line = lines[number_of_lines - 1]

    return number_of_lines
