from consolemenu import PromptUtils, Screen
from .ui_list import listCitations
from .ui_pretty import prettyKey, prettyPrintBlock
from colors import red, green

def removeCitations(processor):
    listCitations(processor, "Select an entry to remove.", removeCitation, processor)

def removeCitation(selection, processor):
    pu = PromptUtils(Screen())
    pu.println(prettyPrintBlock(selection))
    pu.println()
    remove = pu.prompt_for_yes_or_no(f"Remove {prettyKey(selection.key)} from library?")
    pu.clear()
    if remove:
        processor.remove(selection)
        pu.println(prettyKey(selection.key), green('removed from library.'), "\n")
    else:
        pu.println(prettyKey(selection.key), red('not removed from library.'), "\n")
    pu.enter_to_continue()
    pu.clear()