# NOTE: The specification for 'regex' is incomplete. The work order contains only the single character "r" and gives no function signature, required behaviour, or examples. This is a best-effort placeholder implementing the most literal reading: a function named `regex` that takes a pattern string and a text string and returns whether the pattern matches the text, using the standard library `re` module.
import re


def regex(pattern, text):
    return re.fullmatch(pattern, text) is not None
