from consolemenu import PromptUtils, Screen
from .ui_list import listQueries
from .ui_pretty import prettyPrintQuery

def showQueries(processor):
    listQueries(processor, "Select a query to view.", showQuery)
        
def showQuery(selection):
    pu = PromptUtils(Screen())
    pu.println(prettyPrintQuery(selection))
    pu.enter_to_continue()
    pu.clear()