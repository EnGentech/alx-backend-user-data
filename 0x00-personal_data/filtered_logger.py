#!/usr/bin/env python3
"""
function called filter_datum will return the log message obfuscated
"""

from typing import List
import re


def filter_datum(fields: List[str], redaction: str, message: str,
                 separator: str) -> str:
    """ Basic login function """
    for specifics in fields:
        message = re.sub(rf"{specifics}=(.*?)\{separator}",
                         f'{specifics}={redaction}{separator}', message)
    return message

# Coded by EnGentech
