from abc import ABC, abstractmethod
from typing import Generic, TypeVar, Callable
from .monad import Monad


T = TypeVar('T')
U = TypeVar('U')
E = TypeVar('E')
F = TypeVar('F')

class Result(Generic[T, E], Monad[T | E], ABC):
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
    def and_then(self, fn: Callable[[T], U] | Callable[[T], 'Result[U, E]']) -> 'Result[U, E]':
        raise NotImplementedError

    @abstractmethod
    def or_else(self, fn: Callable[[E], F] | Callable[[E], 'Result[T, F]']) -> 'Result[T, F]':
        raise NotImplementedError

    @abstractmethod
    def map(self, fn: Callable[[T], U]) -> 'Result[U, E]':
        raise NotImplementedError

    @abstractmethod
    def flatmap(self, fn: Callable[[T], 'Result[U, E]']) -> 'Result[U, E]':
        raise NotImplementedError

    @abstractmethod
    def is_ok(self) -> bool:
        raise NotImplementedError

    @abstractmethod
    def is_err(self) -> bool:
        raise NotImplementedError

    @abstractmethod
    def __bool__(self) -> bool:
        raise NotImplementedError

    @abstractmethod
    def __eq__(self, other: object) -> bool:
        raise NotImplementedError

    @abstractmethod
    def __repr__(self) -> str:
        raise NotImplementedError

    @staticmethod
    def ok(value: T) -> 'Ok[T]':
        return Ok(value)

    @staticmethod
    def err(value: E | str) -> 'Err[E]':
        return Err(value)


class Ok(Generic[T, E], Result[T, E]):
    def __init__(self, value: T):
        super().__init__(value)

    def expect(self, msg: str) -> T:
        return self._value

    def unwrap(self) -> T:
        return self._value

    def unwrap_or(self, default: T) -> T:
        return self._value

    def and_then(self, fn: Callable[[T], U] | Callable[[T], Result[U, E]]) -> Result[U, E]:
        if isinstance(value := fn(self._value), Result):
            return value
        else:
            return Ok(value)

    def or_else(self, fn: Callable[[E], F] | Callable[[E], Result[T, F]]) -> Result[T, F]:
        return self

    def map(self, fn: Callable[[T], U]) -> Result[U, E]:
        return Ok(fn(self._value))

    def flatmap(self, fn: Callable[[T], Result[U, E]]) -> Result[U, E]:
        return fn(self._value)

    def is_ok(self) -> bool:
        return True

    def is_err(self) -> bool:
        return False

    def __bool__(self) -> bool:
        return True

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Ok):
            return self._value == other._value
        return False

    def __repr__(self) -> str:
        return f'Result::Ok({self._value.__repr__()})'


class Err(Generic[T, E], Result[T, E]):
    def __init__(self, value: E):
        super().__init__(value)

    def expect(self, msg: str) -> T:
        raise Exception(f'{msg}: {self._value}')

    def unwrap(self):
        if isinstance(self._value, Exception):
            raise self._value
        else:
            raise Exception(self._value)

    def unwrap_or(self, default: T) -> T:
        return default

    def and_then(self, fn: Callable[[T], U] | Callable[[T], Result[U, E]]) -> Result[U, E]:
        return self

    def or_else(self, fn: Callable[[E], F] | Callable[[E], Result[T, F]]) -> Result[T, F]:
        if isinstance(value := fn(self._value), Result):
            return value
        else:
            return Ok(value)

    def map(self, fn: Callable[[T], U]) -> Result[U, E]:
        return self

    def flatmap(self, fn: Callable[[T], Result[U, E]]) -> Result[U, E]:
        return self

    def is_ok(self) -> bool:
        return False

    def is_err(self) -> bool:
        return True

    def __bool__(self) -> bool:
        return False

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Err):
            return self._value.args == other._value.args
        return False

    def __repr__(self) -> str:
        return f'Result::Err({self._value.__repr__()})'
