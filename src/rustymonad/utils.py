from functools import wraps, reduce
from typing import TypeVar, Callable, Generator, Any, TypeAlias
from typing_extensions import ParamSpec
from types import GeneratorType
from .monad import Monad
from .result import Result, Ok, Err


P = ParamSpec('P')
M = TypeVar('M', bound=Monad)
T = TypeVar('T')


def do_notation(func: Callable[P, Generator[Monad, Any, M]]) -> Callable[P, M]:
    @wraps(func)
    def _wrapper(*args: P.args, **kwargs: P.kwargs) -> M:
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


DoRet: TypeAlias = Generator[Monad, Any, T]


def try_notation(func: Callable[P, T]) -> Callable[P, Result[T, str]]:
    @wraps(func)
    def _wrapper(*args: P.args, **kwargs: P.kwargs) -> Result[T, str]:
        try:
            return Ok(func(*args, **kwargs))
        except Exception as e:
            return Err(str(e))
    return _wrapper
