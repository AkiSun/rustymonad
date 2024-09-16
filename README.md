# RustyMonad

Rust-Style Monad Utilities for Python

## Getting Started

### Introduction

RustyMonad is a Python package designed to incorporate a Rust-style exception handling mechanisms into Python programming. This approach not only simplifies code and also enhances its readability and maintainability.

### Features

- **Rust-style Exception Handling**: Based on Monad's `Option` and `Result` modules, it provides a mechanism similar to Rust's exception handling
- **Do-Notation Syntax Sugar**: Supports decorators to simplify monadic operations
- **Match-Case Statement Support**: Supports pattern matching using match-case statements
- **Complete Type Annotations**: Includes full type annotations and supports generics (use `mypy` for type checking)
- **No External Dependencies**: The package does not rely on external dependencies, making it lightweight and easy to integrate

### Installation

RustyMonad is available on PyPI:

```bash
python -m pip install RustyMonad
```

For optimal user experience, it is recommended to use Python 3.10 or higher to support the use of `match-case` statements.

### Usage Example

```python
from rustymonad import Result, Ok, Err, DoRet, do_notation


def safe_div(x: float, y: float) -> Result[float, str]:
    if y == 0:
        return Err('division by zero')
    return Ok(x / y)


def safe_sqrt(x: float) -> Result[float, str]:
    if x < 0:
        return Err('square root of a negative number')
    return Ok(math.sqrt(x))


@do_notation
def calc_process(a: float, b: float) -> DoRet[Result[float, str]]:
    root = yield safe_sqrt(a)
    quotient = yield safe_div(root, b)
    return Ok(quotient)


assert calc_process(9, 2) == Ok(1.5)
assert calc_process(9, 0) == Err('division by zero')


match calc_process(9, 2):
    case Ok(result):
        print(f'call calc_process() successful. {result = }')
    case Err(error):
        print(f'call calc_process() failed. {error = }')
```

### More Examples

#### Option

`Option[T]` is used to represent an optional(nullable) value, typically used for type declarations. `Option[T]` can either contain a value `Some(T)` or be empty `Nothing()`. This can replace the `Optional` type from the `typing` module. `Nothing` behaves similarly to `None` but supports branch selection or null value handling through interfaces to avoid using numerous `if` statements for null checks.

Handling null values with `Option`:

```python
from rustymonad import Option, Some, Nothing

def safe_div(x: float, y: float) -> Option[float]:
    if y == 0:
        return Nothing()
    return Some(x / y)

other_method(safe_div(1, 0).unwrap_or(0))

match safe_div(1, 2):
    case Some(x):
        print(f'result is {x}')
    case Nothing():  # Also use `case _:` for the last case statement
        print('cannot divide by 0')
```

#### Result

`Result[T, E]` is commonly used to represent the result of an operation or any exceptions generated during the operation. It is generally used for type declarations. `Result[T, E]` can either contain a success value `Ok(T)` or an error `Err(E)`.

Handling exceptions with `Result`:

```python
from rustymonad import Result, Ok, Err

def safe_div(x: float, y: float) -> Result[float, Exception]:
    try:
        return Ok(x / y)
    except Exception as e:
        return Err(e)

value = (
    safe_div(1, 2)
    .and_then(lambda x: Ok(x * x))
    .or_else(lambda e: Ok(0))
    .inspect(print)
    .unwrap()
)

match safe_div(10, 2).and_then(lambda x: Ok(int(x))):
    case Ok(v) if v % 2 == 1:
        print(f'result is a odd')
    case Ok(_):
        print('result is a even')
    case Err(e):
        print(f'something wrong with {e}')
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
