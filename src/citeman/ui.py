from consolemenu import ConsoleMenu, MenuFormatBuilder
from consolemenu.items import FunctionItem
from consolemenu.menu_component import Dimension
from colors import blue
from .ui_history import showQueries
from .ui_remove import removeCitations
from .ui_show import showCitations
from .ui_query import queryInput
from .prepare import prepare_library, prepare_processor
import pkg_resources

def logo():
    logo_path = pkg_resources.resource_filename(__name__, 'logo')
    with open(logo_path, 'r', encoding="utf-8") as f:
        return ''.join([line for line in f])
    
class MainMenu(ConsoleMenu):
    def __init__(self):
        formatter = MenuFormatBuilder(max_dimension=Dimension(width=100, height = 50))
        formatter.set_border_style_type(3)
        formatter.set_title_align("center")
        formatter.set_subtitle_align("center")
        formatter.set_prompt("Select: ")
        title = logo()
        subtitle = f"A simple {blue('command line citation manager')} for your academic manuscript."
        super().__init__(title=title,
                         subtitle=subtitle,
                         show_exit_option=False,
                         formatter=formatter)

def mainMenu():
    library = prepare_library()
    processor = prepare_processor(library)
    menu = MainMenu()
    
    menu.append_item(FunctionItem("Query", queryInput, [processor]))
    menu.append_item(FunctionItem("Show citations", showCitations, [processor]))
    menu.append_item(FunctionItem("Remove citations", removeCitations, [processor]))
    menu.append_item(FunctionItem("View query history", showQueries, [processor]))

    menu.show()