from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TypeVar, Callable, Any
from .monad import Monad


T = TypeVar('T')
U = TypeVar('U')


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

    @staticmethod
    def just(value: T) -> Just[T]:
        return Just(value)

    @staticmethod
    def nothing() -> NothingType:
        return Nothing


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
        return f'Maybe::Just({self._value.__repr__()})'


class NothingType(Maybe[T]):
    def expect(self, msg: str):
        raise Exception(msg)

    def unwrap(self):
        raise Exception('Nothing')

    def unwrap_or(self, default: T) -> T:
        return default

    def and_then(self, fn: Callable[[T], Maybe[U]]) -> Maybe[Any]:
        return self

    def or_else(self, fn: Callable[[], Maybe[U]]) -> Maybe[U]:
        return fn()

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
        if isinstance(other, NothingType):
            return True
        return False

    def __rshift__(self, fn: Callable[[T], Monad[U]]) -> Monad[Any]:
        return self

    def __repr__(self) -> str:
        return 'Maybe::Nothing'


Nothing: NothingType = NothingType(None)
