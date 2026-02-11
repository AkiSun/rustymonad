"""Error types for rustymonad.

This module defines the base error class and all specific error types
used throughout the rustymonad library.
"""


class RustyMonadError(Exception):
    """Base exception class for rustymonad library.

    All custom exceptions in rustymonad should inherit from this class.
    This provides a clear hierarchy for error handling and allows users
    to catch all rustymonad-related errors with a single except clause.

    Attributes:
        message: The error message describing what went wrong.
        original_error: The original error that caused this exception (if any).
    """

    def __init__(self, message: str, original_error: Exception | None = None) -> None:
        """Initialize a RustyMonadError.

        Args:
            message: The error message describing what went wrong.
            original_error: The original error that caused this exception (optional).
        """
        super().__init__(message)
        self.message = message
        self.original_error = original_error

    def __str__(self) -> str:
        """Return the error message."""
        return self.message

    def __repr__(self) -> str:
        """Return a detailed string representation of the error."""
        return f"{self.__class__.__name__}(message={self.message!r}, original_error={self.original_error!r})"


class ResultError(RustyMonadError):
    """Base exception for Result-related errors.

    This exception is raised when an operation on a Result type fails,
    such as unwrapping an Err value or expecting an Ok value on an Err.

    Attributes:
        value: The erroneous value that caused the error.
    """

    def __init__(self, message: str, value: object, original_error: Exception | None = None) -> None:
        """Initialize a ResultError.

        Args:
            message: The error message describing what went wrong.
            value: The erroneous value that caused the error.
            original_error: The original error that caused this exception (optional).
        """
        super().__init__(message, original_error)
        self.value = value

    def __repr__(self) -> str:
        """Return a detailed string representation of the error."""
        return f"{self.__class__.__name__}(message={self.message!r}, value={self.value!r})"


class UnwrapError(ResultError):
    """Exception raised when unwrapping an Err value.

    This error occurs when calling unwrap() on an Err instance,
    or when calling unwrap_err() on an Ok instance.
    """

    def __init__(self, message: str, value: object, original_error: Exception | None = None) -> None:
        """Initialize an UnwrapError.

        Args:
            message: The error message describing what went wrong.
            value: The erroneous value that caused the error.
            original_error: The original error that caused this exception (optional).
        """
        super().__init__(message, value, original_error)


class ExpectError(ResultError):
    """Exception raised when expect() or expect_err() fails.

    This error occurs when calling expect() on an Err instance
    or expect_err() on an Ok instance, providing a custom error message.
    """

    def __init__(self, message: str, value: object, original_error: Exception | None = None) -> None:
        """Initialize an ExpectError.

        Args:
            message: The error message describing what went wrong.
            value: The erroneous value that caused the error.
            original_error: The original error that caused this exception (optional).
        """
        super().__init__(message, value, original_error)


class UnwrapUncheckedError(ResultError):
    """Exception raised when calling unwrap_unchecked() on an Err value.

    This is an unsafe operation that should only be used when the caller
    is certain the Result is Ok.
    """

    def __init__(self, value: object, original_error: Exception | None = None) -> None:
        """Initialize an UnwrapUncheckedError.

        Args:
            value: The erroneous value that caused the error.
            original_error: The original error that caused this exception (optional).
        """
        message = "called `Result::unwrap_unchecked()` on an `Err` value"
        super().__init__(message, value, original_error)


class OptionError(RustyMonadError):
    """Base exception for Option-related errors.

    This exception is raised when an operation on an Option type fails,
    such as unwrapping a Nothing value.
    """

    def __init__(self, message: str, original_error: Exception | None = None) -> None:
        """Initialize an OptionError.

        Args:
            message: The error message describing what went wrong.
            original_error: The original error that caused this exception (optional).
        """
        super().__init__(message, original_error)


class UnwrapOptionError(OptionError):
    """Exception raised when unwrapping a Nothing value.

    This error occurs when calling unwrap() on a Nothing instance.
    """

    def __init__(self, original_error: Exception | None = None) -> None:
        """Initialize an UnwrapOptionError.

        Args:
            original_error: The original error that caused this exception (optional).
        """
        message = "called `Option::unwrap()` on a `Nothing` value"
        super().__init__(message, original_error)


class ExpectOptionError(OptionError):
    """Exception raised when expect() fails on a Nothing value.

    This error occurs when calling expect() on a Nothing instance
    with a custom error message.
    """

    def __init__(self, message: str, original_error: Exception | None = None) -> None:
        """Initialize an ExpectOptionError.

        Args:
            message: The error message describing what went wrong.
            original_error: The original error that caused this exception (optional).
        """
        super().__init__(message, original_error)


class DoNotationError(RustyMonadError):
    """Exception raised when do_notation encounters an error.

    This includes errors during evaluation or when an unexpected
    type is encountered in the do block.
    """

    def __init__(self, message: str, original_error: Exception | None = None) -> None:
        """Initialize a DoNotationError.

        Args:
            message: The error message describing what went wrong.
            original_error: The original error that caused this exception (optional).
        """
        super().__init__(message, original_error)
