# NOTE: The specification body is only the single letter "r", so the required
# behaviour of `duration` cannot be determined. This is a best-effort placeholder
# that accepts an optional argument and returns it unchanged.

def duration(r=None):
    return r


if __name__ == '__main__':
    print(duration())
    print(duration(5))
    print(duration("r"))
