"""Exceptions that map to friendly CLI error messages."""

from __future__ import annotations


class AistrapError(Exception):
    """Base class for errors that should be shown to the user, not traced."""


AiProjectStarterError = AistrapError


class TemplateNotFoundError(AistrapError):
    """Raised when the requested template does not exist."""


class TargetDirectoryError(AistrapError):
    """Raised when the destination directory cannot be used."""
