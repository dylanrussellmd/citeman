from consolemenu import PromptUtils, Screen
from .ui_list import listCitations
from .ui_pretty import prettyKey, prettyPrintBlock
from colors import red, green

def removeCitations(processor):
    listCitations(processor, "Select an entry to remove.", removeCitation)

def removeCitation(block, processor):
    pu = PromptUtils(Screen())
    pu.println(prettyPrintBlock(block))
    pu.println()
    remove = pu.prompt_for_yes_or_no(f"Remove {prettyKey(block.key)} from library?")
    if remove:
        processor.remove(block)
        pu.println(prettyKey(block.key), green('removed from library.'), "\n")
    else:
        pu.println(prettyKey(block.key), red('not removed from library.'), "\n")
    pu.enter_to_continue()
    pu.clear()