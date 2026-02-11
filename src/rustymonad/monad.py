"""Base Monad class and core monadic functionality.

This module provides the foundational Monad class that serves as the base
for Option and Result types. It implements basic monadic operations that
enable chaining and composition of values.
"""

from __future__ import annotations
from typing import TypeVar, Generic, Callable
import copy


TMonad = TypeVar('TMonad')
UMonad = TypeVar('UMonad')


class Monad(Generic[TMonad]):
    """Base monad class providing fundamental monadic operations.

    This class serves as the foundation for Option and Result types.
    It implements the basic interface for monadic operations including
    mapping, flatmapping, and value extraction.

    Attributes:
        _value: The wrapped value inside the monad.

    Example:
        >>> monad = Monad(42)
        >>> monad.unwrap()
        42
        >>> monad.map(lambda x: x * 2).unwrap()
        84
    """
    __slots__ = ('_value',)
    __match_args__ = ('_value',)

    def __init__(self, value: TMonad) -> None:
        """Initialize a Monad with the given value.

        Args:
            value: The value to wrap inside the monad.
        """
        self._value = value

    def unwrap(self) -> TMonad:
        """Return the contained value.

        Returns:
            The value wrapped by this monad.
        """
        return self._value

    def map(self, fn: Callable[[TMonad], UMonad]) -> Monad[UMonad]:
        """Apply a function to the contained value.

        Args:
            fn: A callable that transforms the contained value.

        Returns:
            A new Monad containing the transformed value.

        Example:
            >>> Monad(5).map(lambda x: x * 2)
            Monad(10)
        """
        return Monad(fn(self._value))

    def flatmap(self, fn: Callable[[TMonad], Monad[UMonad]]) -> Monad[UMonad]:
        """Apply a function that returns a Monad to the contained value.

        Args:
            fn: A callable that takes the contained value and returns a Monad.

        Returns:
            The result of applying fn to the contained value.

        Example:
            >>> def add_one(x: int) -> Monad[int]:
            ...     return Monad(x + 1)
            >>> Monad(5).flatmap(add_one)
            Monad(6)
        """
        return fn(self._value)

    def __bool__(self) -> bool:
        """Return True indicating the monad contains a value.

        Returns:
            True, as a Monad always contains a value.
        """
        return True

    def __eq__(self, other: object) -> bool:
        """Check equality with another object.

        Args:
            other: The object to compare with.

        Returns:
            True if other is a Monad with the same wrapped value, False otherwise.
        """
        if isinstance(other, Monad):
            return self._value == other._value
        return False

    def __rshift__(self, fn: Callable[[TMonad], Monad[UMonad]]):
        """Bind operation using >> operator.

        This enables the >> operator for chaining monadic operations.

        Args:
            fn: A callable that takes the contained value and returns a Monad.

        Returns:
            The result of applying fn to the contained value.

        Example:
            >>> Monad(5) >> (lambda x: Monad(x * 2))
            Monad(10)
        """
        return fn(self._value)

    def __repr__(self) -> str:
        """Return a string representation of the Monad.

        Returns:
            A string in the format 'Monad(value)'.
        """
        return f'Monad({self._value!r})'

    def __copy__(self) -> "Monad[TMonad]":
        """Create a shallow copy of the Monad.

        Returns:
            A new Monad with the same wrapped value (shallow copy of the value).
        """
        return self.__class__(copy.copy(self._value))

    def __deepcopy__(self, memo: dict) -> "Monad[TMonad]":
        """Create a deep copy of the Monad.

        Args:
            memo: A dictionary for memoization of already copied objects.

        Returns:
            A new Monad with a deep copy of the wrapped value.
        """
        return self.__class__(copy.deepcopy(self._value, memo))

