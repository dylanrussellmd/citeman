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

class TypedList(list):
    """
    A typed list that enforces a specific element type.

    Attributes:
        element_type (type): The type of elements allowed in the list.

    Methods:
        __init__(self, element_type, initial_list): Initializes a TypedList object with an element type and an initial list.
        _validate(self, element): Validates if an element is of the correct type.
        append(self, element): Appends an element to the list after validating its type.
        insert(self, index, element): Inserts an element into the list at a specific index after validating its type.
        extend(self, iterable): Extends the list with elements from an iterable after validating their types.
    """

    def __init__(self, element_type, initial_list=None):
        """
        Initializes a TypedList object with an element type and an initial list.

        Args:
            element_type (type): The type of elements allowed in the list.
            initial_list (list, optional): An initial list to populate the TypedList with. Defaults to None.
        """
        self.element_type = element_type
        if initial_list:
            for element in initial_list:
                self._validate(element)
                super().append(element)

    def _validate(self, element):
        """
        Validates if an element is of the correct type.

        Args:
            element: The element to be validated.

        Raises:
            TypeError: If the element is not of the correct type.
        """
        if not isinstance(element, self.element_type):
            raise TypeError(f"Only {self.element_type.__name__} elements are allowed")

    def append(self, element):
        """
        Appends an element to the list after validating its type.

        Args:
            element: The element to be appended.
        """
        self._validate(element)
        super().append(element)

    def insert(self, index, element):
        """
        Inserts an element into the list at a specific index after validating its type.

        Args:
            index (int): The index at which to insert the element.
            element: The element to be inserted.
        """
        self._validate(element)
        super().insert(index, element)

    def extend(self, iterable):
        """
        Extends the list with elements from an iterable after validating their types.

        Args:
            iterable (iterable): The iterable containing elements to be added to the list.
        """
        for element in iterable:
            self._validate(element)
        super().extend(iterable)