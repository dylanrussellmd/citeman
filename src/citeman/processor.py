from bibtexparser.model import DuplicateBlockKeyBlock, Field
from .parser import getBlockRaw
from .query import CrossRef, Query
from .bibliography import write
from .utils import TypedList, removeBraces

class Processor():
    """
    A class that represents a processor for handling queries and managing a library.
    All interactions between the user and the Library/.bib file are handled by the Processor.

    Attributes:
        library (Library): The library object that stores the blocks.
        queryHistory (TypedList): A typed list that stores the query history.

    Methods:
        __init__(self, library): Initializes a Processor object with a library.
        processQuery(self, input): Processes a query and adds it to the query history.
        add(self, block): Adds a block to the library and writes the library to .bib file.
        remove(self, block): Removes a block from the library and writes the library .bib file.
        write(self): Writes the library to .bib file.
        getQuery(self, index): Retrieves a query from the query history based on the index.
        getLastQuery(self): Retrieves the last query from the query history.
    """

    def __init__(self, library):
        """
        Initializes a Processor object with a library.

        Args:
            library (Library): The library object that stores the blocks.
        """
        self.library = library
        self.queryHistory = TypedList(Query) 

    def processQuery(self, input):
        """
        Processes a query and adds it to the query history.

        Args:
            input (str): The article ID to query.

        Raises:
            Exception: If an error occurs while processing the query.
            Should only be raising unanticipated exceptions as most have been
            handled in the Query class.
        """
        try:
            query = CrossRef(input)
            self.queryHistory.append(query)
        except:
            raise
    
    def add(self, block) -> None:
        """
        Adds a block to the library and writes the library to .bib file.

        Args:
            block (Block): The block to be added to the library.
        """
        try:
            self.library.add(block, fail_on_duplicate_key=True)
        except:
            raise

        self.write()

    def remove(self, block) -> None:
        """
        Removes a block from the library and writes the library to .bib file.

        Args:
            block (Block): The block to be removed from the library.
        """
        self.library.remove(block)
        self.write()
    
    @staticmethod
    def updateBlockRaw(block) -> None:
        block._raw = getBlockRaw(block)

    @staticmethod
    def checkCriticalField(block, field):
        try:
            Processor.fieldMissing(block, field)
        except:
            raise CriticalFieldException(field)

    @staticmethod
    def updateField(block, field, value) -> None:
        try:
            Processor.fieldMissing(block, field)
        except:
            raise
        
        block.set_field(Field(field, value))
        Processor.updateBlockRaw(block)

    @staticmethod
    def addField(block, field, value) -> None:
        try:
            Processor.fieldExists(block, field)
        except:
            raise

        block.set_field(Field(field, value))
        Processor.updateBlockRaw(block)

    @staticmethod
    def updateKey(block, key) -> None:
        """
        Changes the key of a block in the library.

        Args:
            block (Block): The block whose key is to be changed.
            key (str): The new key to assign to the block.
        """
        block.key = key
        block._raw = getBlockRaw(block)

    def write(self) -> None:
        """
        Writes the library to .bib file.
        """
        write(self.library)

    def idExists(self, query):
        """
        Compares a given article ID with the library.

        Args:
            id (str): The article ID to compare.

        Returns:
            bool: True if the article ID is in the library, False otherwise.
        """
        entries = self.library.entries
        type = query.type
        for entry in entries:
            id = removeBraces(entry.get(type).value)
            if id is not None and id == query.id:
                    return True
            else:
                return False
    
    def keyExists(self, key):
        """
        Checks if a key already exists in the library.

        Args:
            key (str): The key to check.

        Returns:
            bool: True if the key exists in the library, False otherwise.
        """
        entries = self.library.entries
        for entry in entries:
            if entry.key == key:
                raise KeyExistsError(key)
    
    @staticmethod
    def fieldExists(block, field):
        if block.get(field) is not None:
            raise FieldExistsError(field)
    
    @staticmethod
    def fieldMissing(block, field):
        if block.get(field) is None:
            raise FieldMissingError(field)
            
    def incrementKey(self, block):
        """
        Increments the key of a block in the library to avoid duplicates.

        Args:
            key (str): The new key to assign to the block.
        """
        key_v = 1
        new_key = block.key + f"_{key_v}"
        while True:
            try:
                key_v += 1
                new_key = block.key + f"_{key_v}"
                self.keyExists(new_key)
                break
            except KeyExistsError:
                pass
        block.key = new_key
            
    def removeDuplicateBlocks(self):
        """
        Removes duplicate blocks from the library.
        """
        duplicates = [block for block in self.library.blocks if isinstance(block, DuplicateBlockKeyBlock)]
        self.library.remove(duplicates)

    def getQuery(self, index) -> Query:
        """
        Retrieves a query from the query history based on the index.

        Args:
            index (int): The index of the query in the query history.

        Returns:
            Query: The query object.
        """
        return self.queryHistory[index]

    def getLastQuery(self) -> Query:
        """
        Retrieves the last query from the query history.

        Returns:
            Query: The last query object in the query history.
        """
        return self.getQuery(-1)
    
class CriticalFieldException(Exception):
    def __init__(self, field):
        self.field = field
        super().__init__("Missing critical field: ")

class KeyExistsError(ValueError):
    def __init__(self, key) -> None:
        self.key = key
        super().__init__("Key already exists: ")

class FieldExistsError(ValueError):
    def __init__(self, field) -> None:
        self.field = field
        super().__init__("Field already exists: ")

class FieldMissingError(ValueError):
    def __init__(self, field) -> None:
        self.field = field
        super().__init__("Field missing: ")