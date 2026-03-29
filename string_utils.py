from typing import Set

def reverse(s: str) -> str:
    """
    Reverse the input string.
    
    Args:
        s (str): The string to reverse.
    
    Returns:
        str: The reversed string.
    
    Raises:
        TypeError: If input is not a string.
    """
    if not isinstance(s, str):
        raise TypeError("Input must be a string")
    return s[::-1]

def capitalize_words(s: str) -> str:
    """
    Capitalize the first letter of each word in the string.
    
    Args:
        s (str): The input string.
    
    Returns:
        str: String with each word capitalized.
    
    Raises:
        TypeError: If input is not a string.
    """
    if not isinstance(s, str):
        raise TypeError("Input must be a string")
    return ' '.join(word.capitalize() for word in s.split())

def count_vowels(s: str) -> int:
    """
    Count the number of vowels (a, e, i, o, u, y) in the string, case-insensitive.
    
    Args:
        s (str): The input string.
    
    Returns:
        int: Number of vowels.
    
    Raises:
        TypeError: If input is not a string.
    """
    if not isinstance(s, str):
        raise TypeError("Input must be a string")
    vowels: Set[str] = {'a', 'e', 'i', 'o', 'u', 'y'}
    return sum(1 for c in s.lower() if c in vowels)