
from consolemenu import Screen
from consolemenu.prompt_utils import PromptUtils
from colors import color
from requests import HTTPError
from library import EntrySplitter
from query import CrossRef

def QueryInput():
    pu = PromptUtils(Screen())

    while True:
        input = pu.input(f"Enter {color('DOI', fg='blue')}: ", 
                        enable_quit=True, quit_string="q", 
                        quit_message=f"('{color('q', fg='red')}' to quit)").input_string.strip()
        
        try:
            query = CrossRef(input)
            pu.println(color(f"Found {query.type}", fg="green"), query.id)
        except HTTPError: 
            pu.println(color(f"Unable to find", fg="red"), input)
        except ValueError as e:
            pu.println(color(str(e.args[0]), fg="red"))
        except TypeError as e:
            pu.println(color(str(e.args[0]), fg="red"))

        again = pu.prompt_for_yes_or_no("Search again?")
        if not again:
            break
        pu.clear()

QueryInput()
#doi="10.1126/science.adh7954"
#doi2="poop"
#pmid = "38662827"