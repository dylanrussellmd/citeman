from consolemenu import ConsoleMenu, Screen, SelectionMenu
from consolemenu.items import FunctionItem
from consolemenu.prompt_utils import PromptUtils 
from colors import color
from .ui_pretty import prettyKey, prettyPrintBlock, prettyPrintBlocks
from .ui_query import QueryInput
from .processor import Processor
from .bibliography import setup
import pkg_resources

def libraryIsEmpty(processor):
    if not processor.library.entries:
        pu = PromptUtils(Screen())
        pu.println(f"Library is {color('empty', fg='red')}.")
        pu.enter_to_continue()
        return True
    return False

def queryHistoryIsEmpty(processor):
    if not processor.queryHistory:
        pu = PromptUtils(Screen())
        pu.println(f"Query history is {color('empty', fg='red')}.")
        pu.enter_to_continue()
        return True
    return False

def showCitations(processor):
    if libraryIsEmpty(processor):
        return
    title = "Select an entry to view detailed information."
    entries = processor.library.entries
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
    pu.clear()

def removeCitations(processor):
    while True:
        if libraryIsEmpty(processor):
            return
        title = "Select an entry to remove."
        entries = processor.library.entries
        exit = len(entries)
        selection = SelectionMenu.get_selection(prettyPrintBlocks(entries), title=title)
        try:
            removeCitation(entries[selection], processor)
        except IndexError:
            if selection == exit:
                break

def removeCitation(block, processor):
    pu = PromptUtils(Screen())
    pu.println(prettyPrintBlock(block))
    remove = pu.prompt_for_yes_or_no(f"Remove {prettyKey(block.key)} from library?")
    if remove:
        processor.remove(block)
        pu.println(prettyKey(block.key), color('removed from library.', fg='green'), "\n")
    else:
        pu.println(prettyKey(block.key), color('not removed from library.', fg='red'), "\n")
    pu.enter_to_continue()
    pu.clear()

#def showHistoricalQueries(processor):
#    while True:
#        if queryHistoryIsEmpty(processor):
#            return
#        title = "Select a previous query to view."
#        queries = processor.queryHistory
#        exit = len(queries)
#        selection = SelectionMenu.get_selection(prettyPrintQueries(queries), title=title)
#        try:
#            pass
#        except IndexError:
#            if selection == exit:
#                break

def logo():
    logo_path = pkg_resources.resource_filename(__name__, 'logo')
    with open(logo_path, 'r', encoding="utf-8") as f:
        return ''.join([line for line in f])

def mainMenu():
    library = setup()
    processor = Processor(library)
    subtitle = f"A simple command line citation manager for your academic manuscript."
    menu = ConsoleMenu(logo(), subtitle, show_exit_option=False)
    
    menu.append_item(FunctionItem("Query", QueryInput, [processor]))
    menu.append_item(FunctionItem("Show Citations", showCitations, [processor]))
    menu.append_item(FunctionItem("Remove Citations", removeCitations, [processor]))
    #menu.append_item(FunctionItem("Show Historical Queries", showHistoricalQueries, [processor]))

    menu.show()