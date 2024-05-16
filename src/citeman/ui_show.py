from consolemenu import PromptUtils, Screen
from .ui_list import listCitations
from .ui_pretty import prettyPrintBlock

def showCitations(processor):
    listCitations(processor, "Select an entry to view.", showCitation)
        
def showCitation(selection):
    pu = PromptUtils(Screen())
    pu.println(prettyPrintBlock(selection))
    pu.enter_to_continue()
    pu.clear()