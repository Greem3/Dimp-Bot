

def KeyIn(dictionary: dict, key: str) -> bool|None:
    """
    Return True if the key is in the dictionary, if it is not, return false
    """
    
    try:
        dictionary[key]
        return True
    except:
        return False