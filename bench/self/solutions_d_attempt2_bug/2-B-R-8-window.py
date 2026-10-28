# NOTE: the specification body was not included in the work order (it only reads "r"),
# so the required behaviour of `window` cannot be verified. The implementation below
# assumes the most common meaning: return the sliding-window (w-length) sums or
# extrema is NOT assumed; instead it returns all contiguous windows of length `size`
# from the input sequence, as a list of lists. Replace this once the specification
# is available.

def window(seq, size):
    items = list(seq)
    if not isinstance(size, int) or size <= 0:
        raise ValueError("size must be a positive integer")
    if size > len(items):
        return []
    return [items[i:i + size] for i in range(len(items) - size + 1)]
