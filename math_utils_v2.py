# math_utils_v2.py
# Module providing basic arithmetic operations with documentation.


def add(a: float, b: float) -> float:
    """
    Add two numbers.

    Args:
        a (float): First number.
        b (float): Second number.

    Returns:
        float: Sum of a and b.

    Example:
        >>> add(2.0, 3.0)
        5.0
    """
    return a + b


def subtract(a: float, b: float) -> float:
    """
    Subtract b from a.

    Args:
        a (float): First number.
        b (float): Second number.

    Returns:
        float: Difference of a and b.

    Example:
        >>> subtract(5.0, 3.0)
        2.0
    """
    return a - b


def multiply(a: float, b: float) -> float:
    """
    Multiply two numbers.

    Args:
        a (float): First number.
        b (float): Second number.

    Returns:
        float: Product of a and b.

    Example:
        >>> multiply(4.0, 3.0)
        12.0
    """
    return a * b


def divide(a: float, b: float) -> float:
    """
    Divide a by b.

    Args:
        a (float): Dividend.
        b (float): Divisor.

    Returns:
        float: Quotient of a divided by b.

    Raises:
        ValueError: If b is zero.

    Example:
        >>> divide(10.0, 2.0)
        5.0
    """
    if b == 0:
        raise ValueError("Division by zero is not allowed.")
    return a / b
