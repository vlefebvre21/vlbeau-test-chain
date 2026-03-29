"""Arithmetic utility functions with input validation and extended operations."""

from __future__ import annotations

from typing import Union

Numeric = Union[int, float]


def add(a: Numeric, b: Numeric) -> Numeric:
    """Return the sum of *a* and *b*.

    Args:
        a: First operand.
        b: Second operand.

    Returns:
        The arithmetic sum.

    Raises:
        TypeError: If either operand is not a number.

    >>> add(2, 3)
    5
    >>> add(1.5, 2.5)
    4.0
    """
    _validate_numeric(a, b)
    return a + b


def subtract(a: Numeric, b: Numeric) -> Numeric:
    """Return *a* minus *b*.

    >>> subtract(10, 4)
    6
    """
    _validate_numeric(a, b)
    return a - b


def multiply(a: Numeric, b: Numeric) -> Numeric:
    """Return the product of *a* and *b*.

    Args:
        a: First operand.
        b: Second operand.

    Returns:
        The arithmetic product.

    Raises:
        TypeError: If either operand is not a number.

    >>> multiply(4, 5)
    20
    >>> multiply(0.1, 0.2)  # doctest: +ELLIPSIS
    0.020...
    """
    _validate_numeric(a, b)
    return a * b


def divide(a: Numeric, b: Numeric) -> float:
    """Return *a* divided by *b*.

    Args:
        a: Dividend.
        b: Divisor (must not be zero).

    Returns:
        The quotient as a float.

    Raises:
        TypeError: If either operand is not a number.
        ZeroDivisionError: If *b* is zero.

    >>> divide(10, 3)  # doctest: +ELLIPSIS
    3.333...
    """
    _validate_numeric(a, b)
    if b == 0:
        raise ZeroDivisionError("Cannot divide by zero.")
    return a / b


def power(base: Numeric, exponent: Numeric) -> Numeric:
    """Return *base* raised to *exponent*.

    >>> power(2, 10)
    1024
    """
    _validate_numeric(base, exponent)
    return base ** exponent


# ── Internal helpers ─────────────────────────────────────────────────────

def _validate_numeric(*args: object) -> None:
    """Raise :exc:`TypeError` if any argument is not ``int`` or ``float``."""
    for arg in args:
        if not isinstance(arg, (int, float)):
            raise TypeError(
                f"Expected a numeric value (int | float), got {type(arg).__name__!r}."
            )


# ── CLI demo ─────────────────────────────────────────────────────────────

if __name__ == "__main__":
    pairs: list[tuple[str, Numeric]] = [
        ("add(2, 3)", add(2, 3)),
        ("subtract(10, 4)", subtract(10, 4)),
        ("multiply(4, 5)", multiply(4, 5)),
        ("divide(10, 3)", divide(10, 3)),
        ("power(2, 10)", power(2, 10)),
    ]
    for label, result in pairs:
        print(f"{label} = {result}")
