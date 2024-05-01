from enum import Enum
import warnings
from habanero import cn
from Bio import Entrez # type: ignore
import re
import xml.etree.ElementTree as ET

# When working with `venv`, to get pylance to work:
# You have to choose the correct interpreter.
# Use shortcuts "Ctrl+Shift+P" and type "Python: Select Interperter" to choose the venv.

doi="10.1126/science.adh7954"
doi2="poop"
pmid = "38662827"

class Source:
    def __init__(self, query):
        if isinstance(query, str):
            self.query = [query]
        elif isinstance(query, list) and all(isinstance(i, str) for i in query):
            self.query = query
        else:
            raise TypeError("query must be a string or a list of strings")
        
        self.id = ID(self.query)
        self.result = self._result(self.id)

    @staticmethod
    def _result(id):
        pass

class ReID(Enum):
    DOI = r"^10\.\d{4,9}\/[-._;()/:A-Z0-9]+$"
    PMID = r"^\d+$"

# https://www.crossref.org/blog/dois-and-matching-regular-expressions/
# Need to review to learn and consolidate.
# When to use static methods?
class ID:
    def __init__(self, id):
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

# consider allowing different urls/formats for cn.contentnegotiation
class CrossRef(Source):
            
    @staticmethod            
    def _result(id):
        try:
            result = cn.content_negotiation(id.id, format='bibtex', url="https://doi.org")
        except:
            raise
        return result

# https://biopython.org/docs/latest/api/Bio.Entrez.html
# https://www.ncbi.nlm.nih.gov/books/NBK25499/#chapter4.EFetch
class PubMed(Source):
            
    @staticmethod            
    def _result(id):
        try:
            Entrez.email = "dyl.russell@gmail.com"
            handle = Entrez.esummary(db="pubmed", id = id.id, retmode= "xml")
            records = Entrez.parse(handle)
        except:
            raise

print(CrossRef(doi2).result)