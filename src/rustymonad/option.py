from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TypeVar, Callable, Any
from .monad import Monad


T = TypeVar('T')
U = TypeVar('U')
E = TypeVar('E')


class Option(Monad[T], ABC):
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
    def and_then(self, fn: Callable[[T], Option[U]]) -> Option[U]:
        raise NotImplementedError

    @abstractmethod
    def or_else(self, fn: Callable[[], Option[U]]) -> Option[U]:
        raise NotImplementedError
    
    @abstractmethod
    def inspect(self, fn: Callable[[T], None]) -> Option[T]:
        raise NotImplementedError
    
    @abstractmethod
    def is_some_and(self, fn: Callable[[T], bool]) -> bool:
        raise NotImplementedError

    @abstractmethod
    def ok_or(self, err: E) -> Result[T, E]:
        raise NotImplementedError
    
    @abstractmethod
    def filter(self, fn: Callable[[T], bool]) -> Option[T]:
        raise NotImplementedError

    @abstractmethod
    def map(self, fn: Callable[[T], U]) -> Monad[U]:
        raise NotImplementedError

    @abstractmethod
    def flatmap(self, fn: Callable[[T], Monad[U]]) -> Monad[U]:
        raise NotImplementedError

    @abstractmethod
    def is_some(self) -> bool:
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


class Some(Option[T]):
    def expect(self, msg: str) -> T:
        return self._value

    def unwrap(self) -> T:
        return self._value

    def unwrap_or(self, default: T) -> T:
        return self._value

    def and_then(self, fn: Callable[[T], Option[U]]) -> Option[U]:
        """Apply a function that returns Option to the contained value.
        
        Args:
            fn: A callable that takes the contained value (T) and returns Option[U]
        
        Returns:
            Option[U]: The result of fn if it's Some, Nothing if the result is Nothing
        
        Raises:
            TypeError: If fn does not return an Option type
        """
        value = fn(self._value)
        if not isinstance(value, Option):
            raise TypeError(
                f"and_then expects fn to return Option, got {type(value).__name__}"
            )
        return value

    def or_else(self, fn: Callable[[], Option[U]]) -> Option[Any]:
        return self

    def inspect(self, fn: Callable[[T], None]) -> Option[T]:
        fn(self._value)
        return self
    
    def is_some_and(self, fn: Callable[[T], bool]) -> bool:
        return fn(self._value)
    
    def ok_or(self, err: E) -> Result[T, E]:
        return Ok(self._value)
    
    def filter(self, fn: Callable[[T], bool]) -> Option[T]:
        if fn(self._value):
            return self
        return Nothing()

    def map(self, fn: Callable[[T], U]) -> Monad[U]:
        return Some(fn(self._value))

    def flatmap(self, fn: Callable[[T], Monad[U]]) -> Monad[U]:
        return fn(self._value)

    def is_some(self) -> bool:
        return True

    def is_nothing(self) -> bool:
        return False

    def __bool__(self) -> bool:
        return True

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Some):
            return self._value == other._value
        return False

    def __rshift__(self, fn: Callable[[T], Monad[U]]) -> Monad[U]:
        return fn(self._value)

    def __repr__(self) -> str:
        return f'Option::Some({self._value!r})'


class Nothing(Option[Any]):
    _instance: Nothing | None = None

    def __new__(cls) -> Nothing:
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self) -> None:
        # Use instance-level flag to track if this specific instance was initialized
        # This prevents re-initialization even if _initialized flag is reset externally
        flag = getattr(self, '_nothing_initialized', False)
        if not flag:
            super().__init__(Ellipsis)
            self._nothing_initialized = True

    def expect(self, msg: str):
        raise Exception(msg)

    def unwrap(self):
        raise Exception('called `Option::unwrap()` on a `Nothing` value')

    def unwrap_or(self, default: T) -> T:
        return default

    def and_then(self, fn: Callable[[Any], Option[U]]) -> Option[Any]:
        return self

    def or_else(self, fn: Callable[[], Option[U]]) -> Option[U]:
        return fn()
    
    def inspect(self, fn: Callable[[T], None]) -> Option[T]:
        return self
    
    def is_some_and(self, fn: Callable[[T], bool]) -> bool:
        return False
    
    def ok_or(self, err: E) -> Result[T, E]:
        return Err(err)

    def filter(self, fn: Callable[[T], bool]) -> Option[T]:
        return self

    def map(self, fn: Callable[[T], U]) -> Monad[Any]:
        return self

    def flatmap(self, fn: Callable[[T], Monad[U]]) -> Monad[Any]:
        return self
    
    def is_some(self) -> bool:
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
        return 'Option::Nothing'


Nothing()


from .result import Result, Ok, Err
