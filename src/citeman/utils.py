import re

def removeBraces(string):
    """
    Removes ending braces from the given string.

    Args:
        string (str): The input string.

    Returns:
        str: The string with braces removed.
    """
    return re.sub(r'^\{?(.*?)\}?$', r'\1', string)

def removeAt(s):
    return re.sub(r'^@+', '', s)

def isFieldMissing(block, str):
    return block.get(str) is None