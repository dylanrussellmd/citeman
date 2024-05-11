from consolemenu import PromptUtils, Screen, UserQuit
from colors import red, blue, green, strip_color
from .ui_pretty import prettyKey, prettyPrintBlock, prettyPrintQueryReport
from .utils import removeAt, removeBraces
from .processor import CriticalFieldException, KeyExistsError

def QueryInput(processor):
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
        query = processor.getLastQuery()

        # If the query is succesful (i.e., no errors and returns a citation), do:
        if query.success:
            # Print successful query report
            printQuerySuccessReport(pu, query)  
            confirm = pu.prompt_for_yes_or_no("Is this the citation you were looking for? ")
            if confirm:       
                # Check critical fields
                criticalFieldsUI(pu, processor, query.block, ['author', 'year', 'title'])
                # Update the author field (if present) to remove the braces.
                # This is necessary to prevent double brace wrapping of the author field which treats
                # a list of multiple authors as a single author.
                updateAuthorField(processor, query.block)
                # Accept or alter the key of the block
                acceptKeyUI(pu, processor, query.block)
                # Add the block to the library
                addKeyUI(pu, processor, query)
        else:
            # Print query report if query is not successful.
            # Should contain the error message.
            pu.println(prettyPrintQueryReport(query))
        
        again = pu.prompt_for_yes_or_no("Search again?")
        if not again:
            break
        pu.clear()

def printQuerySuccessReport(pu, query):
    pu.println(prettyPrintQueryReport(query))
    pu.println(prettyPrintBlock(query.block))
    pu.println()

def criticalFieldsUI(pu, processor, block, fields):
    while len(fields) > 0:
        field = fields.pop(0)
        try:
            processor.checkCriticalField(block, field)
        except CriticalFieldException as e:
            pu.println(f"{red(e)}{blue(e.field)}.")
            addField = pu.prompt_for_yes_or_no(f"Add {blue(e.field)} field? ")
            if addField:
                value = pu.input(f"Enter {blue(e.field)}: ").input_string.strip()
                processor.addField(block, e.field, value)
                pu.println(f"{blue(e.field)} {green('field added')}.")
                pu.println()

def updateAuthorField(processor, block):
    try:
        processor.updateField(block, 'author', removeBraces(block.get('author').value))
    except:
        pass

def acceptKeyUI(pu, processor, block):
    while True:
        key = pu.input("Enter key (Enter to accept default key): ", default=blue(block.key)).input_string.strip()
        key = removeAt(strip_color(key))
        try:
            processor.keyExists(key)
            if key != block.key:
                processor.updateKey(block, key)
            break
        except KeyExistsError as e:
            pu.println(f"{red(e)}{blue(e.key)}. Please enter a different key.")
            pu.println()

def addKeyUI(pu, processor, query):
    block = query.block
    add = pu.prompt_for_yes_or_no(f"Add {prettyKey(block.key)} to library? ")
    pu.println()
    if add: 
        try:
            processor.add(block)
            pu.println(prettyKey(block.key), green('added to library.'), "\n")
        except:
            raise
    else:
        pu.println(prettyKey(block.key), red('not added to library.'), "\n")



