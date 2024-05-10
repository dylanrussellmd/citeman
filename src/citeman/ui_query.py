def QueryInput(processor):
    pu = PromptUtils(Screen())

    while True:
        try:
            input = pu.input(f"Enter {color('DOI', fg='blue')}: ", 
                            enable_quit=True, quit_string="q", 
                            quit_message=f"('{color('q', fg='red')}' to quit)").input_string.strip()
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
            # Check critical fields
            criticalFieldsUI(pu, processor, query.block, ['author', 'year', 'title'])
            
            # Update the author field (if present) to remove the braces.
            # This is necessary to prevent double brace wrapping of the author field which treats
            # a list of multiple authors as a single author.
            if not isFieldMissing(query.block, 'author'):
                processor.updateField(query.block, 'author', removeBraces(query.block.get('author').value))
            
            while True:
                key = removeAt(pu.input("Enter key (Enter to accept default key): ", default=color(f"{block.key}", fg='blue')).input_string.strip())
                if key != block.key:
                        try:
                            processor.changeKey(block, key)
                            break
                        except ValueError as e:
                            pu.println(f"{color(e, fg='red')} Please enter a different key.")
                            pu.println()
                else:
                    break
            add = pu.prompt_for_yes_or_no(f"Add {prettyKey(block.key)} to library?")
            pu.println()
            if add: 
                try:
                    processor.add(block)
                    pu.println(prettyKey(block.key), color('added to library.', fg='green'), "\n")
                except ValueError as e:
                    pu.println(prettyKey(block.key), color('appears to be a duplicate key.', fg='red'))
                    processor.removeDuplicateBlocks()
                    if processor.compare(query):
                        pu.println(prettyKey(block.key), color(f"already exists in library with matching {query.type} {query.id}.", fg='red'))
                        pu.println(prettyKey(block.key), color('not added to library.', fg='red'))
                    else:
                        pu.println("The duplicate", prettyKey(block.key), f"does not exist in the library with a matching {query.type}.")
                        alternate = pu.prompt_for_yes_or_no(f"Add {prettyKey(block.key)} to library with an alternate key?")
                        pu.println()
                        if alternate:
                            processor.incrementKey(block)
                            processor.add(block)
                            pu.println(prettyKey(block.key), color('added to library with alternate key.', fg='green'), "\n")
                        else:
                            pu.println(prettyKey(block.key), color('not added to library.', fg='red'))
            else:
                pu.println(prettyKey(block.key), color('not added to library.', fg='red'), "\n")
        else:
            pu.println(queryReport(query))
        
        again = pu.prompt_for_yes_or_no(f"Search {color('again?', fg='blue')}")
        if not again:
            break
        pu.clear()

def printQuerySuccessReport(pu, query):
    pu.println(queryReport(query))
    pu.println(prettyPrintBlock(query.block))
    pu.println()

def criticalFieldsUI(pu, processor, block, fields):
    while len(fields) > 0:
        field = fields.pop(0)
        try:
            processor.checkCriticalField(block, field)
        except CriticalFieldException as e:
            pu.println(color(f"Missing {e.field} field.", fg='red'))
            addField = pu.prompt_for_yes_or_no(f"Add {color(e.field, fg='blue')} field?")
            if addField:
                value = pu.input(f"Enter {color(e.field, fg='blue')}: ").input_string.strip()
                processor.addField(block, e.field, value)
                pu.println(f"{color(e.field, fg='blue')} {color('field added', fg='green')}.")
                pu.println()       


