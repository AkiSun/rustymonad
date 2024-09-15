from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TypeVar, Callable, Any
from .monad import Monad
from . import Result, Ok, Err


T = TypeVar('T')
U = TypeVar('U')
E = TypeVar('E')


class Maybe(Monad[T], ABC):
    @abstractmethod
    def expect(self, msg: str) -> T:
        raise NotImplementedError

    @abstractmethod
    def unwrap(self) -> T:
        raise NotImplementedError

    @abstractmethod
    def unwrap_or(self, default: T) -> T:
        raise NotImplementedError

    @abstractmethod
    def and_then(self, fn: Callable[[T], Maybe[U]]) -> Maybe[U]:
        raise NotImplementedError

    @abstractmethod
    def or_else(self, fn: Callable[[], Maybe[U]]) -> Maybe[U]:
        raise NotImplementedError
    
    @abstractmethod
    def inspect(self, fn: Callable[[T], None]) -> Maybe[T]:
        raise NotImplementedError
    
    @abstractmethod
    def is_just_and(self, fn: Callable[[T], bool]) -> bool:
        raise NotImplementedError
    
    @abstractmethod
    def ok_or(self, err: E) -> Result[T, E]:
        raise NotImplementedError
    
    @abstractmethod
    def filter(self, fn: Callable[[T], bool]) -> Maybe[T]:
        raise NotImplementedError

    @abstractmethod
    def map(self, fn: Callable[[T], U]) -> Monad[U]:
        raise NotImplementedError

    @abstractmethod
    def flatmap(self, fn: Callable[[T], Monad[U]]) -> Monad[U]:
        raise NotImplementedError

    @abstractmethod
    def is_just(self) -> bool:
        raise NotImplementedError

    @abstractmethod
    def is_nothing(self) -> bool:
        raise NotImplementedError

    @abstractmethod
    def __bool__(self) -> bool:
        raise NotImplementedError

    @abstractmethod
    def __eq__(self, other: object) -> bool:
        raise NotImplementedError

    @abstractmethod
    def __rshift__(self, fn: Callable[[T], Monad[U]]) -> Monad[U]:
        raise NotImplementedError

    @abstractmethod
    def __repr__(self) -> str:
        raise NotImplementedError


class Just(Maybe[T]):
    def expect(self, msg: str) -> T:
        return self._value

    def unwrap(self) -> T:
        return self._value

    def unwrap_or(self, default: T) -> T:
        return self._value

    def and_then(self, fn: Callable[[T], Maybe[U]]) -> Maybe[U]:
        if isinstance(value := fn(self._value), Maybe):
            return value
        else:
            return Just(value)

    def or_else(self, fn: Callable[[], Maybe[U]]) -> Maybe[Any]:
        return self

    def inspect(self, fn: Callable[[T], None]) -> Maybe[T]:
        fn(self._value)
        return self
    
    def is_just_and(self, fn: Callable[[T], bool]) -> bool:
        return fn(self._value)
    
    def ok_or(self, err: E) -> Result[T, E]:
        return Ok(self._value)
    
    def filter(self, fn: Callable[[T], bool]) -> Maybe[T]:
        if fn(self._value):
            return self
        return Nothing()

    def map(self, fn: Callable[[T], U]) -> Monad[U]:
        return Just(fn(self._value))

    def flatmap(self, fn: Callable[[T], Monad[U]]) -> Monad[U]:
        return fn(self._value)

    def is_just(self) -> bool:
        return True

    def is_nothing(self) -> bool:
        return False

    def __bool__(self) -> bool:
        return True

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Just):
            return self._value == other._value
        return False

    def __rshift__(self, fn: Callable[[T], Monad[U]]) -> Monad[U]:
        return fn(self._value)

    def __repr__(self) -> str:
        return f'Maybe::Just({self._value!r})'


class Nothing(Maybe[Any]):
    __instance: Nothing | None = None

    def __new__(cls) -> Nothing:
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance
    
    def __init__(self) -> None:
        super().__init__(Ellipsis)

    def expect(self, msg: str):
        raise Exception(msg)

    def unwrap(self):
        raise Exception('called `Maybe::unwrap()` on a `Nothing` value')

    def unwrap_or(self, default: T) -> T:
        return default

    def and_then(self, fn: Callable[[Any], Maybe[U]]) -> Maybe[Any]:
        return self

    def or_else(self, fn: Callable[[], Maybe[U]]) -> Maybe[U]:
        return fn()
    
    def inspect(self, fn: Callable[[T], None]) -> Maybe[T]:
        return self
    
    def is_just_and(self, fn: Callable[[T], bool]) -> bool:
        return False
    
    def ok_or(self, err: E) -> Result[T, E]:
        return Err(err)

    def filter(self, fn: Callable[[T], bool]) -> Maybe[T]:
        return self

    def map(self, fn: Callable[[T], U]) -> Monad[Any]:
        return self

    def flatmap(self, fn: Callable[[T], Monad[U]]) -> Monad[Any]:
        return self
    
    def is_just(self) -> bool:
        return False

    def is_nothing(self) -> bool:
        return True
    
    def __bool__(self) -> bool:
        return False

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Nothing):
            return True
        return False

    def __rshift__(self, fn: Callable[[T], Monad[U]]) -> Monad[Any]:
        return self

    def __repr__(self) -> str:
        return 'Maybe::Nothing'

Nothing()
