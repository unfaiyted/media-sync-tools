import re


def is_uuid(string):
    """Check if string is a valid UUID"""
    regex = r'^[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}\Z'
    match = re.fullmatch(regex, string, re.I)
    return bool(match)

