from query import CrossRef, Query

class Processor():
    def __init__(self, library):
        self.library = library
        self.queryHistory = TypedList(Query) 

    def processQuery(self, input):
        try:
            query = CrossRef(input)
            self.queryHistory.append(query)
        except:
            raise
    
    def add(self, block) -> None:
        self.library.add(block)

    def remove(self, block) -> None:
        self.library.remove(block)

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