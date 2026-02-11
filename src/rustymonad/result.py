"""Result type for error handling.

This module provides the Result type, which is used to represent either
a successful value (Ok) or an error (Err). It is inspired by Rust's Result
type and enables explicit error handling without exceptions.

The Result type is useful for:
- Handling errors without using try/except
- Composing functions that may fail
- Making error conditions explicit in the type system

Example:
    >>> def parse_int(s: str) -> Result[int, str]:
    ...     try:
    ...         return Ok(int(s))
    ...     except ValueError as e:
    ...         return Err(str(e))
    >>> parse_int("42").unwrap()
    42
    >>> parse_int("invalid").unwrap_err()
    'invalid'
"""

from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TypeVar, Callable, Any
import copy
from .monad import Monad
from .errors import (
    RustyMonadError,
    UnwrapError,
    ExpectError,
    UnwrapUncheckedError,
)


TResult = TypeVar("TResult")
UResult = TypeVar("UResult")
EResult = TypeVar("EResult")
FResult = TypeVar("FResult")


class ResultMixin:
    """Mixin class providing common functionality for Result types."""

    @staticmethod
    def _raise_value(value: Any) -> None:
        """Helper method to raise exception from value.

        Args:
            value: The value to raise. If it's an Exception, it's raised directly.

        Raises:
            UnwrapError: Always raised.
        """
        if isinstance(value, Exception):
            raise UnwrapError(str(value), value, original_error=value)
        else:
            raise UnwrapError(str(value), value)

    @staticmethod
    def _format_error_msg(msg: str, value: Any) -> str:
        """Helper method to format error messages.

        Args:
            msg: The base error message.
            value: The error value.

        Returns:
            Formatted error message string.
        """
        return f"{msg}: {value}"

    def _identity_map(self, fn: Callable[[TResult], UResult]) -> Result:
        """Common pattern for methods that return self in Err case.

        Args:
            fn: Ignored for Err variant.

        Returns:
            self (Err).
        """
        return self

    def _apply_fn_if_valid(self, fn: Callable[[TResult], None]) -> "Result":
        """Common pattern for inspect methods.

        Args:
            fn: The function to apply (only for Ok variant).

        Returns:
            self.
        """
        return self


class Result(Monad[TResult | EResult], ABC):
    """Abstract base class for Result type.

    Result represents either a success (Ok) or a failure (Err). This abstract
    class defines the interface that both Ok and Err must implement.

    Use Ok(value) for success and Err(error) for failure.

    Attributes:
        _value: The wrapped value (success value for Ok, error for Err).

    Example:
        >>> Ok(42)
        Result::Ok(42)
        >>> Err("error")
        Result::Err('error')
    """
    __slots__ = ()

    @abstractmethod
    def expect(self, msg: str) -> TResult:
        """Return the Ok value or raise with a custom message.

        Args:
            msg: Error message to use if Err.

        Returns:
            The Ok value.

        Raises:
            ExpectError: If this is Err.
        """
        raise NotImplementedError

    @abstractmethod
    def expect_err(self, msg: str) -> EResult:
        """Return the Err value or raise with a custom message.

        Args:
            msg: Error message to use if Ok.

        Returns:
            The Err value.

        Raises:
            ExpectError: If this is Ok.
        """
        raise NotImplementedError

    @abstractmethod
    def unwrap(self) -> TResult:
        """Return the Ok value.

        Returns:
            The Ok value.

        Raises:
            UnwrapError: If this is Err.
        """
        raise NotImplementedError

    @abstractmethod
    def unwrap_unchecked(self) -> TResult:
        """Return the value directly without any checks.

        This is an "unsafe" operation, only use when sure Result is Ok.

        Returns:
            The Ok value.

        Raises:
            UnwrapUncheckedError: If this is Err.
        """
        raise NotImplementedError

    @abstractmethod
    def unwrap_err(self) -> EResult:
        """Return the Err value.

        Returns:
            The Err value.

        Raises:
            UnwrapError: If this is Ok.
        """
        raise NotImplementedError

    @abstractmethod
    def unwrap_or(self, default: TResult) -> TResult:
        """Return the Ok value or a default if Err.

        Args:
            default: The value to return if Err.

        Returns:
            The Ok value if Ok, otherwise the default.
        """
        raise NotImplementedError

    @abstractmethod
    def unwrap_or_else(self, fn: Callable[[], TResult]) -> TResult:
        """Return the Ok value or compute from a function if Err.

        Args:
            fn: A callable that returns the default value if Err.

        Returns:
            The Ok value if Ok, otherwise fn().
        """
        raise NotImplementedError

    @abstractmethod
    def map_err(self, fn: Callable[[EResult], FResult]) -> Result[TResult, FResult]:
        """Map the Err value to a new error type.

        Args:
            fn: A function to transform the Err value.

        Returns:
            self if Ok, otherwise Err(fn(error)).
        """
        raise NotImplementedError

    @abstractmethod
    def and_then(self, fn: Callable[[TResult], Result[UResult, EResult]]) -> Result[UResult, EResult]:
        """Apply a function that returns Result to the Ok value.

        Args:
            fn: A callable that takes the Ok value and returns Result[UResult, EResult].

        Returns:
            The result of fn if Ok, otherwise self (Err).

        Example:
            >>> Ok(5).and_then(lambda x: Ok(x * 2))
            Result::Ok(10)
        """
        raise NotImplementedError

    @abstractmethod
    def or_else(self, fn: Callable[[EResult], Result[UResult, EResult]]) -> Result[UResult, EResult]:
        """Apply a function that returns Result to the Err value.

        Args:
            fn: A callable that takes the Err value and returns Result[UResult, EResult].

        Returns:
            self if Ok, otherwise the result of fn.
        """
        raise NotImplementedError

    @abstractmethod
    def inspect(self, fn: Callable[[TResult], None]) -> Result[TResult, EResult]:
        """Inspect the Ok value without modifying it.

        Args:
            fn: A callable to invoke with the Ok value (if Ok).

        Returns:
            self.

        Example:
            >>> Ok(42).inspect(print)
            Result::Ok(42)
        """
        raise NotImplementedError

    @abstractmethod
    def inspect_err(self, fn: Callable[[EResult], None]) -> Result[TResult, EResult]:
        """Inspect the Err value without modifying it.

        Args:
            fn: A callable to invoke with the Err value (if Err).

        Returns:
            self.
        """
        raise NotImplementedError

    @abstractmethod
    def is_ok_and(self, fn: Callable[[TResult], bool]) -> bool:
        """Check if Ok and the value satisfies a predicate.

        Args:
            fn: A predicate function to apply to the value.

        Returns:
            True if Ok and fn(value) is True, otherwise False.
        """
        raise NotImplementedError

    @abstractmethod
    def is_err_and(self, fn: Callable[[EResult], bool]) -> bool:
        """Check if Err and the error satisfies a predicate.

        Args:
            fn: A predicate function to apply to the error.

        Returns:
            True if Err and fn(error) is True, otherwise False.
        """
        raise NotImplementedError

    @abstractmethod
    def ok(self) -> Option[TResult]:
        """Convert to Option, mapping Ok to Some.

        Returns:
            Some(value) if Ok, Nothing if Err.
        """
        raise NotImplementedError

    @abstractmethod
    def err(self) -> Option[EResult]:
        """Convert to Option, mapping Err to Some.

        Returns:
            Some(error) if Err, Nothing if Ok.
        """
        raise NotImplementedError

    @abstractmethod
    def map(self, fn: Callable[[TResult], UResult]) -> Monad[UResult]:
        """Apply a function to the Ok value.

        Args:
            fn: A callable that transforms the Ok value.

        Returns:
            Ok(fn(value)) if Ok, otherwise self (Err).
        """
        raise NotImplementedError

    @abstractmethod
    def flatmap(self, fn: Callable[[TResult], Monad[UResult]]) -> Monad[UResult]:
        """Apply a function that returns a Monad to the Ok value.

        Args:
            fn: A callable that takes the value and returns Monad[UResult].

        Returns:
            The result of fn if Ok, otherwise self (Err).
        """
        raise NotImplementedError

    @abstractmethod
    def is_ok(self) -> bool:
        """Check if this is an Ok variant.

        Returns:
            True if Ok, False if Err.
        """
        raise NotImplementedError

    @abstractmethod
    def is_err(self) -> bool:
        """Check if this is an Err variant.

        Returns:
            True if Err, False if Ok.
        """
        raise NotImplementedError

    @abstractmethod
    def __bool__(self) -> bool:
        """Check if the Result is Ok.

        Returns:
            True if Ok, False if Err.
        """
        raise NotImplementedError

    @abstractmethod
    def __eq__(self, other: object) -> bool:
        """Check equality with another Result.

        Args:
            other: The object to compare.

        Returns:
            True if both are Ok with equal values or both are Err with equal errors.
        """
        raise NotImplementedError

    @abstractmethod
    def __hash__(self) -> int:
        """Return a hash value for the Result.

        Returns:
            Hash value based on the wrapped value.
        """
        raise NotImplementedError

    @abstractmethod
    def __rshift__(self, fn: Callable[[TResult], Monad[UResult]]) -> Monad[UResult]:
        """Bind operation using >> operator.

        Args:
            fn: A callable that takes the value and returns Monad[UResult].

        Returns:
            The result of fn if Ok, otherwise self (Err).
        """
        raise NotImplementedError

    @abstractmethod
    def __repr__(self) -> str:
        """Return a string representation of the Result.

        Returns:
            'Result::Ok(value)' or 'Result::Err(error)'.
        """
        raise NotImplementedError

    @staticmethod
    def try_catch(fn: Callable[[TResult], UResult]) -> Callable[[TResult], Result[UResult, str]]:
        """Decorator that wraps a function to catch exceptions as Result.

        Args:
            fn: The function to wrap.

        Returns:
            A wrapper function that returns Ok(result) on success,
            Err(exception_message) on failure.

        Example:
            >>> @Result.try_catch
            ... def may_fail():
            ...     if random.random() > 0.5:
            ...         raise ValueError("oops")
            ...     return "success"
        """
        def _wrapper(*args, **kwargs):
            try:
                return Ok(fn(*args, **kwargs))
            except Exception as e:
                return Err(str(e))

        return _wrapper


class Ok(ResultMixin, Result[TResult, Any]):
    """Result variant that represents a successful value.

    Ok represents the success variant of Result. It contains a value
    indicating successful execution.

    Example:
        >>> Ok(42)
        Result::Ok(42)
        >>> Ok("success")
        Result::Ok('success')
    """
    __slots__ = ()

    def __init__(self, value: TResult) -> None:
        """Initialize Ok with a success value.

        Args:
            value: The success value.
        """
        super().__init__(value)

    def expect(self, msg: str) -> TResult:
        """Return the contained value (Ok always returns the value).

        Args:
            msg: Ignored for Ok.

        Returns:
            The contained value.
        """
        return self._value

    def expect_err(self, msg: str) -> EResult:
        """Raise ExpectError (Ok never has an error value).

        Args:
            msg: The error message.

        Raises:
            ExpectError: Always raised for Ok.
        """
        raise ExpectError(self._format_error_msg(msg, self._value), self._value)

    def unwrap(self) -> TResult:
        """Return the contained value.

        Returns:
            The contained value.
        """
        return self._value

    def unwrap_err(self):
        """Raise UnwrapError (Ok never has an error value).

        Raises:
            UnwrapError: Always raised for Ok.
        """
        self._raise_value(self._value)

    def unwrap_or(self, default: TResult) -> TResult:
        """Return the contained value (ignores the default).

        Args:
            default: Ignored for Ok.

        Returns:
            The contained value.
        """
        return self._value

    def unwrap_or_else(self, fn: Callable[[], TResult]) -> TResult:
        """Return the contained value (ignores the function).

        Args:
            fn: Ignored for Ok.

        Returns:
            The contained value.
        """
        return self._value

    def map_err(self, fn: Callable[[EResult], FResult]) -> Result[TResult, FResult]:
        """Return Ok without calling the function.

        Args:
            fn: Ignored for Ok.

        Returns:
            self.
        """
        return Ok(self._value)

    def unwrap_unchecked(self) -> TResult:
        """Return the value directly without any checks.

        This is an "unsafe" operation, only use when sure Result is Ok.

        Returns:
            The contained value.
        """
        return self._value

    def and_then(self, fn: Callable[[TResult], Result[UResult, EResult]]) -> Result[UResult, EResult]:
        """Apply fn to the contained value and return the result.

        Args:
            fn: A callable that takes the value and returns Result[UResult, EResult].

        Returns:
            The result of fn(value).
        """
        return fn(self._value)

    def or_else(self, fn: Callable[[EResult], Result[UResult, EResult]]) -> Result[Any, EResult]:
        """Return self without calling the function.

        Args:
            fn: Ignored for Ok.

        Returns:
            self.
        """
        return self

    def inspect(self, fn: Callable[[TResult], None]) -> Result[TResult, EResult]:
        """Inspect the contained value.

        Args:
            fn: A callable to invoke with the value.

        Returns:
            self.
        """
        fn(self._value)
        return self

    def inspect_err(self, fn: Callable[[EResult], None]) -> Result[TResult, EResult]:
        """Do nothing (the error function is not called for Ok).

        Args:
            fn: Ignored.

        Returns:
            self.
        """
        return self

    def is_ok_and(self, fn: Callable[[TResult], bool]) -> bool:
        """Check if the value satisfies the predicate.

        Args:
            fn: A predicate function to apply to the value.

        Returns:
            The result of fn(value).
        """
        return fn(self._value)

    def is_err_and(self, fn: Callable[[EResult], bool]) -> bool:
        """Return False (Ok never has an error).

        Args:
            fn: Ignored.

        Returns:
            False.
        """
        return False

    def ok(self) -> Option[TResult]:
        """Convert to Some.

        Returns:
            Some(value).
        """
        return Some(self._value)

    def err(self) -> Option[EResult]:
        """Convert to Nothing (Ok has no error).

        Returns:
            Nothing().
        """
        return Nothing()

    def map(self, fn: Callable[[TResult], UResult]) -> Monad[UResult]:
        """Apply fn to the contained value.

        Args:
            fn: A callable that transforms the value.

        Returns:
            Ok(fn(value)).
        """
        return Ok(fn(self._value))

    def flatmap(self, fn: Callable[[TResult], Monad[UResult]]) -> Monad[UResult]:
        """Apply fn to the contained value.

        Args:
            fn: A callable that takes the value and returns Monad[UResult].

        Returns:
            The result of fn(value).
        """
        return fn(self._value)

    def is_ok(self) -> bool:
        """Check if this is Ok.

        Returns:
            True.
        """
        return True

    def is_err(self) -> bool:
        """Check if this is Err.

        Returns:
            False.
        """
        return False

    def __bool__(self) -> bool:
        """Check if the Result is Ok.

        Returns:
            True.
        """
        return True

    def __eq__(self, other: object) -> bool:
        """Check equality with another Result.

        Args:
            other: The object to compare.

        Returns:
            True if other is Ok with equal value, False otherwise.
        """
        if isinstance(other, Ok):
            return self._value == other._value
        return False

    def __hash__(self) -> int:
        """Return a hash value for the Ok.

        Returns:
            Hash value based on the wrapped value.

        Raises:
            TypeError: If the wrapped value is unhashable
                (e.g., a list or dict). Only hashable types like
                strings, exceptions, and numbers can be used with
                Ok in sets or as dict keys.
        """
        return hash(self._value)

    def __rshift__(self, fn: Callable[[TResult], Monad[UResult]]) -> Monad[UResult]:
        """Apply fn to the contained value and return the result.

        Args:
            fn: A callable that takes the value and returns Monad[UResult].

        Returns:
            The result of fn(value).
        """
        return fn(self._value)

    def __repr__(self) -> str:
        """Return a string representation.

        Returns:
            'Result::Ok(value)'.
        """
        return f"Result::Ok({self._value!r})"

    def __copy__(self) -> "Ok[TResult]":
        """Create a shallow copy of Ok.

        Returns:
            A new Ok with a shallow copy of the wrapped value.
        """
        return Ok(copy.copy(self._value))

    def __deepcopy__(self, memo: dict) -> "Ok[TResult]":
        """Create a deep copy of Ok.

        Args:
            memo: A dictionary for memoization of already copied objects.

        Returns:
            A new Ok with a deep copy of the wrapped value.
        """
        return Ok(copy.deepcopy(self._value, memo))


class Err(ResultMixin, Result[Any, EResult]):
    """Result variant that represents an error.

    Err represents the error variant of Result. It contains an error
    value indicating failed execution.

    Example:
        >>> Err("error message")
        Result::Err('error message')
        >>> Err(ValueError("invalid"))
        Result::Err(ValueError('invalid'))
    """
    __slots__ = ()

    def __init__(self, value: EResult) -> None:
        """Initialize Err with an error value.

        Args:
            value: The error value.
        """
        super().__init__(value)

    def expect(self, msg: str):
        """Raise ExpectError with the given message.

        Args:
            msg: The base error message.

        Raises:
            ExpectError: Always raised for Err.
        """
        raise ExpectError(self._format_error_msg(msg, self._value), self._value)

    def expect_err(self, msg: str) -> EResult:
        """Return the contained error value.

        Args:
            msg: Ignored for Err.

        Returns:
            The contained error value.
        """
        return self._value

    def unwrap(self):
        """Raise UnwrapError.

        Raises:
            UnwrapError: Always raised for Err.
        """
        self._raise_value(self._value)

    def unwrap_err(self) -> EResult:
        """Return the contained error value.

        Returns:
            The contained error value.
        """
        return self._value

    def unwrap_or(self, default: TResult) -> TResult:
        """Return the default value.

        Args:
            default: The value to return.

        Returns:
            The default value.
        """
        return default

    def unwrap_or_else(self, fn: Callable[[], TResult]) -> TResult:
        """Call the function and return its result.

        Args:
            fn: A callable that returns the default value.

        Returns:
            The result of fn().
        """
        return fn()

    def map_err(self, fn: Callable[[EResult], FResult]) -> Result[TResult, FResult]:
        """Apply fn to the error value.

        Args:
            fn: A function to transform the error.

        Returns:
            Err(fn(error)).
        """
        return Err(fn(self._value))

    def unwrap_unchecked(self) -> TResult:
        """Raise UnwrapUncheckedError (Err is never safe to unwrap).

        Raises:
            UnwrapUncheckedError: Always raised for Err.
        """
        raise UnwrapUncheckedError(self._value)

    def and_then(self, fn: Callable[[TResult], Result[UResult, EResult]]) -> Result[UResult, EResult]:
        """Return self without calling the function.

        Args:
            fn: Ignored for Err.

        Returns:
            self.
        """
        return self

    def or_else(self, fn: Callable[[EResult], Result[UResult, EResult]]) -> Result[UResult, EResult]:
        """Apply fn to the error value and return the result.

        Args:
            fn: A callable that takes the error and returns Result.

        Returns:
            The result of fn(error).
        """
        return fn(self._value)

    def inspect(self, fn: Callable[[TResult], None]) -> Result[TResult, EResult]:
        """Do nothing (the function is not called for Err).

        Args:
            fn: Ignored.

        Returns:
            self.
        """
        return self

    def inspect_err(self, fn: Callable[[EResult], None]) -> Result[TResult, EResult]:
        """Inspect the error value.

        Args:
            fn: A callable to invoke with the error.

        Returns:
            self.
        """
        fn(self._value)
        return self

    def is_ok_and(self, fn: Callable[[TResult], bool]) -> bool:
        """Return False (Err never has a success value).

        Args:
            fn: Ignored.

        Returns:
            False.
        """
        return False

    def is_err_and(self, fn: Callable[[EResult], bool]) -> bool:
        """Check if the error satisfies the predicate.

        Args:
            fn: A predicate function to apply to the error.

        Returns:
            The result of fn(error).
        """
        return fn(self._value)

    def ok(self) -> Option[TResult]:
        """Convert to Nothing (Err has no success value).

        Returns:
            Nothing().
        """
        return Nothing()

    def err(self) -> Option[EResult]:
        """Convert to Some.

        Returns:
            Some(error).
        """
        return Some(self._value)

    def map(self, fn: Callable[[TResult], UResult]) -> Monad[Any]:
        """Return self without calling the function.

        Args:
            fn: Ignored for Err.

        Returns:
            self.
        """
        return self

    def flatmap(self, fn: Callable[[TResult], Monad[UResult]]) -> Monad[Any]:
        """Return self without calling the function.

        Args:
            fn: Ignored for Err.

        Returns:
            self.
        """
        return self

    def is_ok(self) -> bool:
        """Check if this is Ok.

        Returns:
            False.
        """
        return False

    def is_err(self) -> bool:
        """Check if this is Err.

        Returns:
            True.
        """
        return True

    def __bool__(self) -> bool:
        """Check if the Result is Ok.

        Returns:
            False.
        """
        return False

    def __eq__(self, other: object) -> bool:
        """Check equality with another Result.

        Args:
            other: The object to compare.

        Returns:
            True if other is Err with equal error, False otherwise.
        """
        if isinstance(other, Err):
            return self._value == other._value
        return False

    def __hash__(self) -> int:
        """Return a hash value for the Err.

        Note:
            Err objects are intentionally not hashable because error values
            (e.g., exceptions, custom error objects, lists, dicts) are often
            not hashable. If you need to use Err in a set or as a dict key,
            wrap the error in a hashable type (e.g., a string or tuple).

        Raises:
            TypeError: Always raised since Err is not hashable.
        """
        raise TypeError(f"'{type(self).__name__}' objects are not hashable")

    def __rshift__(self, fn: Callable[[TResult], Monad[UResult]]) -> Monad[Any]:
        """Return self without calling the function.

        Args:
            fn: Ignored for Err.

        Returns:
            self.
        """
        return self

    def __repr__(self) -> str:
        """Return a string representation.

        Returns:
            'Result::Err(error)'.
        """
        return f"Result::Err({self._value!r})"

    def __copy__(self) -> "Err[EResult]":
        """Create a shallow copy of Err.

        Returns:
            A new Err with a shallow copy of the wrapped error value.
        """
        return Err(copy.copy(self._value))

    def __deepcopy__(self, memo: dict) -> "Err[EResult]":
        """Create a deep copy of Err.

        Args:
            memo: A dictionary for memoization of already copied objects.

        Returns:
            A new Err with a deep copy of the wrapped error value.
        """
        return Err(copy.deepcopy(self._value, memo))


from .option import Option, Some, Nothing

