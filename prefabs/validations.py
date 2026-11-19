"""Validation rule sets. Each check returns an error message or None."""

import re

def rules():
    """Returns the rule sets, grouped by name (e.g. 'name')."""
    return {
        "name" : {
            "empty": [lambda x: "Characters can't have an empty name. Come on, don't be shy!" if not x else None],
            "length": [lambda x: "Too short! Your name needs at least 3 letters." if len(x) < 3 else None],
            "letters": [lambda x: "Names can only contain letters and spaces. No funny symbols, please!" if not re.match("^[a-zA-Z ]+$", x) else None],
        }
    }
