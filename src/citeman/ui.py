from consolemenu import ConsoleMenu
from consolemenu.items import FunctionItem
from .ui_history import showQueryHistory
from .ui_remove import removeCitations
from .ui_show import showCitations
from .ui_query import queryInput
from .processor import Processor
from .bibliography import setup
import pkg_resources

def logo():
    logo_path = pkg_resources.resource_filename(__name__, 'logo')
    with open(logo_path, 'r', encoding="utf-8") as f:
        return ''.join([line for line in f])

def mainMenu():
    library = setup()
    processor = Processor(library)
    subtitle = f"A simple command line citation manager for your academic manuscript."
    menu = ConsoleMenu(logo(), subtitle, show_exit_option=False)
    
    menu.append_item(FunctionItem("Query", queryInput, [processor]))
    menu.append_item(FunctionItem("Show Citations", showCitations, [processor]))
    menu.append_item(FunctionItem("Remove Citations", removeCitations, [processor]))
    menu.append_item(FunctionItem("Show Historical Queries", showQueryHistory, [processor]))

    menu.show()