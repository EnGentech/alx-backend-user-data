#!/usr/bin/env python3
"""
function called filter_datum will return the log message obfuscated
"""

from typing import List
import re


def filter_datum(fields: List[str], redaction:
                 str, message: str, seperator: str) -> str:
    """Basic loggin function"""
    for specifics in fields:
        message = re.sub(rf'{specifics}=.+?{seperator}',
                         f"{specifics}={redaction}{seperator}", message)
    return message

# Coded by EnGentech
