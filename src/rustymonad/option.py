"""Option type for handling nullable values.

This module provides the Option type, which is used to represent a value that
may or may not exist. It is inspired by Rust's Option type and consists of
two variants: Some (contains a value) and Nothing (represents the absence of value).

The Option type is useful for:
- Handling nullable values without using None
- Avoiding NoneType errors through type checking
- Composing functions that may or may not return a value

Example:
    >>> def find_user(id: int) -> Option[User]:
    ...     # Returns Some(user) if found, Nothing otherwise
    ...     pass
    >>> user = find_user(123)
    >>> user.unwrap_or(default_user).name
"""

from __future__ import annotations
from abc import ABC, ABCMeta, abstractmethod
from typing import TypeVar, Callable, Any
import copy
from .monad import Monad
from .errors import ExpectOptionError, UnwrapOptionError


T = TypeVar("T")
U = TypeVar("U")
E = TypeVar("E")


class Option(Monad[T], ABC):
    """Abstract base class for Option type.

    Option represents a value that may or may not exist. This abstract class
    defines the interface that both Some and Nothing must implement.

    Use Some(value) to wrap a value, or Nothing() to represent absence.

    Attributes:
        _value: The wrapped value (use unwrap() to access).

    Example:
        >>> opt = Some(42)
        >>> opt.unwrap()
        42
        >>> Nothing()
        Option::Nothing
    """
    __slots__ = ()

    @abstractmethod
    def expect(self, msg: str) -> T:
        """Return the contained value or raise with a custom message.

        Args:
            msg: Error message to use if the value is Nothing.

        Returns:
            The contained value if Some.

        Raises:
            ExpectOptionError: If the value is Nothing.
        """
        raise NotImplementedError

    @abstractmethod
    def unwrap(self) -> T:
        """Return the contained value.

        Returns:
            The contained value if Some.

        Raises:
            UnwrapOptionError: If the value is Nothing.
        """
        raise NotImplementedError

    @abstractmethod
    def unwrap_or(self, default: T) -> T:
        """Return the contained value or a default if Nothing.

        Args:
            default: The value to return if this is Nothing.

        Returns:
            The contained value if Some, otherwise the default.
        """
        raise NotImplementedError

    @abstractmethod
    def and_then(self, fn: Callable[[T], Option[U]]) -> Option[U]:
        """Apply a function that returns Option to the contained value.

        Args:
            fn: A callable that takes the contained value and returns Option[U].

        Returns:
            The result of fn if Some, Nothing if the result is Nothing.

        Example:
            >>> Some(5).and_then(lambda x: Some(x * 2))
            Option::Some(10)
        """
        raise NotImplementedError

    @abstractmethod
    def or_else(self, fn: Callable[[], Option[U]]) -> Option[U]:
        """Return the contained value or compute an alternative.

        Args:
            fn: A callable that returns an alternative Option if Nothing.

        Returns:
            The contained value if Some, otherwise the result of fn().

        Example:
            >>> Nothing().or_else(lambda: Some(default))
            Option::Some(default)
        """
        raise NotImplementedError

    @abstractmethod
    def inspect(self, fn: Callable[[T], None]) -> Option[T]:
        """Inspect the contained value without modifying it.

        Args:
            fn: A callable to invoke with the contained value (if Some).

        Returns:
            self, allowing method chaining.

        Example:
            >>> Some(42).inspect(print)
            Option::Some(42)
        """
        raise NotImplementedError

    @abstractmethod
    def is_some_and(self, fn: Callable[[T], bool]) -> bool:
        """Check if Some and the value satisfies a predicate.

        Args:
            fn: A predicate function to apply to the value.

        Returns:
            True if Some and fn(value) is True, otherwise False.

        Example:
            >>> Some(5).is_some_and(lambda x: x > 0)
            True
        """
        raise NotImplementedError

    @abstractmethod
    def ok_or(self, err: E) -> Result[T, E]:
        """Convert to a Result, mapping Nothing to Err.

        Args:
            err: The error value to use if Nothing.

        Returns:
            Ok(value) if Some, Err(err) if Nothing.

        Example:
            >>> Some(42).ok_or("error")
            Result::Ok(42)
        """
        raise NotImplementedError

    @abstractmethod
    def filter(self, fn: Callable[[T], bool]) -> Option[T]:
        """Keep the value only if it satisfies a predicate.

        Args:
            fn: A predicate function. Returns Some if True, Nothing if False.

        Returns:
            Self if Some and fn(value) is True, otherwise Nothing.

        Example:
            >>> Some(5).filter(lambda x: x > 3)
            Option::Some(5)
        """
        raise NotImplementedError

    @abstractmethod
    def map(self, fn: Callable[[T], U]) -> Monad[U]:
        """Apply a function to the contained value.

        Args:
            fn: A callable that transforms the contained value.

        Returns:
            Some(fn(value)) if Some, Nothing if Nothing.

        Example:
            >>> Some(5).map(lambda x: x * 2)
            Option::Some(10)
        """
        raise NotImplementedError

    @abstractmethod
    def flatmap(self, fn: Callable[[T], Monad[U]]) -> Monad[U]:
        """Apply a function that returns a Monad to the contained value.

        Args:
            fn: A callable that takes the value and returns Monad[U].

        Returns:
            The result of fn if Some, Nothing if Nothing.

        Example:
            >>> Some(5).flatmap(lambda x: Some(x * 2))
            Option::Some(10)
        """
        raise NotImplementedError

    @abstractmethod
    def is_some(self) -> bool:
        """Check if this is a Some variant.

        Returns:
            True if Some, False if Nothing.
        """
        raise NotImplementedError

    @abstractmethod
    def is_nothing(self) -> bool:
        """Check if this is a Nothing variant.

        Returns:
            True if Nothing, False if Some.
        """
        raise NotImplementedError

    @abstractmethod
    def __bool__(self) -> bool:
        """Check if the Option contains a value.

        Returns:
            True if Some, False if Nothing.
        """
        raise NotImplementedError

    # Note: We don't define __eq__ and __hash__ as abstract here because
    # Option inherits __eq__ and __hash__ from Monad, which already provides
    # correct implementations. The concrete Some and Nothing classes override
    # these methods as needed.

    @abstractmethod
    def __rshift__(self, fn: Callable[[T], Monad[U]]) -> Monad[U]:
        """Bind operation using >> operator.

        Args:
            fn: A callable that takes the value and returns Monad[U].

        Returns:
            The result of fn if Some, Nothing if Nothing.
        """
        raise NotImplementedError

    @abstractmethod
    def __repr__(self) -> str:
        """Return a string representation of the Option.

        Returns:
            'Option::Some(value)' or 'Option::Nothing'.
        """
        raise NotImplementedError


class Some(Option[T]):
    """Option variant that contains a value.

    Some represents the presence of a value. It is created by wrapping
    any value with Some().

    Example:
        >>> Some(42)
        Option::Some(42)
        >>> Some("hello")
        Option::Some('hello')
    """
    __slots__ = ()

    def expect(self, msg: str) -> T:
        """Return the contained value (Some always returns the value).

        Args:
            msg: Ignored for Some.

        Returns:
            The contained value.
        """
        return self._value

    def unwrap(self) -> T:
        """Return the contained value.

        Returns:
            The contained value.
        """
        return self._value

    def unwrap_or(self, default: T) -> T:
        """Return the contained value (ignores the default).

        Args:
            default: Ignored for Some.

        Returns:
            The contained value.
        """
        return self._value

    def or_else(self, fn: Callable[[], Option[U]]) -> Option[Any]:
        """Return the contained value (ignores the alternative function).

        Args:
            fn: Ignored for Some.

        Returns:
            self.
        """
        return self

    def inspect(self, fn: Callable[[T], None]) -> Option[T]:
        """Inspect the contained value.

        Args:
            fn: A callable to invoke with the value.

        Returns:
            self.
        """
        fn(self._value)
        return self

    def is_some_and(self, fn: Callable[[T], bool]) -> bool:
        """Check if the value satisfies the predicate.

        Args:
            fn: A predicate function to apply to the value.

        Returns:
            The result of fn(value).
        """
        return fn(self._value)

    def ok_or(self, err: E) -> Result[T, E]:
        """Convert to Result::Ok.

        Args:
            err: Ignored for Some.

        Returns:
            Ok(value).
        """
        return Ok(self._value)

    def filter(self, fn: Callable[[T], bool]) -> Option[T]:
        """Keep the value only if it satisfies the predicate.

        Args:
            fn: A predicate function.

        Returns:
            self if fn(value) is True, otherwise Nothing.
        """
        if fn(self._value):
            return self
        return Nothing()

    def and_then(self, fn: Callable[[T], Option[U]]) -> Option[U]:
        """Apply fn to the contained value and return the result.

        Args:
            fn: A callable that takes the value and returns Option[U].

        Returns:
            The result of fn(value).

        Raises:
            TypeError: If fn does not return an Option instance.
        """
        result = fn(self._value)
        if not isinstance(result, Option):
            raise TypeError(
                f"and_then expects fn to return Option, got {type(result).__name__}"
            )
        return result

    def flatmap(self, fn: Callable[[T], Monad[U]]) -> Monad[U]:
        """Apply fn to the contained value and return the result.

        Args:
            fn: A callable that takes the value and returns Monad[U].

        Returns:
            The result of fn(value).
        """
        return fn(self._value)

    def map(self, fn: Callable[[T], U]) -> Monad[U]:
        """Apply fn to the contained value and return Some with the result.

        Args:
            fn: A callable that transforms the contained value.

        Returns:
            Some(fn(value)).
        """
        return Some(fn(self._value))

    def is_some(self) -> bool:
        """Check if this is Some.

        Returns:
            True.
        """
        return True

    def is_nothing(self) -> bool:
        """Check if this is Nothing.

        Returns:
            False.
        """
        return False

    def __bool__(self) -> bool:
        """Check if the Option contains a value.

        Returns:
            True.
        """
        return True

    def __eq__(self, other: object) -> bool:
        """Check equality with another Option.

        Args:
            other: The object to compare.

        Returns:
            True if other is Some with equal value, False otherwise.
        """
        if isinstance(other, Some):
            return self._value == other._value
        return False

    def __lt__(self, other: object) -> bool:
        """Less than comparison for Option.

        Args:
            other: The object to compare.

        Returns:
            True if other is Nothing (Some > Nothing),
            True if other is Some and self._value < other._value,
            TypeError if types are incompatible.
        """
        if isinstance(other, Nothing):
            return False  # Some > Nothing
        if isinstance(other, Some):
            return self._value < other._value
        raise TypeError(
            f"'<' not supported between instances of 'Some' and '{type(other).__name__}'"
        )

    def __le__(self, other: object) -> bool:
        """Less than or equal comparison for Option.

        Args:
            other: The object to compare.

        Returns:
            True if other is Nothing (Some > Nothing),
            True if other is Some and self._value <= other._value,
            TypeError if types are incompatible.
        """
        if isinstance(other, Nothing):
            return False  # Some > Nothing
        if isinstance(other, Some):
            return self._value <= other._value
        raise TypeError(
            f"'<=' not supported between instances of 'Some' and '{type(other).__name__}'"
        )

    def __gt__(self, other: object) -> bool:
        """Greater than comparison for Option.

        Args:
            other: The object to compare.

        Returns:
            True if other is Nothing (Some > Nothing),
            True if other is Some and self._value > other._value,
            TypeError if types are incompatible.
        """
        if isinstance(other, Nothing):
            return True  # Some > Nothing
        if isinstance(other, Some):
            return self._value > other._value
        raise TypeError(
            f"'>' not supported between instances of 'Some' and '{type(other).__name__}'"
        )

    def __ge__(self, other: object) -> bool:
        """Greater than or equal comparison for Option.

        Args:
            other: The object to compare.

        Returns:
            True if other is Nothing (Some > Nothing),
            True if other is Some and self._value >= other._value,
            TypeError if types are incompatible.
        """
        if isinstance(other, Nothing):
            return True  # Some > Nothing
        if isinstance(other, Some):
            return self._value >= other._value
        raise TypeError(
            f"'>=' not supported between instances of 'Some' and '{type(other).__name__}'"
        )

    def __hash__(self) -> int:
        """Return a hash value for the Some.

        Returns:
            Hash value based on the wrapped value.
        """
        return hash(self._value)

    def __rshift__(self, fn: Callable[[T], Monad[U]]) -> Monad[U]:
        """Apply fn to the contained value and return the result.

        Args:
            fn: A callable that takes the value and returns Monad[U].

        Returns:
            The result of fn(value).
        """
        return fn(self._value)

    def __repr__(self) -> str:
        """Return a string representation.

        Returns:
            'Option::Some(value)'.
        """
        return f"Option::Some({self._value!r})"

    def __copy__(self) -> "Some[T]":
        """Create a shallow copy of Some.

        Returns:
            A new Some with a shallow copy of the wrapped value.
        """
        return Some(copy.copy(self._value))

    def __deepcopy__(self, memo: dict) -> "Some[T]":
        """Create a deep copy of Some.

        Args:
            memo: A dictionary for memoization of already copied objects.

        Returns:
            A new Some with a deep copy of the wrapped value.
        """
        return Some(copy.deepcopy(self._value, memo))


class NothingMeta(ABCMeta):
    """Metaclass that implements the Nothing singleton pattern.

    This metaclass ensures that only one Nothing instance exists,
    making Nothing a singleton similar to Rust's None.
    """
    _instance: "Nothing" | None = None

    def __call__(cls, *args, **kwargs) -> "Nothing":
        """Return the singleton Nothing instance.

        Returns:
            The singleton Nothing instance.
        """
        if cls._instance is None:
            cls._instance = super().__call__(*args, **kwargs)
        return cls._instance


class Nothing(Option[Any], metaclass=NothingMeta):
    """Option variant that represents the absence of a value.

    Nothing is a singleton that represents when a value does not exist.
    It is similar to Rust's None or Python's None, but with type safety.

    Example:
        >>> Nothing()
        Option::Nothing
        >>> Nothing() is Nothing()
        True
    """
    __slots__ = ()

    def __init__(self, value: Any = None) -> None:
        """Initialize Nothing (singleton, ignores the value).

        Args:
            value: Ignored.
        """
        if value is None:
            value = Ellipsis
        super().__init__(value)

    def expect(self, msg: str):
        """Raise ExpectOptionError with the given message.

        Args:
            msg: The error message.

        Raises:
            ExpectOptionError: Always raised for Nothing.
        """
        raise ExpectOptionError(msg)

    def unwrap(self):
        """Raise UnwrapOptionError.

        Raises:
            UnwrapOptionError: Always raised for Nothing.
        """
        raise UnwrapOptionError()

    def unwrap_or(self, default: T) -> T:
        """Return the default value.

        Args:
            default: The value to return.

        Returns:
            The default value.
        """
        return default

    def and_then(self, fn: Callable[[Any], Option[U]]) -> Option[Any]:
        """Return Nothing without calling the function.

        Args:
            fn: Ignored.

        Returns:
            self (Nothing).
        """
        return self

    def or_else(self, fn: Callable[[], Option[U]]) -> Option[U]:
        """Call the alternative function and return its result.

        Args:
            fn: A callable that returns an alternative Option.

        Returns:
            The result of fn().
        """
        return fn()

    def inspect(self, fn: Callable[[T], None]) -> Option[T]:
        """Do nothing (the function is not called).

        Args:
            fn: Ignored.

        Returns:
            self.
        """
        return self

    def is_some_and(self, fn: Callable[[T], bool]) -> bool:
        """Return False (Nothing never satisfies a predicate).

        Args:
            fn: Ignored.

        Returns:
            False.
        """
        return False

    def ok_or(self, err: E) -> Result[T, E]:
        """Convert to Result::Err.

        Args:
            err: The error value to use.

        Returns:
            Err(err).
        """
        return Err(err)

    def filter(self, fn: Callable[[T], bool]) -> Option[T]:
        """Return Nothing (Nothing never passes a filter).

        Args:
            fn: Ignored.

        Returns:
            self.
        """
        return self

    def map(self, fn: Callable[[T], U]) -> Monad[Any]:
        """Return Nothing without calling the function.

        Args:
            fn: Ignored.

        Returns:
            self.
        """
        return self

    def flatmap(self, fn: Callable[[T], Monad[U]]) -> Monad[Any]:
        """Return Nothing without calling the function.

        Args:
            fn: Ignored.

        Returns:
            self.
        """
        return self

    def is_some(self) -> bool:
        """Check if this is Some.

        Returns:
            False.
        """
        return False

    def is_nothing(self) -> bool:
        """Check if this is Nothing.

        Returns:
            True.
        """
        return True

    def __bool__(self) -> bool:
        """Check if the Option contains a value.

        Returns:
            False.
        """
        return False

    def __eq__(self, other: object) -> bool:
        """Check equality with another Option.

        Args:
            other: The object to compare.

        Returns:
            True if other is Nothing, False otherwise.
        """
        if isinstance(other, Nothing):
            return True
        return False

    def __lt__(self, other: object) -> bool:
        """Less than comparison for Option.

        Args:
            other: The object to compare.

        Returns:
            True if other is Some (Nothing < Some),
            False if other is Nothing,
            TypeError if types are incompatible.
        """
        if isinstance(other, Some):
            return True  # Nothing < Some
        if isinstance(other, Nothing):
            return False  # Nothing == Nothing
        raise TypeError(
            f"'<' not supported between instances of 'Nothing' and '{type(other).__name__}'"
        )

    def __le__(self, other: object) -> bool:
        """Less than or equal comparison for Option.

        Args:
            other: The object to compare.

        Returns:
            True if other is Some (Nothing < Some),
            True if other is Nothing (Nothing == Nothing),
            TypeError if types are incompatible.
        """
        if isinstance(other, Some):
            return True  # Nothing < Some
        if isinstance(other, Nothing):
            return True  # Nothing == Nothing
        raise TypeError(
            f"'<=' not supported between instances of 'Nothing' and '{type(other).__name__}'"
        )

    def __gt__(self, other: object) -> bool:
        """Greater than comparison for Option.

        Args:
            other: The object to compare.

        Returns:
            False if other is Some (Nothing < Some),
            False if other is Nothing,
            TypeError if types are incompatible.
        """
        if isinstance(other, Some):
            return False  # Nothing < Some
        if isinstance(other, Nothing):
            return False  # Nothing == Nothing
        raise TypeError(
            f"'>' not supported between instances of 'Nothing' and '{type(other).__name__}'"
        )

    def __ge__(self, other: object) -> bool:
        """Greater than or equal comparison for Option.

        Args:
            other: The object to compare.

        Returns:
            False if other is Some (Nothing < Some),
            True if other is Nothing (Nothing == Nothing),
            TypeError if types are incompatible.
        """
        if isinstance(other, Some):
            return False  # Nothing < Some
        if isinstance(other, Nothing):
            return True  # Nothing == Nothing
        raise TypeError(
            f"'>=' not supported between instances of 'Nothing' and '{type(other).__name__}'"
        )

    def __hash__(self) -> int:
        """Return a hash value for the Nothing.

        Returns:
            hash(None) - same as hashing None.
        """
        return hash(None)

    def __rshift__(self, fn: Callable[[T], Monad[U]]) -> Monad[Any]:
        """Return Nothing without calling the function.

        Args:
            fn: Ignored.

        Returns:
            self.
        """
        return self

    def __repr__(self) -> str:
        """Return a string representation.

        Returns:
            'Option::Nothing'.
        """
        return "Option::Nothing"

    def __copy__(self) -> "Nothing":
        """Return the singleton Nothing instance.

        Returns:
            The singleton Nothing instance.
        """
        return self

    def __deepcopy__(self, memo: dict) -> "Nothing":
        """Return the singleton Nothing instance.

        Args:
            memo: Ignored (Nothing is a singleton).

        Returns:
            The singleton Nothing instance.
        """
        return self


# Export Nothing as a function that returns the singleton


from .result import Result, Ok, Err
