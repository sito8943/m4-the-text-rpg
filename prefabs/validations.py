import re

def rules():
    return {
        "name" : {
            "empty": [lambda x: "Name cannot be empty." if not x else None],
            "length": [lambda x: "Name must be at least 3 characters long." if len(x) < 3 else None],
            "letters": [lambda x: "Name can only contain letters and spaces." if not re.match("^[a-zA-Z ]+$", x) else None],
        }
    }