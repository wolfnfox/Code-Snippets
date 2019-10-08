import re

# Online tool for testing regular expressions
# https://regex101.com/ or https://regexr.com/

windows_drive_letter = re.compile(r'^([a-zA-Z]:)')
legal_basefilename_chars = re.compile(r'[\w \.\{\}\[\]\(\)\-]')
illegal_basefilename_chars = re.compile(r'[^\w \.\{\}\[\]\(\)\-]')
legal_path_chars = re.compile(r'[\w \.\{\}\[\]\(\)\-\\\/]')
illegal_path_chars = re.compile(r'[^\w \.\{\}\[\]\(\)\-\\\/]')

legal_url_chars = re.compile(r'[a-zA-Z0-9\-\_\.\~\:\/\?\#\[\]\@\!\$\&\'\(\)\*\+\,\;\=]')
illegal_url_chars = re.compile(r'[^a-zA-Z0-9\-\_\.\~\:\/\?\#\[\]\@\!\$\&\'\(\)\*\+\,\;\=]')

email_address = re.compile(r'\b[\w\.\'\-]{1,64}\@[\w\.\'\-]{1,184}(?:\.[a-zA-Z]{2,4})\b')
http_url = re.compile(r'\b(?:https?:\/\/)?(?:www.)?(?:[a-zA-Z0-9\-\_\.\~\:\/\?\#\[\]\@\!\$\&\'\(\)\*\+\,\;\=]+)')

short_date = re.compile(r'\b(?:\d|\d{2})[ \.\-\\\/]\d{2}[ \.\-\\\/]\d{2}(?:\d{2})?\b')
long_date = re.compile(r'\b(?:\d|\d{2}) ?(?:(?:[sS][tT])|(?:[nN][dD])|(?:[rR][dD])|(?:[tT][hH]))? ?(?:[A-Z][a-zA-Z]{2,8}) ?\d{2}(?:\d{2})?\b')

number = re.compile(r'(?:[+-] ?)?(?:\d{1,3})(?:\,?\d{3})*(?:\.\d+)?')
currency = re.compile(r'(?:[+-] ?)?(?:[£$€] ?)?(?:\d{1,3})(?:\,?\d{3})*(?:\.\d+)?[cp]?\b')

uk_tel_number = re.compile(r'\b(?:00 ?44|\+ ?44|0)(?: ?\d){9,10}\b')
uk_postcode = re.compile(r'\b(?:[A-Z]|[A-Z]{2})(?:\d|\d{2})[A-Z]? \d[A-Z]{2}\b')
uk_vehicle_reg = re.compile(r'\b[A-Z]{2}\d{2} ?[A-Z]{3}\b')
