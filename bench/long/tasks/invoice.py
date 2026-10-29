"""Long task: invoice totals whose money rules change over five rounds."""

R1 = '''
from decimal import Decimal, ROUND_HALF_UP


def total(lines):
    s = sum((Decimal(q) * Decimal(p) for _, q, p in lines), Decimal(0))
    return str(s.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))
'''

R2 = '''
from decimal import Decimal, ROUND_HALF_UP


def total(lines, tax_rate="0"):
    s = sum((Decimal(q) * Decimal(p) for _, q, p in lines), Decimal(0))
    s = s * (1 + Decimal(tax_rate))
    return str(s.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))
'''

R3 = '''
from decimal import Decimal, ROUND_HALF_UP


def _line(line):
    q, p = Decimal(line[1]), Decimal(line[2])
    d = Decimal(line[3]) if len(line) > 3 else Decimal(0)
    return q * p * (1 - d / 100)


def total(lines, tax_rate="0"):
    s = sum((_line(l) for l in lines), Decimal(0))
    s = s * (1 + Decimal(tax_rate))
    return str(s.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))
'''

R4 = '''
from decimal import Decimal, ROUND_HALF_UP

ROUNDING = ROUND_HALF_UP
CENT = Decimal("0.01")


def _line(line):
    q, p = Decimal(line[1]), Decimal(line[2])
    d = Decimal(line[3]) if len(line) > 3 else Decimal(0)
    return (q * p * (1 - d / 100)).quantize(CENT, rounding=ROUNDING)


def total(lines, tax_rate="0"):
    sub = sum((_line(l) for l in lines), Decimal(0))
    tax = (sub * Decimal(tax_rate)).quantize(CENT, rounding=ROUNDING)
    return str(sub + tax)
'''

R5 = R4.replace("ROUND_HALF_UP", "ROUND_HALF_EVEN")


def t1_sum(m):
    assert m.total([("a", 2, "1.50"), ("b", 1, "0.25")]) == "3.25"
    assert m.total([]) == "0.00"


def t1_rounds_half_up_at_the_end(m):
    assert m.total([("a", 1, "0.005")]) == "0.01"
    assert m.total([("a", 3, "0.335")]) == "1.01"  # 1.005 -> 1.01


def t1_exact_decimal(m):
    assert m.total([("a", 10, "0.1")] * 3) == "3.00"


def t2_tax(m):
    assert m.total([("a", 1, "100")], tax_rate="0.1") == "110.00"
    assert m.total([("a", 1, "100")]) == "100.00"


def t2_tax_rounding(m):
    assert m.total([("a", 1, "0.05"), ("b", 1, "0.05")], tax_rate="0.15") == "0.12"  # 0.115 -> 0.12


def t3_discount(m):
    assert m.total([("a", 2, "10", "25"), ("b", 1, "5")]) == "20.00"
    assert m.total([("a", 1, "200", "12.5")], tax_rate="0.1") == "192.50"


def t3_discount_then_one_rounding(m):
    assert m.total([("a", 1, "0.10", "5"), ("b", 1, "0.10", "5")]) == "0.19"  # 0.095 + 0.095 = 0.19


def t4_round_each_line(m):
    assert m.total([("a", 1, "0.10", "5"), ("b", 1, "0.10", "5")]) == "0.20"  # 0.10 + 0.10
    assert m.total([("a", 1, "0.004"), ("b", 1, "0.004")]) == "0.00"  # not 0.008 -> 0.01


def t4_tax_on_rounded_sum(m):
    assert m.total([("a", 1, "0.05"), ("b", 1, "0.05")], tax_rate="0.15") == "0.12"  # 0.10 + 0.015 -> 0.02
    assert m.total([("a", 1, "1.004")], tax_rate="0.5") == "1.50"  # 1.00 + 0.50, not 1.506 -> 1.51


def t5_bankers_rounding(m):
    assert m.total([("a", 1, "0.005")]) == "0.00"
    assert m.total([("a", 1, "0.015")]) == "0.02"
    assert m.total([("a", 3, "0.335")]) == "1.00"  # 1.005 -> 1.00


def t5_bankers_tax(m):
    assert m.total([("a", 1, "0.25")], tax_rate="0.1") == "0.27"  # tax 0.025 -> 0.02


S1 = ('Write a Python module with `total(lines) -> str`. Each line is a tuple (description: str, quantity: int, '
      'unit_price: str), the price a decimal string such as "1.50". Return the sum of quantity times unit price as a '
      'string with exactly two decimals, e.g. "3.25". Use exact decimal arithmetic (no floats) and round once, at the '
      'end, to cents, with halves rounded up (0.005 becomes 0.01).')
S2 = ('Add tax: `total(lines, tax_rate: str = "0")`. The result is the sum times (1 + tax_rate), rounded once at the '
      'end as before.')
S3 = ('Add discounts: a line may have a fourth element, a discount percent as a decimal string (e.g. "12.5"), '
      'applied to that line\'s amount before tax. Lines without it have no discount. Still round once at the end.')
S4 = ('Change the rounding rule: round each line\'s (discounted) amount to cents first; the subtotal is the sum of '
      'the rounded lines; tax is the subtotal times the rate, rounded to cents separately; the result is subtotal plus '
      'tax. Halves still round up.')
S5 = ('Change: use banker\'s rounding (round half to even) everywhere instead of rounding halves up: 0.005 becomes '
      '0.00, 0.015 becomes 0.02.')

ROUNDS = [
    {"spec": S1, "ref": R1, "tests": {"t1_sum": t1_sum, "t1_rounds_half_up_at_the_end": t1_rounds_half_up_at_the_end,
                                     "t1_exact_decimal": t1_exact_decimal}},
    {"spec": S2, "ref": R2, "tests": {"t2_tax": t2_tax, "t2_tax_rounding": t2_tax_rounding}},
    {"spec": S3, "ref": R3, "tests": {"t3_discount": t3_discount,
                                     "t3_discount_then_one_rounding": t3_discount_then_one_rounding}},
    {"spec": S4, "ref": R4, "tests": {"t4_round_each_line": t4_round_each_line, "t4_tax_on_rounded_sum": t4_tax_on_rounded_sum},
     "retires": ["t3_discount_then_one_rounding"]},
    {"spec": S5, "ref": R5, "tests": {"t5_bankers_rounding": t5_bankers_rounding, "t5_bankers_tax": t5_bankers_tax},
     "retires": ["t1_rounds_half_up_at_the_end"]},
]
