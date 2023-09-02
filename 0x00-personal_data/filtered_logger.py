#!/usr/bin/env python3
"""Personal data"""
from typing import List
import re
import logging
import os
import mysql.connector

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

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields
    def format(self, record: logging.LogRecord) -> str:
        """Formatting of messages"""
        oncall = super(RedactingFormatter, self).format(record)
        return filter_datum(self.fields, self.REDACTION, oncall, self.SEPARATOR)
    
PII_FIELDS = ("name", "email", "phone", "ssn", "password")
    
def get_logger() -> logging.Logger:
    """A logger function"""
    logger = logging.getLogger('user_data')
    logger.setlevel(logging.INFO)
    logger.propagate = False
    stream = logging.StreamHandler().setFormatter(RedactingFormatter(PII_FIELDS))
    logger.addHandler(stream)
    return logger

def get_db() -> mysql.connector.connection.MySQLConnection:
    """Stores database credientials as environment variable"""
    user = os.getenv('PERSONAL_DATA_DB_USERNAME')
    passwrd = os.getenv('PERSONAL_DATA_DB_PASSWORD')
    host = os.getenv('PERSONAL_DATA_DB_HOST')
    database = os.getenv('PERSONAL_DATA_DB_NAME')
    connector = mysql.connector.connect(user=user, password=passwrd, host=host, database=database)
    return connector