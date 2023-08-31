#!/usr/bin/env python3
"""Personal data"""
from typing import List
import re
def filter_datum(fields: List[str], redaction: str, message: str, separator: str):
    """ A function that 
    Returns a obfuscated log message"""
    for i in fields:
        message = re.sub(i +'=' + '.*?'+ separator, 
                         i + '=' + redaction + separator, message)
    return message