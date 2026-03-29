"""Input validation utilities for email, URL, and phone number formats.

All validators are pure functions using only the Python standard library.
They accept a string and return ``True``/``False``, or optionally a
:class:`ValidationResult` with an explanation on failure.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Union
from urllib.parse import urlparse


# ── Result type ──────────────────────────────────────────────────────────


@dataclass(frozen=True, slots=True)
class ValidationResult:
    """Carries the outcome of a validation check.

    Truthy when valid, falsy when not — so it works as a drop-in
    replacement for a plain ``bool`` in ``if`` statements.

    >>> r = ValidationResult(valid=False, reason="bad format")
    >>> bool(r)
    False
    >>> r.reason
    'bad format'
    """

    valid: bool
    reason: str = ""

    def __bool__(self) -> bool:
        return self.valid


# ── Constants ────────────────────────────────────────────────────────────

# RFC 5322 simplified — intentionally strict on common edge-cases:
#   - No consecutive dots in local part
#   - Domain must have at least one dot with 2+ char TLD
#   - Max 254 chars total (RFC 5321)
_EMAIL_LOCAL = r"[a-zA-Z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-zA-Z0-9!#$%&'*+/=?^_`{|}~-]+)*"
_EMAIL_DOMAIN = r"[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*\.[a-zA-Z]{2,}"
_EMAIL_RE = re.compile(rf"^{_EMAIL_LOCAL}@{_EMAIL_DOMAIN}$")

_PHONE_DIGITS_RE = re.compile(r"^\+?\d{7,15}$")

_ALLOWED_URL_SCHEMES = frozenset({"http", "https"})


# ── Validators ───────────────────────────────────────────────────────────


def validate_email(
    s: Union[str, object],
    *,
    detailed: bool = False,
) -> Union[bool, ValidationResult]:
    """Validate an email address.

    Args:
        s: The string to validate.
        detailed: If ``True``, return a :class:`ValidationResult` instead
                  of a plain bool.

    Returns:
        ``True`` / ``False``, or a :class:`ValidationResult` when
        *detailed* is set.

    >>> validate_email("user@example.com")
    True
    >>> validate_email("not-an-email")
    False
    >>> validate_email("a" * 255 + "@x.com")
    False
    >>> validate_email("user@example.com", detailed=True)
    ValidationResult(valid=True, reason='')
    """
    ok, reason = _check_email(s)
    if detailed:
        return ValidationResult(valid=ok, reason=reason)
    return ok


def validate_url(
    s: Union[str, object],
    *,
    allowed_schemes: frozenset[str] | None = None,
    detailed: bool = False,
) -> Union[bool, ValidationResult]:
    """Validate a URL (http/https by default).

    Args:
        s: The string to validate.
        allowed_schemes: Override the accepted schemes (default http/https).
        detailed: If ``True``, return a :class:`ValidationResult`.

    Returns:
        ``True`` / ``False``, or a :class:`ValidationResult`.

    >>> validate_url("https://example.com/path?q=1")
    True
    >>> validate_url("ftp://files.example.com")
    False
    >>> validate_url("ftp://x.com", allowed_schemes=frozenset({"ftp"}))
    True
    >>> validate_url("not a url")
    False
    """
    ok, reason = _check_url(s, allowed_schemes or _ALLOWED_URL_SCHEMES)
    if detailed:
        return ValidationResult(valid=ok, reason=reason)
    return ok


def validate_phone(
    s: Union[str, object],
    *,
    min_digits: int = 7,
    max_digits: int = 15,
    detailed: bool = False,
) -> Union[bool, ValidationResult]:
    """Validate a phone number (E.164-ish: optional ``+``, 7–15 digits).

    Non-digit characters (spaces, dashes, dots, parens) are stripped
    before validation.

    Args:
        s: The string to validate.
        min_digits: Minimum digit count (default 7).
        max_digits: Maximum digit count (default 15, per ITU-T E.164).
        detailed: If ``True``, return a :class:`ValidationResult`.

    Returns:
        ``True`` / ``False``, or a :class:`ValidationResult`.

    >>> validate_phone("+33 6 12 34 56 78")
    True
    >>> validate_phone("(555) 123-4567")
    True
    >>> validate_phone("123")
    False
    >>> validate_phone("+33612345678", detailed=True)
    ValidationResult(valid=True, reason='')
    """
    ok, reason = _check_phone(s, min_digits, max_digits)
    if detailed:
        return ValidationResult(valid=ok, reason=reason)
    return ok


# ── Internal checks ──────────────────────────────────────────────────────


def _check_email(s: object) -> tuple[bool, str]:
    if not isinstance(s, str):
        return False, f"Expected str, got {type(s).__name__}"
    s = s.strip()
    if not s:
        return False, "Empty string"
    if len(s) > 254:
        return False, f"Too long ({len(s)} chars, max 254)"
    if not _EMAIL_RE.match(s):
        return False, "Does not match email pattern"
    return True, ""


def _check_url(s: object, allowed_schemes: frozenset[str]) -> tuple[bool, str]:
    if not isinstance(s, str):
        return False, f"Expected str, got {type(s).__name__}"
    s = s.strip()
    if not s:
        return False, "Empty string"
    if " " in s:
        return False, "URL contains spaces"
    try:
        parsed = urlparse(s)
    except ValueError as exc:
        return False, f"Parse error: {exc}"
    if parsed.scheme not in allowed_schemes:
        return False, f"Scheme '{parsed.scheme}' not in {sorted(allowed_schemes)}"
    if not parsed.netloc:
        return False, "Missing netloc (domain)"
    return True, ""


def _check_phone(s: object, min_digits: int, max_digits: int) -> tuple[bool, str]:
    if not isinstance(s, str):
        return False, f"Expected str, got {type(s).__name__}"
    # Strip common formatting characters
    cleaned = re.sub(r"[\s()\-.\u2010\u2011\u2012\u2013\u2014/]", "", s.strip())
    if not cleaned:
        return False, "Empty after cleaning"
    pattern = re.compile(rf"^\+?\d{{{min_digits},{max_digits}}}$")
    if not pattern.match(cleaned):
        digit_count = sum(c.isdigit() for c in cleaned)
        if digit_count < min_digits:
            return False, f"Too few digits ({digit_count}, min {min_digits})"
        if digit_count > max_digits:
            return False, f"Too many digits ({digit_count}, max {max_digits})"
        return False, "Contains invalid characters"
    return True, ""


# ── CLI demo ─────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("── Email ──")
    for addr in ["user@example.com", "a.b+tag@sub.domain.co", "bad@@email", "", None]:
        r = validate_email(addr, detailed=True)
        print(f"  {addr!r:30s} → {r.valid}  {r.reason}")

    print("\n── URL ──")
    for url in ["https://example.com/p?q=1", "ftp://x.com", "not a url", "", 42]:
        r = validate_url(url, detailed=True)
        print(f"  {url!r:30s} → {r.valid}  {r.reason}")

    print("\n── Phone ──")
    for phone in ["+33 6 12 34 56 78", "(555) 123-4567", "123", "+1-800-FLOWERS", ""]:
        r = validate_phone(phone, detailed=True)
        print(f"  {phone!r:30s} → {r.valid}  {r.reason}")
