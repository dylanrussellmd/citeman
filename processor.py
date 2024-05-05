from query import CrossRef, Query
from colors import color
from requests import HTTPError

class Processor():
    def __init__(self, library):
        self.library = library
        self.queryHistory = TypedList(Query) 

    def processQuery(self, input):
        try:
            query = CrossRef(input)
            query.makeBlock()
        except HTTPError:
            error = f"{color('Unable to find', fg='red')} {input}"
            query.fail(error)
        except ValueError as e:
            query.fail(errorReport(e))
        except TypeError as e:
            query.fail(errorReport(e))
        except:
            raise
        self.queryHistory.append(query)

    def add(self, block) -> None:
        self.library.add(block)

    def getQuery(self, index) -> Query:
        return self.queryHistory[index]

    def getLastQuery(self) -> Query:
        return self.getQuery(-1)
    
class TypedList(list):
    def __init__(self, element_type, initial_list=None):
        self.element_type = element_type
        if initial_list:
            for element in initial_list:
                self._validate(element)
                super().append(element)

    def _validate(self, element):
        if not isinstance(element, self.element_type):
            raise TypeError(f"Only {self.element_type.__name__} elements are allowed")

    def append(self, element):
        self._validate(element)
        super().append(element)

    def insert(self, index, element):
        self._validate(element)
        super().insert(index, element)

    def extend(self, iterable):
        for element in iterable:
            self._validate(element)
        super().extend(iterable)

def errorReport(e):
    return f"{color('Error:', fg='red')} {e.args[0]}"