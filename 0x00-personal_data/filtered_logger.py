#!/usr/bin/env python3
"""Personal data"""
from typing import List
import re
import logging
def filter_datum(fields: List[str], redaction: str, message: str, separator: str) -> str:
    """ A function that 
    Returns a obfuscated log message"""
    for i in fields:
        message = re.sub(i + "=" + ".*?"+ separator, 
                         i + "=" + redaction + separator, message)
    return message


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self):
        super(RedactingFormatter, self).__init__(self.FORMAT)

    def format(self, record: logging.LogRecord) -> str:
        