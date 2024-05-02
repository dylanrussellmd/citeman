from enum import Enum
from typing import Type
import warnings
from habanero import cn
from Bio import Entrez # type: ignore
import re

# When working with `venv`, to get pylance to work:
# You have to choose the correct interpreter.
# Use shortcuts "Ctrl+Shift+P" and type "Python: Select Interperter" to choose the venv.

class Query:
    def __init__(self, id: Type[str]) -> None:
        if isinstance(id, str):
            self.id = id
        elif isinstance(id, list) and all(isinstance(i, str) for i in id):
            warnings.warn("ID is a list of strings. Using the first element.")
            self.id = id[0]
        else:
            raise TypeError("ID must be a string or a list of strings")
        
        self.type = self._type(self.id)

    @staticmethod
    def _type(id):
        for reid in ReID:
            if re.match(reid.value, id, flags=re.I):
                print(f"Pattern matches: {reid.name}:{id}")
                return reid.name
        raise ValueError("ID is not a valid article identifier")

class ReID(Enum):
    DOI = r"^10\.\d{4,9}\/[-._;()/:A-Z0-9]+$"
    PMID = r"^\d+$"

# https://www.crossref.org/blog/dois-and-matching-regular-expressions/
# Need to review to learn and consolidate.
# When to use static methods?

# consider allowing different urls/formats for cn.contentnegotiation
class CrossRef(Query):
    def __init__(self, id: type[str]) -> None:
        super().__init__(id)
        self.result = self._result(self.id)

    @staticmethod            
    def _result(id):
        try:
            result = cn.content_negotiation(id, format='bibtex', url="https://doi.org")
        except:
            raise
        return result

# https://biopython.org/docs/latest/api/Bio.Entrez.html
# https://www.ncbi.nlm.nih.gov/books/NBK25499/#chapter4.EFetch
class PubMed(Query):
    def __init__(self, id: type[str]) -> None:
        super().__init__(id)
        self.result = self._result(self.id)
    
    @staticmethod            
    def _result(id):
        try:
            Entrez.email = "dyl.russell@gmail.com"
            handle = Entrez.esummary(db="pubmed", id = id, retmode= "xml")
            records = Entrez.parse(handle)
        except:
            raise