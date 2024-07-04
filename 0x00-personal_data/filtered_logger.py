#!/usr/bin/env python3
"""
Main file
"""
import re


def filter_datum(fields, redaction, message, separator):
    """sequence function"""
    pattern = f"({'|'.join(map(re.escape, fields))})=([^ {separator}]*)"
    return re.sub(pattern, lambda m: f"{m.group(1)}={redaction}", message)
