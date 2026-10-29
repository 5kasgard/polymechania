"""Long task: an INI-like config parser whose rules change over five rounds."""

R1 = '''
def parse(text):
    out = {}
    for line in text.splitlines():
        if not line.strip():
            continue
        if "=" not in line:
            raise ValueError(line)
        k, v = line.split("=", 1)
        out[k.strip()] = v.strip()
    return out
'''

R2 = '''
def parse(text):
    out = {"": {}}
    sec = ""
    for line in text.splitlines():
        s = line.strip()
        if not s:
            continue
        if s.startswith("[") and s.endswith("]"):
            sec = s[1:-1].strip()
            out.setdefault(sec, {})
            continue
        if "=" not in line:
            raise ValueError(line)
        k, v = line.split("=", 1)
        out[sec][k.strip()] = v.strip()
    return out
'''

R3 = '''
def _strip_comment(v):
    i = v.find(" #")
    return v[:i] if i >= 0 else v


def parse(text):
    out = {"": {}}
    sec = ""
    for line in text.splitlines():
        s = line.strip()
        if not s or s[0] in "#;":
            continue
        if s.startswith("[") and s.endswith("]"):
            sec = s[1:-1].strip()
            out.setdefault(sec, {})
            continue
        if "=" not in line:
            raise ValueError(line)
        k, v = line.split("=", 1)
        out[sec][k.strip()] = _strip_comment(v).strip()
    return out
'''

R4 = R3.replace("def parse(text):", "def _parse_raw(text):") + '''

import re

_REF = re.compile(r"\\$\\{([^}]*)\\}")


def parse(text):
    raw = _parse_raw(text)
    done = {}

    def value(sec, key, stack):
        if (sec, key) in done:
            return done[(sec, key)]
        if (sec, key) in stack:
            raise ValueError("cycle at " + sec + "." + key)
        if sec not in raw or key not in raw[sec]:
            raise ValueError("undefined " + sec + "." + key)

        def sub(mm):
            ref = mm.group(1)
            if "." in ref:
                s, k = ref.split(".", 1)
            else:
                s, k = sec, ref
            return value(s, k, stack | {(sec, key)})

        v = _REF.sub(sub, raw[sec][key])
        done[(sec, key)] = v
        return v

    return {s: {k: value(s, k, frozenset()) for k in ks} for s, ks in raw.items()}
'''

R5 = R4.replace('''        k, v = line.split("=", 1)
        out[sec][k.strip()] = _strip_comment(v).strip()''', '''        k, v = line.split("=", 1)
        if k.strip() in out[sec]:
            raise ValueError("duplicate " + k.strip())
        out[sec][k.strip()] = _strip_comment(v).strip()''')


def raises(f, *a):
    try:
        f(*a)
    except ValueError:
        return True
    return False


def t1_pairs(m):
    assert m.parse("a = 1\n\n  b=two words  \nc =\n") == {"a": "1", "b": "two words", "c": ""}


def t1_value_may_contain_equals(m):
    assert m.parse("url = http://x/?a=b") == {"url": "http://x/?a=b"}


def t1_bad_line(m):
    assert raises(m.parse, "a = 1\nnot a pair\n")


def t1_later_wins(m):
    assert m.parse("a = 1\na = 2") == {"a": "2"}


def t2_sections(m):
    got = m.parse("top = 0\n[one]\na = 1\n[ two ]\na = 2\n[one]\nb = 3\n")
    assert got == {"": {"top": "0"}, "one": {"a": "1", "b": "3"}, "two": {"a": "2"}}


def t2_empty_and_no_root(m):
    assert m.parse("") == {"": {}}
    assert m.parse("[s]\n") == {"": {}, "s": {}}


def t3_comment_lines(m):
    assert m.parse("# top\n  ; also\n[s]\n# x = 1\na = 1\n") == {"": {}, "s": {"a": "1"}}


def t3_inline_comment(m):
    assert m.parse("a = 1 # one\nb = c#d\nc = x  # y # z") == {"": {"a": "1", "b": "c#d", "c": "x"}}


def t4_interpolation(m):
    got = m.parse("[paths]\nroot = /srv\nlogs = ${root}/logs\n[app]\nout = ${paths.logs}/app.log\n")
    assert got["paths"]["logs"] == "/srv/logs" and got["app"]["out"] == "/srv/logs/app.log"


def t4_chain_and_errors(m):
    assert m.parse("a = 1\nb = ${a}${a}\nc = ${b}-${a}")[""] == {"a": "1", "b": "11", "c": "11-1"}
    assert raises(m.parse, "a = ${missing}")
    assert raises(m.parse, "a = ${b}\nb = ${a}")
    assert raises(m.parse, "a = ${a}")


def t5_duplicates_refused(m):
    assert raises(m.parse, "a = 1\na = 2")
    assert raises(m.parse, "[s]\nk = 1\n[t]\nk = 1\n[s]\nk = 2")


def t5_same_key_other_sections_fine(m):
    assert m.parse("k = 0\n[s]\nk = 1\n[t]\nk = 2")[""] == {"k": "0"}


S1 = ('Write a Python module with `parse(text: str) -> dict[str, str]` for config text made of lines `key = value`. '
      'Strip whitespace around keys and values; the value is everything after the first "=" (it may itself contain '
      '"=", and may be empty). Ignore blank lines. Raise ValueError for any other line without "=". If a key repeats, '
      'the later value wins.')
S2 = ('Change: add sections. A line `[name]` (whitespace inside the brackets is stripped) starts section `name`; '
      'pairs before any section belong to the section "". `parse` now returns dict[str, dict[str, str]]: section name '
      'to its pairs. The "" section is always present, even if empty; a section header with no pairs still appears; '
      'a section may be reopened later and its pairs merge.')
S3 = ('Add comments. A line whose first non-space character is "#" or ";" is ignored. In a value, a space followed '
      'by "#" starts an inline comment that is removed (along with the whitespace before it); a "#" with no space '
      'before it is part of the value.')
S4 = ('Add interpolation. In a value, `${key}` is replaced by the final value of `key` in the same section, and '
      '`${section.key}` by the final value of `key` in `section`. References may chain. Raise ValueError for a '
      'reference to a key that does not exist and for any cycle of references.')
S5 = ('Change: a key repeated within the same section (including across reopened sections) is now an error: raise '
      'ValueError instead of letting the later value win. The same key in different sections is fine.')

ROUNDS = [
    {"spec": S1, "ref": R1, "tests": {"t1_pairs": t1_pairs, "t1_value_may_contain_equals": t1_value_may_contain_equals,
                                     "t1_bad_line": t1_bad_line, "t1_later_wins": t1_later_wins}},
    {"spec": S2, "ref": R2, "tests": {"t2_sections": t2_sections, "t2_empty_and_no_root": t2_empty_and_no_root},
     "retires": ["t1_pairs", "t1_value_may_contain_equals", "t1_later_wins"]},
    {"spec": S3, "ref": R3, "tests": {"t3_comment_lines": t3_comment_lines, "t3_inline_comment": t3_inline_comment}},
    {"spec": S4, "ref": R4, "tests": {"t4_interpolation": t4_interpolation, "t4_chain_and_errors": t4_chain_and_errors}},
    {"spec": S5, "ref": R5, "tests": {"t5_duplicates_refused": t5_duplicates_refused,
                                     "t5_same_key_other_sections_fine": t5_same_key_other_sections_fine}},
]

# Round 2 changes the return shape, so round 1's shape tests retire with it;
# the duplicate-key rule ("later wins") then lives only in the section form:
ROUNDS[1]["tests"]["t2_later_wins_in_section"] = lambda m: _later(m)
ROUNDS[4]["retires"] = ["t2_later_wins_in_section"]


def _later(m):
    assert m.parse("[s]\na = 1\na = 2")["s"] == {"a": "2"}
