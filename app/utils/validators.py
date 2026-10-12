from datetime import date

VALID_STATUSES = {"pending", "in_progress", "completed"}
VALID_PRIORITIES = {"low", "medium", "high"}

def validate_registration(data):
    errors = {}
    if not isinstance(data, dict):
        return {"request": ["JSON body is required."]}
    username = str(data.get("username", "")).strip()
    email = str(data.get("email", "")).strip()
    password = str(data.get("password", ""))

    if len(username) < 3:
        errors["username"] = ["Username must be at least 3 characters."]
    if "@" not in email or "." not in email:
        errors["email"] = ["Enter a valid email address."]
    if len(password) < 6:
        errors["password"] = ["Password must be at least 6 characters."]
    return errors

def validate_task_data(data, update=False):
    errors = {}
    if not isinstance(data, dict):
        return {"request": ["JSON body is required."]}

    if not update and not str(data.get("title", "")).strip():
        errors["title"] = ["Title is required."]
    if "title" in data and len(str(data["title"]).strip()) < 3:
        errors["title"] = ["Title must be at least 3 characters."]
    if "status" in data and data["status"] not in VALID_STATUSES:
        errors["status"] = ["Status must be one of: pending, in_progress, completed."]
    if "priority" in data and data["priority"] not in VALID_PRIORITIES:
        errors["priority"] = ["Priority must be one of: low, medium, high."]
    if "due_date" in data and data["due_date"]:
        try:
            date.fromisoformat(data["due_date"])
        except (ValueError, TypeError):
            errors["due_date"] = ["Due date must use YYYY-MM-DD format."]
    return errors
