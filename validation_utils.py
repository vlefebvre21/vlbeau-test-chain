import re
from urllib.parse import urlparse

def validate_email(s):
    """
    Validate an email address using regex.
    """
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, s.strip()))

def validate_url(s):
    """
    Validate a URL using urllib.parse.
    Returns True if it has http/https scheme and netloc.
    """
    try:
        result = urlparse(s.strip())
        return all([
            result.scheme in ('http', 'https'),
            result.netloc
        ])
    except ValueError:
        return False

def validate_phone(s):
    """
    Validate a phone number.
    Strips non-digits/+ and checks for 7-15 digits, optional leading +.
    """
    cleaned = re.sub(r'[^\d+]', '', s.strip())
    pattern = r'^\+?\d{7,15}$'
    return bool(re.match(pattern, cleaned))

if __name__ == "__main__":
    # Email examples
    print("Email:")
    print(validate_email("test@example.com"))  # True
    print(validate_email("invalid-email"))     # False

    # URL examples
    print("\nURL:")
    print(validate_url("https://example.com")) # True
    print(validate_url("not-a-url"))           # False

    # Phone examples
    print("\nPhone:")
    print(validate_phone("+33612345678"))      # True
    print(validate_phone("123-456-7890"))      # True (after cleaning)
    print(validate_phone("abc"))               # False