"""Long task: word statistics whose definitions change over five rounds."""

R1 = '''
import re
from collections import Counter


def words(text):
    return re.findall(r"[a-z]+", text.lower())


def top_words(text, n):
    c = Counter(words(text))
    return sorted(c.items(), key=lambda kv: (-kv[1], kv[0]))[:n]
'''

R2 = '''
import re
from collections import Counter


def words(text, stop=()):
    stop = {s.lower() for s in stop}
    return [w for w in re.findall(r"[a-z]+(?:'[a-z]+)*", text.lower()) if w not in stop]


def top_words(text, n, stop=()):
    c = Counter(words(text, stop))
    return sorted(c.items(), key=lambda kv: (-kv[1], kv[0]))[:n]
'''

R3 = R2 + '''

def top_ngrams(text, n, k, stop=()):
    ws = words(text, stop)
    c = Counter(" ".join(ws[i:i + k]) for i in range(len(ws) - k + 1))
    return sorted(c.items(), key=lambda kv: (-kv[1], kv[0]))[:n]
'''

R4 = '''
import re
from collections import Counter


def words(text, stop=()):
    stop = {s.lower() for s in stop}
    return [w for w in re.findall(r"[a-z]+(?:'[a-z]+)*", text.lower()) if w not in stop]


def _top(items, n):
    c = Counter(items)
    first = {}
    for i, x in enumerate(items):
        first.setdefault(x, i)
    return sorted(c.items(), key=lambda kv: (-kv[1], first[kv[0]]))[:n]


def top_words(text, n, stop=()):
    return _top(words(text, stop), n)


def top_ngrams(text, n, k, stop=()):
    ws = words(text, stop)
    return _top([" ".join(ws[i:i + k]) for i in range(len(ws) - k + 1)], n)
'''

R5 = R4.replace('''def words(text, stop=()):
    stop = {s.lower() for s in stop}
    return [w for w in re.findall(r"[a-z]+(?:'[a-z]+)*", text.lower()) if w not in stop]''', '''def _split(text):
    out, cur = [], ""
    for i, ch in enumerate(text):
        if ch.isalpha():
            cur += ch
        elif ch == "'" and cur and i + 1 < len(text) and text[i + 1].isalpha():
            cur += ch
        else:
            if cur:
                out.append(cur)
            cur = ""
    if cur:
        out.append(cur)
    return [w.casefold() for w in out]


def words(text, stop=()):
    stop = {s.casefold() for s in stop}
    return [w for w in _split(text) if w not in stop]''')


def t1_counts_and_order(m):
    assert m.top_words("The cat and the hat. THE end, cat!", 3) == [("the", 3), ("cat", 2), ("and", 1)]


def t1_ties_alphabetical(m):
    assert m.top_words("b a c b a c", 2) == [("a", 2), ("b", 2)]


def t1_only_letters(m):
    assert m.top_words("x1y 2 z_z", 5) == [("z", 2), ("x", 1), ("y", 1)]


def t2_stopwords(m):
    assert m.top_words("The cat and the hat", 2, stop=("THE", "and")) == [("cat", 1), ("hat", 1)]


def t2_inner_apostrophes(m):
    text = "it's it's it's it's rock'n'roll rock'n'roll rock'n'roll don't don't 'quoted'"
    assert m.top_words(text, 4) == [("it's", 4), ("rock'n'roll", 3), ("don't", 2), ("quoted", 1)]


def t3_ngrams(m):
    assert m.top_ngrams("a b a b a", 2, 2) == [("a b", 2), ("b a", 2)]
    assert m.top_ngrams("one two", 5, 3) == []


def t3_ngrams_after_stopwords(m):
    assert m.top_ngrams("the red the red the red fox", 1, 2, stop=("the",)) == [("red red", 2)]


def t4_ties_by_first_appearance(m):
    assert m.top_words("b a c b a c", 2) == [("b", 2), ("a", 2)]
    assert m.top_ngrams("z y x w", 2, 2) == [("z y", 1), ("y x", 1)]


def t5_unicode_letters(m):
    assert m.top_words("Café café CAFÉ naïve", 2) == [("café", 3), ("naïve", 1)]
    assert m.top_words("Straße STRASSE", 1) == [("strasse", 2)]


def t5_digits_still_split(m):
    assert m.top_words("über2über", 1) == [("über", 2)]


S1 = ('Write a Python module with `top_words(text: str, n: int) -> list[tuple[str, int]]`. Words are maximal runs '
      'of the letters a-z, case-insensitive (lower-case them). Return the n most frequent words with their counts, '
      'most frequent first; ties in alphabetical order.')
S2 = ('Add `stop=()` to `top_words`: a collection of stop words (case-insensitive) to leave out. Also, an apostrophe '
      "between two letters is part of the word (\"don't\", \"rock'n'roll\"); other apostrophes are not.")
S3 = ('Add `top_ngrams(text, n, k, stop=())`: the n most frequent sequences of k consecutive words, joined by single '
      'spaces, counted over the word list after stop words are removed; same order rules as `top_words`. If there are '
      'fewer than k words, return [].')
S4 = ('Change: ties (in both functions) are now broken by first appearance in the text, earliest first, instead of '
      'alphabetically.')
S5 = ('Change: letters are now any Unicode letters (as `str.isalpha`), not just a-z, and case is folded with '
      '`str.casefold` (so "Straße" and "STRASSE" are the same word, "strasse"). The apostrophe rule is unchanged; '
      'digits and other characters still separate words.')

ROUNDS = [
    {"spec": S1, "ref": R1, "tests": {"t1_counts_and_order": t1_counts_and_order, "t1_ties_alphabetical": t1_ties_alphabetical,
                                     "t1_only_letters": t1_only_letters}},
    {"spec": S2, "ref": R2, "tests": {"t2_stopwords": t2_stopwords, "t2_inner_apostrophes": t2_inner_apostrophes}},
    {"spec": S3, "ref": R3, "tests": {"t3_ngrams": t3_ngrams, "t3_ngrams_after_stopwords": t3_ngrams_after_stopwords}},
    {"spec": S4, "ref": R4, "tests": {"t4_ties_by_first_appearance": t4_ties_by_first_appearance},
     "retires": ["t1_ties_alphabetical"]},
    {"spec": S5, "ref": R5, "tests": {"t5_unicode_letters": t5_unicode_letters, "t5_digits_still_split": t5_digits_still_split}},
]
