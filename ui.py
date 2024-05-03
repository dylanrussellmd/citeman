from bibtexparser import Library
from consolemenu import ConsoleMenu, Screen, SelectionMenu
from consolemenu.items import FunctionItem
from consolemenu.prompt_utils import PromptUtils
from colors import color
from requests import HTTPError
from process import Processor
from query import CrossRef
import re

def errorReport(e):
    return f"{color('Error:', fg='red')} {e.args[0]}"

def prettyKey(key):
    key = f"@{key}"
    return f"[{color(key, fg='blue')}]"

def prettyYear(year):
    return color(year, fg='yellow')

def shortAuthor(authors):
    authors = authors.split(" and ")
    if len(authors) > 1:
        return f"{authors[0]} et al."
    return authors[0]

def prettyPrintBlock(block):
    return f"\n{prettyKey(block.key)}\n{block.raw}\n"

def prettyPrintBlockShort(block):
    def removeBraces(string):
        re.sub(r'^\{?(.*)\}?$', r'\1', string)
        
    key = block.key
    author = block.get('author').value
    year = block.get('year').value
    title = block.get('title').value

    string = f"{prettyKey(key)}\n{shortAuthor(author)}, {prettyYear(year)}\n{title}\n"
    return string

def prettyPrintBlocks(blocks):
    return [prettyPrintBlockShort(block) for block in blocks]

def QueryInput(library):
    pu = PromptUtils(Screen())

    while True:
        input = pu.input(f"Enter {color('DOI', fg='blue')}: ", 
                        enable_quit=True, quit_string="q", 
                        quit_message=f"('{color('q', fg='red')}' to quit)").input_string.strip()
        
        try:
            query = CrossRef(input)
            pu.println(color(f"Found {query.type}", fg="green"), query.id)
            processor = Processor(query, library)
            pu.println(prettyPrintBlock(processor.block))
            pu.prompt_for_yes_or_no(f"Add {prettyKey(processor.block.key)} to library?")
            processor.process()
            pu.println(prettyKey(processor.block.key), color('added to library', fg='green'), "\n")
        except HTTPError: 
            pu.println(f"{color('Unable to find', fg='red')} {input}")
        except ValueError as e:
            pu.println(errorReport(e))
        except TypeError as e:
            pu.println(errorReport(e))
        except:
            raise

        again = pu.prompt_for_yes_or_no(f"Search {color('again?', fg='blue')}")
        if not again:
            break
        pu.clear()

def showCitations(library):
    menu = SelectionMenu(prettyPrintBlocks(library.entries))
    menu.show() 

def mainMenu():
    library = Library()
    menu = ConsoleMenu("Pycite", "Select an option:")
    
    menu.append_item(FunctionItem("Query", QueryInput, [library]))
    menu.append_item(FunctionItem("Show Citations", showCitations, [library]))

    menu.show()

doi="10.1126/science.adh7954"
library = Library()
processor = Processor(CrossRef(doi), library)
#processor.process()
print(prettyPrintBlockShort(processor.block))
#
#10.1371/journal.pone.0173664
#doi2="poop"
#pmid = "38662827"