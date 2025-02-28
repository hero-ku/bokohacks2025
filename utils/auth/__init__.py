NON_SPECIAL_CHARACTERS = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"

def verify_password(password: str) -> bool:
    """Verifies the password against the criteria."""
    return any([
        len(password) >= 8,
        any(char.isdigit() for char in password),
        any(char.isupper() for char in password),
        any(char not in NON_SPECIAL_CHARACTERS for char in password)
    ])