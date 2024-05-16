import os
from bibtexparser.entrypoint import parse_file
from bibtexparser.library import Library
from pickle import load
from citeman.processor import Processor

def prepare_library():
    bib = 'bibliography.bib'
    if not os.path.exists(bib):
        # Create the file if it doesn't exist
        with open(bib, 'a'):
            pass
        return Library()

    # Read the file into a library object
    return parse_file(bib)

def prepare_processor(library):
    pickle = 'citeman.p'
    if not os.path.exists(pickle):
        # Create the file if it doesn't exist
        with open(pickle, 'w'):
            pass
        processor = Processor(library)
        processor.save()
        return processor
    
    # Read in pickle file
    with open(pickle, 'rb') as f:
        processor = load(f)
    processor.overwriteLibrary(library)
    return processor