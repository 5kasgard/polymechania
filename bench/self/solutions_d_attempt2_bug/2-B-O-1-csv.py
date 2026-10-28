# NOTE: The specification body was not supplied; only the name 'csv' and the
# single letter 'r' were given. The module below implements a best-guess
# interpretation (a minimal CSV line parser with the standard library) and
# should be checked against the full specification when it arrives.
import csv as _csv
import io as _io


def csv(text):
    """Parse CSV text into a list of rows, each row a list of string fields."""
    if isinstance(text, bytes):
        text = text.decode("utf-8")
    return [list(row) for row in _csv.reader(_io.StringIO(text))]
