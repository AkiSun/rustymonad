"""RustyMonad - A Python implementation of Rust-style monads.

This library provides Option and Result types with comprehensive monadic operations,
inspired by Rust's standard library. It enables functional programming patterns
in Python with proper error handling and composition.

Modules:
    monad: Base Monad class and core functionality.
    option: Option type (Some/Nothing) for nullable values.
    result: Result type (Ok/Err) for error handling.
    utils: Utility functions for do-notation and try-notation.
    errors: Custom exception types for rustymonad.

Example:
    >>> from rustymonad import Option, Result, Some, Nothing, Ok, Err
    >>> def divide(a: int, b: int) -> Result[int, str]:
    ...     if b == 0:
    ...         return Err("division by zero")
    ...     return Ok(a // b)
    >>> result = Ok(10).and_then(lambda x: divide(x, 2))
    >>> result.unwrap()
    5
"""
from .monad import Monad
from .option import Option, Some, Nothing
from .result import Result, Ok, Err
from .utils import DoRet, do_notation, try_notation
from .errors import (
    RustyMonadError,
    ResultError,
    OptionError,
    UnwrapError,
    ExpectError,
    UnwrapUncheckedError,
    UnwrapOptionError,
    ExpectOptionError,
    DoNotationError,
)


__all__ = [
    'Monad',
    'Option',
    'Some',
    'Nothing',
    'Result',
    'Ok',
    'Err',
    'DoRet',
    'do_notation',
    'try_notation',
    'RustyMonadError',
    'ResultError',
    'OptionError',
    'UnwrapError',
    'ExpectError',
    'UnwrapUncheckedError',
    'UnwrapOptionError',
    'ExpectOptionError',
    'DoNotationError',
]
