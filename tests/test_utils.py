from citeman.utils import removeBraces, removeAt

def test_removeBraces():
    assert removeBraces("{Hello}") == "Hello"
    assert removeBraces("{{Hello}}") == "{Hello}"
    assert removeBraces("{Hello") == "Hello"
    assert removeBraces("Hello") == "Hello"
    assert removeBraces("Hello}") == "Hello"
    assert removeBraces("Hel{}lo") == "Hel{}lo"

def test_removeAt():
    assert removeAt("@Hello") == "Hello"
    assert removeAt("@@Hello") == "Hello"
    assert removeAt("Hello") == "Hello"
    assert removeAt("@") == ""
    assert removeAt("@@") == ""
    assert removeAt("@@Hello@") == "Hello@"
    assert removeAt("@@Hell@o@@") == "Hell@o@@"