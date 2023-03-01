

def anonymize_email(email: str) -> str:
    broken_email = email.split('@')
    return f'{email[0]}***@{broken_email[1]}'