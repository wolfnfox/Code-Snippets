import logging
import re

# Online tool for testing regular expressions
# https://regex101.com/

windows_drive_letter = re.compile(r'^([a-zA-Z]:)')
legal_filename_chars = re.compile(r'[a-zA-Z0-9 \.\{\}\[\]\(\)\-\_\\\/]')
illegal_filename_chars = re.compile(r'[^a-zA-Z0-9 \.\{\}\[\]\(\)\-\_\\\/]')

uk_postcode = re.compile(r'([A-Z]|[A-Z]{2})([0-9]{1}|[0-9]{2})([A-Z]? [0-9][A-Z]{2})')
uk_vehicle_reg = re.compile(r'([A-Z]{2} ?[0-9]{2} ?[A-Z]{3})')