from functools import wraps
from typing import TypeVar, Callable, Generator, TypeAlias, ParamSpec, Any
from types import GeneratorType
from .monad import Monad
from .result import Result, Ok, Err
from .errors import DoNotationError


P = ParamSpec('P')
TUtils = TypeVar('TUtils')
MUtils = TypeVar('MUtils', bound=Monad)
DoRet: TypeAlias = Generator[Monad, Any, MUtils]


def do_notation(func: Callable[P, DoRet[MUtils]]) -> Callable[P, MUtils]:
    """Decorator that implements do-notation for monads.

    Args:
        func: A generator function that yields monadic values.

    Returns:
        A wrapped function that executes the do-notation block.

    Raises:
        TypeError: If the function doesn't return a generator or if a yielded
            value is not a Monad type.
        DoNotationError: If an error occurs during do-notation execution.
    """
    @wraps(func)
    def _wrapper(*args: P.args, **kwargs: P.kwargs) -> MUtils:
        generator = func(*args, **kwargs)
        if isinstance(generator, GeneratorType):
            monad = Monad(None)
            while True:
                try:
                    result = monad.flatmap(generator.send)
                    if not isinstance(result, Monad):
                        raise TypeError(
                            f"Expected a Monad type from yield, but got {type(result).__name__}. "
                            f"Ensure all yielded values are monads (e.g., Ok(...), Err(...), Some(...), Nothing)."
                        )
                    elif (not result) or (result is monad):
                        return result  # type: ignore
                    monad = result
                except StopIteration as e:
                    return e.value
                except DoNotationError:
                    raise
                except Exception as e:
                    # Get line number from generator frame if available
                    line_no = "unknown"
                    try:
                        if generator.gi_frame and hasattr(generator.gi_frame, 'f_lineno'):
                            line_no = generator.gi_frame.f_lineno
                    except Exception:
                        pass
                    raise DoNotationError(
                        f"Error in do-notation (around line {line_no}): {str(e)}",
                        original_error=e
                    ) from e
        else:
            raise TypeError(
                f"do-notation requires a generator function, but got {type(generator).__name__}. "
                f"Ensure '@do_notation' is applied to a function that uses 'yield' statements."
            )
    return _wrapper


def try_notation(func: Callable[P, TUtils]) -> Callable[P, Result[TUtils, str]]:
    """Decorator that wraps a function to return a Result.

    This decorator catches all exceptions and returns them as Err values,
    enabling error handling without try/except blocks.

    Args:
        func: The function to wrap.

    Returns:
        A wrapper function that returns Ok(result) on success,
        Err(exception_message) on failure.

    Example:
        >>> @try_notation
        ... def risky_divide(a: int, b: int) -> float:
        ...     return a / b
        >>> risky_divide(10, 2)
        Result::Ok(5.0)
        >>> risky_divide(10, 0)
        Result::Err('division by zero')
    """
    @wraps(func)
    def _wrapper(*args, **kwargs) -> Result[TUtils, str]:
        try:
            return Ok(func(*args, **kwargs))
        except Exception as e:
            return Err(str(e))
    return _wrapper

