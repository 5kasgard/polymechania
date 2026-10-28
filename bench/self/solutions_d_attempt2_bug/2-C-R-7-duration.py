# NOTE: the specification body is empty ("r"), so the required behaviour of
# `duration` cannot be determined. This is a best-effort placeholder that
# returns a plain duration (end minus start) and should be replaced once the
# real specification is supplied.


def duration(start, end):
    return end - start


if __name__ == '__main__':
    print(duration(3, 10))
    print(duration(10, 3))
    print(duration(0, 0))
