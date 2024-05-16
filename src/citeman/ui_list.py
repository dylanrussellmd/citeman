from consolemenu import SelectionMenu
from .ui_notice import noticeScreen
from .ui_pretty import prettyPrintBlocks, prettyPrintQueries
from .errors import HistoryEmptyError, LibraryEmptyError
from colors import red

def listCitations(processor, message, action, *args):
    while True:
        try:
            entries = processor.entries
        except LibraryEmptyError as e:
            noticeScreen(e, red)
            break

        exit = len(entries)
        try:
            selection = SelectionMenu.get_selection(prettyPrintBlocks(entries), title=message)
            action(entries[selection], *args)
        except IndexError:
            if selection == exit:
                break

def listQueries(processor, message, action, *args):
    while True:
        try:
            queries = processor.queryHistory
        except HistoryEmptyError as e:
            noticeScreen(e, red)
            break
        exit = len(queries)
        try:
            selection = SelectionMenu.get_selection(prettyPrintQueries(queries), title=message)
            action(queries[selection], *args)
        except IndexError:
            if selection == exit:
                break
