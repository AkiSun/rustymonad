from typing import Generic, TypeVar, Callable


T = TypeVar('T')
U = TypeVar('U')


class Monad(Generic[T]):
    __match_args__ = ('_value',)

    def __init__(self, value: T):
        self._value = value

    def unwrap(self) -> T:
        return self._value

    def map[U](self, fn: Callable[[T], U]) -> 'Monad[U]':
        return Monad(fn(self._value))

    def flatmap[U](self, fn: Callable[[T], 'Monad[U]']) -> 'Monad[U]':
        return fn(self._value)

    def __bool__(self) -> bool:
        return True

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Monad):
            return self._value == other._value
        return False

    def __repr__(self) -> str:
        return f'Monad({self._value.__repr__()})'
