from bibtexparser import Library
from consolemenu import ConsoleMenu, Screen, SelectionMenu
from consolemenu.items import FunctionItem
from consolemenu.prompt_utils import PromptUtils, UserQuit
from colors import color
from processor import Processor
import re

def removeBraces(string):
    return re.sub(r'^\{?(.*?)\}?$', r'\1', string)

def prettyKey(key):
    key = f"[@{key}]"
    return f"{color(key, fg='blue')}"

def prettyYear(year):
    year = removeBraces(year)
    return color(year, fg='yellow')

def prettyAuthor(authors):
    authors = removeBraces(authors)
    authors = authors.split(" and ")
    author = authors[0].split(", ")
    if len(author) > 1:
        author = f"{author[0]}, {author[1][:1]}."
    else:
        author = author[0]

    if len(authors) > 1:
        author = f"{author} et al."

    return color(author, fg='blue')

def prettyTitle(title):
    title = removeBraces(title)
    return color(title, fg='green')

def prettyPrintBlock(block):
    return f"\n{prettyKey(block.key)}\n{block.raw}\n"

def prettyPrintBlockShort(block):
        
    author = block.get('author').value
    year = block.get('year').value
    title = block.get('title').value

    string = f"{prettyAuthor(author)}, {prettyYear(year)}, {prettyTitle(title)}\n"
    return string

def prettyPrintBlocks(blocks):
    return [prettyPrintBlockShort(block) for block in blocks]

def QueryInput(processor):
    pu = PromptUtils(Screen())

    while True:
        try:
            input = pu.input(f"Enter {color('DOI', fg='blue')}: ", 
                            enable_quit=True, quit_string="q", 
                            quit_message=f"('{color('q', fg='red')}' to quit)").input_string.strip()
        except UserQuit:
            break
            
        processor.processQuery(input)
        query = processor.getLastQuery()
        if query.success:
            block = query.block
            pu.println(color(f"Found {query.type}", fg="green"), query.id)
            pu.println(prettyPrintBlock(block))
            add = pu.prompt_for_yes_or_no(f"Add {prettyKey(block.key)} to library?")
            if add: 
                processor.add(block)
                pu.println(prettyKey(block.key), color('added to library', fg='green'), "\n")
            else:
                pu.println(prettyKey(block.key), color('not added to library', fg='red'), "\n")
        else:
            pu.println(query.result)
        
        again = pu.prompt_for_yes_or_no(f"Search {color('again?', fg='blue')}")
        if not again:
            break
        pu.clear()

def showCitations(library):
    title = "Select an entry to view detailed information."
    entries = library.entries
    exit = len(entries)
    while True:
        selection = SelectionMenu.get_selection(prettyPrintBlocks(entries), title=title)
        try:
            showCitation(entries[selection])
        except IndexError:
            if selection == exit:
                break
        
def showCitation(selection):
    pu = PromptUtils(Screen())
    pu.println(prettyPrintBlock(selection))
    pu.enter_to_continue()

def mainMenu():
    library = Library()
    processor = Processor(library)
    menu = ConsoleMenu("Pycite", "Select an option:")
    
    menu.append_item(FunctionItem("Query", QueryInput, [processor]))
    menu.append_item(FunctionItem("Show Citations", showCitations, [library]))

    menu.show()
#
#doi="10.1371/journal.pone.0173664"
#library = Library()
#query = CrossRef(doi)
#processor = Processor(query, library)
#processor.process()
#showCitations(library)

mainMenu()
#
#doi2="poop"
#pmid = "38662827"