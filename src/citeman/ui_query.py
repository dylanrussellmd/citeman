from consolemenu import PromptUtils, Screen, UserQuit
from colors import red, blue, green, strip_color
from .ui_pretty import prettyKey, prettyPrintBlock, prettyPrintQueryReport
from .utils import removeAt, removeBraces
from .errors import CriticalFieldException, KeyExistsError

def queryInput(processor):
    pu = PromptUtils(Screen())
    while True:
        try:
            input = pu.input(f"Enter {blue('DOI')}: ", 
                            enable_quit=True, quit_string="q", 
                            quit_message=f"('{red('q')}' to quit)").input_string.strip()
        except UserQuit:
            break
        # Make the query and then return the last query from processor.
        # The last query should be the query just processed.    
        processor.processQuery(input)
        pu.clear()
        query = processor.getLastQuery()
        pu.println(prettyPrintQueryReport(query))
        # If the query is succesful (i.e., no errors and returns a citation), do:
        if query.success:
            pu.println()
            pu.println(query.raw)
            pu.println()
            confirm = pu.prompt_for_yes_or_no("Is this the citation you were looking for? ")

            if confirm:       
                criticalFieldsUI(pu, processor, query, ['author', 'year', 'title'])
                # Update the author field (if present) to remove the braces.
                # This is necessary to prevent double brace wrapping of the author field which treats
                # a list of multiple authors as a single author.
                updateAuthorField(processor, query)
                acceptKeyUI(pu, processor, query)
                addKeyUI(pu, processor, query)
        
        again = pu.prompt_for_yes_or_no("Search again?")
        if not again:
            break
        pu.clear()

def criticalFieldsUI(pu, processor, query, fields):
    while len(fields) > 0:
        field = fields.pop(0)
        try:
            processor.checkCriticalField(query.block, field)
        except CriticalFieldException as e:
            pu.println(f"{red(e)}{blue(e.field)}.")
            addField = pu.prompt_for_yes_or_no(f"Add {blue(e.field)} field? ")
            if addField:
                value = pu.input(f"Enter {blue(e.field)}: ").input_string.strip()
                processor.addField(query.block, e.field, value)
                pu.println(f"{blue(e.field)} {green('field added')}.")
                pu.println()

def updateAuthorField(processor, query):
    try:
        processor.updateField(query.block, 'author', removeBraces(query.block.get('author').value))
    except:
        pass

def acceptKeyUI(pu, processor, query):
    while True:
        pu.clear()
        key = pu.input("Enter key (Enter to accept default key): ", default=blue(query.block.key)).input_string.strip()
        key = removeAt(strip_color(key))
        try:
            processor.keyExists(key)
            if key != query.block.key:
                processor.updateKey(query.block, key)
            break
        except KeyExistsError as e:
            pu.println(f"{red(e)}{blue(e.key)}. Please enter a different key.")

def addKeyUI(pu, processor, query):
    pu.clear()
    add = pu.prompt_for_yes_or_no(f"Add {prettyKey(query.block.key)} to library? ")
    pu.clear()
    if add: 
        try:
            processor.add(query.block)
            pu.println(prettyKey(query.block.key), green('added to library.'), "\n")
        except:
            raise
    else:
        pu.println(prettyKey(query.block.key), red('not added to library.'), "\n")