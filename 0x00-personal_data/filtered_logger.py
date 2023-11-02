#!/usr/bin/env python3
"""
function called filter_datum will return the log message obfuscated
"""

from typing import List
import re
import logging


def filter_datum(fields: List[str], redaction: str, message: str,
                 separator: str) -> str:
    """ Basic login function """
    for specifics in fields:
        message = re.sub(rf"{specifics}=(.*?)\{separator}",
                         f'{specifics}={redaction}{separator}', message)
    return message


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields):
        """Initialization"""
        self.fields = fields
        super(RedactingFormatter, self).__init__(self.FORMAT)

    def format(self, record: logging.LogRecord) -> str:
        """format function definition"""
        return filter_datum(self.fields, self.REDACTION, super().format(record), self.SEPARATOR)

# Coded by EnGentech
