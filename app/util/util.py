import re
import uuid

def get_uuid():
    """
    Returns a v4 UUID as string without dashes in the middle.
    """
    return re.sub(
        "-",
        "",
        str(uuid.uuid4())
    )
