from functools import wraps
from typing import TypeVar, Callable, Generator, TypeAlias, Any
from types import GeneratorType
from .monad import Monad
from .result import Result, Ok, Err


T = TypeVar('T')
DoRet: TypeAlias = Generator[Monad, Any, T]


def do_notation(func: Callable[..., DoRet[Monad]]) -> Callable[..., Monad]:
    @wraps(func)
    def _wrapper(*args, **kwargs) -> Monad:
        generator = func(*args, **kwargs)
        if isinstance(generator, GeneratorType):
            monad = Monad(None)
            while True:
                try:
                    result = monad.flatmap(generator.send)
                    if not isinstance(result, Monad):
                        raise TypeError(f'Expected monad type, got {type(result)}')
                    elif (not result) or (result is monad):
                        return result  # type: ignore
                    monad = result
                except StopIteration as e:
                    return e.value
        else:
            raise TypeError('do-notation expected a generator')
    return _wrapper


def try_notation(func: Callable[..., T]) -> Callable[..., Result[T, str]]:
    @wraps(func)
    def _wrapper(*args, **kwargs) -> Result[T, str]:
        try:
            return Ok(func(*args, **kwargs))
        except Exception as e:
            return Err(str(e))
    return _wrapper
