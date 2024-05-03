from library import EntrySplitter
from colors import color

class Processor():
    def __init__(self, query, library):
        self.query = query
        self.library = library
        self.block = self.__block(self.query.result)
    
    def __block(self, result):
        return EntrySplitter(result).split()
 
    def process(self) -> None:
        self.library.add(self.block)