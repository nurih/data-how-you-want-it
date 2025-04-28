from datetime import date, datetime
import re

""" Regex to match illegal characters in MongoDB field names.
    See: https://www.mongodb.com/docs/manual/reference/limits/#mongodb-limit-Restrictions-on-Field-Names
    Field names cannot contain the null character.
    The server permits storage of field names that contain dots (.) and dollar signs ($). But drivers might not support this.
    * Behavior:
      - No whitespace
      - No punctuation
    """
SAFE_FIELD_RE = re.compile("([^a-zA-Z0-9])")

def date_to_datetime(day: date) -> datetime:
    """Convert a date to a datetime."""
    return datetime.combine(day, datetime.min.time())


def safe_file_name(raw: str, lower=False) -> str:
    """Returns input as legal string for field naming in MongoDB."""
    processed = SAFE_FIELD_RE.sub("_", raw)
    return processed.lower() if lower else processed
