import re

def removeBraces(string):
    """
    Removes starting and ending braces from the given string.
    Only removes up to a single pair of outer braces.
    Does not requires a matching pair to remove.
    Will remove a singlar starting or ending braces.

    Args:
        string (str): The input string.

    Returns:
        str: The string with braces removed.
    """
    return re.sub(r'^\{?(.*?)\}?$', r'\1', string)

def removeAt(s):
    """
    Removes leading '@' characters from the given string.
    Will remove all leading '@' characters.
    Does not remove non-leading '@' characters.

    Args:
        s (str): The input string.

    Returns:
        str: The string with leading '@' characters removed.
    """
    return re.sub(r'^@+', '', s)
