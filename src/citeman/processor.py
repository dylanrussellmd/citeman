from bibtexparser.model import DuplicateBlockKeyBlock, Field
from bibtexparser.entrypoint import write_file
from pickle import dump
from .errors import CriticalFieldException, FieldExistsError, FieldMissingError, HistoryEmptyError, KeyExistsError, LibraryEmptyError
from .entry import getEntryRaw
from .query import CrossRef, Query
from .utils import removeBraces

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
            library (Library): The library object that stores the entries.
        """
        self.library = library
        self._queryHistory = list()

    @property
    def entries(self):
        if not self.library.entries:
            raise LibraryEmptyError()
        return self.library.entries

    @property 
    def queryHistory(self):
        if not self._queryHistory:
            raise HistoryEmptyError()
        return self._queryHistory
    
    def overwriteLibrary(self, library):
        self.library = library

    def save(self):
        with open('citeman.p', 'wb') as f:
            dump(self, f)

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
            self._queryHistory.append(query)
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

        self._write()
        self.save()

    def remove(self, block) -> None:
        """
        Removes a block from the library and writes the library to .bib file.

        Args:
            block (Block): The block to be removed from the library.
        """
        self.library.remove(block)
        self._write()
        self.save()

    @staticmethod
    def updateEntryRaw(block) -> None:
        block._raw = getEntryRaw(block)

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
        Processor.updateEntryRaw(block)

    @staticmethod
    def addField(block, field, value) -> None:
        try:
            Processor.fieldExists(block, field)
        except:
            raise

        block.set_field(Field(field, value))
        Processor.updateEntryRaw(block)

    @staticmethod
    def updateKey(block, key) -> None:
        """
        Changes the key of a block in the library.

        Args:
            block (Block): The block whose key is to be changed.
            key (str): The new key to assign to the block.
        """
        block.key = key
        block._raw = getEntryRaw(block)

    def _write(self) -> None:
        """
        Writes the library to .bib file.
        """
        bib = 'bibliography.bib'
        write_file(bib, self.library)

    def idExists(self, query):
        """
        Compares a given article ID with the library.

        Args:
            id (str): The article ID to compare.

        Returns:
            bool: True if the article ID is in the library, False otherwise.
        """
        try:
            entries = self.entries
        except LibraryEmptyError:
            return False
        type = query.type
        for entry in entries:
            id = removeBraces(entry.get(type).value)
            if id is not None and id == query.id:
                    return True
            else:
                return False
    
    def keyExists(self, key):
        try:
            entries = self.entries
        except LibraryEmptyError:
            return
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
    
    # MIGHT NOT BE NEEDED
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