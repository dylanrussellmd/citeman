from colors import green, red, blue, yellow
from .utils import removeBraces

def prettyPrintQueryShort(query):
    if query.success:
        return f"{query.id} - {green('Success')}"
    elif not query.success:
        return f"{query.id} - {red('Failure')}"   

def prettyPrintQueryReport(query):
    if query.success:
        return f"{green('Success:')} {query.result}"
    elif not query.success:
        return f"{red('Error:')} {query.result}"
    
def prettyPrintQueryRaw(query):
    if query.success:
        return f"{blue('Original query results')}:\n{query.raw}"
    
def prettyPrintQuery(query):
    return f"{prettyPrintQueryReport(query)}\n\n{prettyPrintQueryRaw(query)}\n"

def prettyPrintQueries(queries):
    return [prettyPrintQueryShort(query) for query in queries]

def prettyKey(key):
    key = f"[@{key}]"
    return f"{blue(key)}"

def prettyYear(year):
    year = removeBraces(year)
    return yellow(year)

def prettyAuthor(authors):
    authors = removeBraces(authors)
    authors = authors.split(" and ")
    author = authors[0].split(", ")
    if len(author) > 1:
        author = f"{author[0]}, {author[1][:1]}."
    else:
        author = author[0]

    if len(authors) > 1:
        author = f"{author} et al."

    return blue(author)

def prettyTitle(title):
    title = removeBraces(title)
    return green(title)

def prettyPrintBlock(block):
    return f"{green('Markdown key:')}\n{prettyKey(block.key)}\n\n{green('Current citation:')}\n{block.raw}"

def prettyPrintBlockShort(block):
    elements = []
    try:
        elements.append(prettyAuthor(block.get('author').value))
    except: pass
    try:
        elements.append(prettyYear(block.get('year').value))
    except: pass
    try:
        elements.append(prettyTitle(block.get('title').value))
    except: pass

    return ', '.join(elements) if elements else 'No author, title, or year available.'
    
def prettyPrintBlocks(blocks):
    return [prettyPrintBlockShort(block) for block in blocks]
