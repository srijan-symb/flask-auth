import re


def is_valid_email(email):
    regex = r"^\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4}\b"
    return re.match(regex, email)


def validate_signup_data(data):
    if "name" not in data or not data["name"].strip():
        return False, "Name cannot be left blank"
    if "email" not in data or not data["email"].strip():
        return False, "Email cannot be left blank"
    if not is_valid_email(data["email"]):
        return False, "Email is not valid"
    if "password" not in data or not data["password"]:
        return False, "Password cannot be left blank"
    return True, ""


def validate_login_data(data):
    if "email" not in data or not data["email"].strip():
        return False, "Email cannot be left blank"
    if not is_valid_email(data["email"]):
        return False, "Email is not valid"
    if "password" not in data or not data["password"]:
        return False, "Password cannot be left blank"
    return True, ""


def validate_contact_data(data):
    if "name" not in data or not data["name"].strip():
        return False, "Name is required"
    if "phone" not in data or not data["phone"].strip():
        return False, "Phone is required"
    if "email" in data and data["email"]:
        if not is_valid_email(data["email"]):
            return False, "Email is not valid"
    return True, ""
