import logging
import re

# Online tool for testing regular expressions
# https://regex101.com/ or https://regexr.com/

windows_drive_letter = re.compile(r'^([a-zA-Z]:)')
legal_filename_chars = re.compile(r'[\w \.\{\}\[\]\(\)\-\\\/]')
illegal_filename_chars = re.compile(r'[^\w \.\{\}\[\]\(\)\-\\\/]')

email_address = re.compile(r'\b[\w\.\'\-]{1,64}\@[\w\.\'\-]{1,184}(?:\.[a-zA-Z]{2,4})\b')

short_date = re.compile(r'\b(?:\d|\d{2})[ \.\-\\\/]\d{2}[ \.\-\\\/]\d{2}(?:\d{2})?\b')
long_date = re.compile(r'\b(?:\d|\d{2}) ?(?:(?:[sS][tT])|(?:[nN][dD])|(?:[rR][dD])|(?:[tT][hH]))? ?(?:[A-Z][a-zA-Z]{2,8}) ?\d{2}(?:\d{2})?\b')

currency = re.compile(r'')

uk_tel_number = re.compile(r'\b(?:00 ?44|\+ ?44|0)(?: ?\d){9,10}\b')
uk_postcode = re.compile(r'\b(?:[A-Z]|[A-Z]{2})(?:\d|\d{2})[A-Z]? \d[A-Z]{2}\b')
uk_vehicle_reg = re.compile(r'\b[A-Z]{2}\d{2} ?[A-Z]{3}\b')