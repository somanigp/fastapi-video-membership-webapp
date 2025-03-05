from email_validator import validate_email, EmailNotValidError
# NOTE Logic to validate if user emails are valid, thus validator or sanitizer.


def check_email_validity(email):
    msg = ""
    valid = False
    # normalized_email = None  # Ensures no invalid email is returned
    try:
        result = validate_email(email, check_deliverability=True)  # Enable domain check. If validation fails, then func will go to exception block from here.
        # normalized_email = valid.normalized  # Get cleaned email
        email = result.normalized  # Normalized email if valid, otherwise the input email.
        # return valid.normalized  # Returns the normalized email (lowercased, trimmed, etc.)
        valid = True
    except EmailNotValidError as e:
        # return f"Invalid email: {e}"
        msg = str(e)
    return valid, msg, email  # Tuple

