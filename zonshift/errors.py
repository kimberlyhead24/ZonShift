"""Exception types used across ZonShift.

Every error raised on purpose derives from ZonShiftError, so callers can 
catch the whole family with one ''except'' clause.
"""
class ZonShiftError(Exception):
    """Base class for all Zonshift errors."""

class InvalidValueError(ZonShiftError, ValueError):
    """A value is outside its allowed range (for example, humidity of 140%)."""

class UnknownZoneError(ZonShiftError):
    """A zone identifier does not match any known zone."""
