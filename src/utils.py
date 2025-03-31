IGNORE_CHARS = [",", "'", "\"", "."]


def standarize_name(name: str):
    """
    Standarize a name to match the Billboard naming standards.

    Parameters:
        - name: Name to standarize
    """
    name = name.lower()
    name = name.title()

    return name


def parse_name_for_request(name: str):
    """
    Parse a name to match the Billboard url request.

    Parameters:
        - name: Name to parse
    """
    name = name.lower()

    for char in IGNORE_CHARS:
        name = name.replace(char, "")

    name = name.replace(" ", "-")

    return name
