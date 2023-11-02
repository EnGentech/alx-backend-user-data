#!/usr/bin/env python3
"""
function called filter_datum will return the log message obfuscated
"""

import logging
import re

def filter_datum(fields: list, redaction: str, message: str, seperator: str) -> str:
    """
    Basic loggin function
    """
    for specifics in fields:
        pattern = rf'{specifics}=.+?{seperator}'
        message = re.sub(pattern, f"{specifics}={redaction}{seperator}", message)
    return message

# Coded by EnGentech
