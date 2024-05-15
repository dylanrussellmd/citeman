from consolemenu import SelectionMenu
from .ui_notice import noticeScreen
from .ui_pretty import prettyPrintBlocks
from .errors import LibraryEmptyError
from colors import red

def listCitations(processor, message, action):
    try:
        entries = processor.entries
    except LibraryEmptyError as e:
        noticeScreen(e, red)
        return
    exit = len(entries)
    selection = SelectionMenu.get_selection(prettyPrintBlocks(entries), title=message)
    while True:        
        try:
            action(entries[selection])
        except IndexError:
            if selection == exit:
                break
