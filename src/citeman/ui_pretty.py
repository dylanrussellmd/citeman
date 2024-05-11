from colors import color
from .processor import Processor
from .utils import removeBraces

def prettyPrintQueryReport(query):
    if query.success:
        return f"{color('Success:', fg='green')} {query.result}"
    elif not query.success:
        return f"{color('Error:', fg='red')} {query.result}"

def prettyPrintQuery(query):
    return f"{query.id} - {prettyPrintQueryReport(query)}"

def prettyPrintQueries(queries):
    return [prettyPrintQuery(query) for query in queries]

def prettyKey(key):
    key = f"[@{key}]"
    return f"{color(key, fg='blue')}"

def prettyYear(year):
    year = removeBraces(year)
    return color(year, fg='yellow')

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

    return color(author, fg='blue')

def prettyTitle(title):
    title = removeBraces(title)
    return color(title, fg='green')

def prettyPrintBlock(block):
    return f"\n{prettyKey(block.key)}\n{block.raw}"

def prettyPrintBlockShort(block):
    elements = []
    try:
        Processor.fieldExists(block, 'author')
        elements.append(prettyAuthor(block.get('author').value))
    except: pass
    try:
        Processor.fieldExists(block, 'year')
        elements.append(prettyYear(block.get('year').value))
    except: pass
    try:
        Processor.fieldExists(block, 'title')
        elements.append(prettyTitle(block.get('title').value))
    except: pass

    return ', '.join(elements) if elements else 'No author, title, or year available.'
    
def prettyPrintBlocks(blocks):
    return [prettyPrintBlockShort(block) for block in blocks]
