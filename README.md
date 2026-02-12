# RustyMonad

Rust-Style Monad Utilities for Python

## Overview

RustyMonad is a Python package that brings Rust's powerful error handling patterns to Python. It provides `Option` and `Result` types inspired by Rust's standard library, enabling functional programming patterns with explicit error handling.

## Core Types

### Option[T] - Handling Optional Values

The `Option` type represents a value that may or may not exist:

- **`Some[T]`** - Contains a value
- **`Nothing`** - Represents the absence of a value (singleton)

```python
from rustymonad import Option, Some, Nothing

# Creating Option values
value: Option[int] = Some(42)
empty: Option[int] = Nothing()

# Safe access with unwrap_or
result = empty.unwrap_or(0)  # Returns 0

# Pattern matching
match value:
    case Some(x):
        print(f"Got value: {x}")
    case Nothing():
        print("No value")
```

### Result[T, E] - Handling Success and Failure

The `Result` type represents either success or failure:

- **`Ok[T]`** - Contains a success value
- **`Err[E]`** - Contains an error value

```python
from rustymonad import Result, Ok, Err

def divide(a: int, b: int) -> Result[int, str]:
    if b == 0:
        return Err("division by zero")
    return Ok(a // b)

# Using Result
result = divide(10, 2)
result.unwrap()  # Returns 5

failed = divide(10, 0)
failed.unwrap_err()  # Returns "division by zero"
```

## Key Features

### 1. Monadic Operations

Chain operations safely with `map`, `flatmap`, `and_then`, and `or_else`:

```python
from rustymonad import Ok, Err, Some, Nothing

# Chaining operations on Ok
chained = (
    Ok(10)
    .map(lambda x: x * 2)          # Ok(20)
    .and_then(lambda x: Ok(x + 1)) # Ok(21)
    .or_else(lambda e: Ok(0))      # Ok(21) - not called
)

# Short-circuit on Err
shortcut = (
    Err("error")
    .map(lambda x: x * 2)          # Err("error") - not called
    .unwrap_or(0)                   # Returns 0
)

# Option chaining
opt_chained = (
    Some(5)
    .map(lambda x: x * 2)           # Some(10)
    .and_then(lambda x: Some(x + 1))# Some(11)
    .unwrap_or(0)                   # Returns 11
)

# Nothing short-circuits
nothing_chained = (
    Nothing()
    .map(lambda x: x * 2)           # Nothing
    .unwrap_or(42)                  # Returns 42
)
```

### 2. Do-Notation (Monadic Bind Syntax)

Write sequential operations in a linear style using the `@do_notation` decorator:

```python
from rustymonad import Result, Ok, Err, DoRet, do_notation

@do_notation
def calculate(a: float, b: float) -> DoRet[Result[float, str]]:
    """Calculate sqrt(a) / b with proper error handling."""
    root = yield Ok(a ** 0.5)       # Square root
    quotient = yield Ok(root / b)   # Division
    return Ok(quotient)

# Usage
calculate(16, 4)  # Ok(1.0)
calculate(-1, 4) # Ok(0.5) - works with Ok wrapper
```

### 3. Try-Decorator

Automatically convert functions to return `Result`:

```python
from rustymonad import Result, try_notation

@try_notation
def parse_int(s: str) -> int:
    return int(s)

parse_int("42")   # Ok(42)
parse_int("abc")  # Err("invalid literal for int() with base 10: 'abc'")
```

### 4. Pattern Matching with match-case

Python 3.10+ structural pattern matching:

```python
from rustymonad import Ok, Err, Some, Nothing

def process(value: Result[int, str]) -> str:
    match value:
        case Ok(x) if x > 100:
            return "large number"
        case Ok(x):
            return f"number: {x}"
        case Err(e):
            return f"error: {e}"
        case _:
            return "unexpected"

# Option pattern matching
def describe(opt: Option[str]) -> str:
    match opt:
        case Some(s) if len(s) > 10:
            return "long string"
        case Some(s):
            return f"string: {s}"
        case Nothing():
            return "no value"
```

### 5. Error Handling with Custom Exceptions

```python
from rustymonad import (
    Ok, Err,
    UnwrapError,
    ExpectError,
    UnwrapOptionError,
    ExpectOptionError
)

# Safe unwrap with defaults
result = Ok(42).unwrap_or(0)  # 42
result = Err("oops").unwrap_or(0)  # 0

# Expect with custom messages
result = Ok(42).expect("should have value")  # 42
# result = Err("oops").expect("should have value")  # Raises ExpectError

# Option-specific errors
some_val = Some(42).unwrap()  # 42
# nothing = Nothing().unwrap()  # Raises UnwrapOptionError
```

### 6. Error Mapping and Transformation

```python
from rustymonad import Ok, Err

# Transform errors
error_transformed = (
    Err("file not found")
    .map_err(lambda e: f"IO Error: {e}")  # Err("IO Error: file not found")
)

# Recover from errors
recovered = (
    Err("initial error")
    .or_else(lambda e: Ok("recovered"))  # Ok("recovered")
)

# Conditional checks
is_large = Ok(100).is_ok_and(lambda x: x > 50)  # True
is_err = Err("error").is_err_and(lambda e: "not found" in e)  # True
```

### 7. Copy Support

All monadic types support shallow and deep copying:

```python
from rustymonad import Ok, Some

# Shallow copy
original = Ok([1, 2, 3])
copied = original.__copy__()
copied.unwrap().append(4)
original.unwrap()  # [1, 2, 3, 4] - original affected (shallow)
copied.unwrap()   # [1, 2, 3, 4]

# Deep copy
deep = original.__deepcopy__()
deep.unwrap().append(5)
original.unwrap()  # [1, 2, 3, 4] - original not affected
deep.unwrap()      # [1, 2, 3, 4, 5]
```

### 8. Hash Support

All monadic types are hashable, allowing use in sets and as dictionary keys:

```python
from rustymonad import Ok, Err, Some, Nothing

# Hash Some values
some_hashable = Some(42)
hash(some_hashable)  # Returns hash of the wrapped value
hash(Some("hello"))  # Returns hash of "hello"

# Hash Nothing
nothing_hash = hash(Nothing())  # Returns hash(None)

# Use in sets and dicts
seen = {Some(1), Some(2), Some(1)}  # {Some(1), Some(2)}
value_map = {Some(10): "ten"}       # Can use as dict key
```

### 9. Comparison Operations

Compare `Option` and `Result` types using standard comparison operators:

```python
from rustymonad import Ok, Err, Some, Nothing

# Option comparisons
assert Some(1) < Some(2)      # Some with smaller value is less
assert Some(1) <= Some(1)      # Equal values are equal
assert Some(2) > Some(1)       # Some with larger value is greater
assert Some(1) >= Some(1)      # Equal values are equal

# Some vs Nothing - Some is always greater
assert Some(1) > Nothing()
assert Nothing() < Some(1)

# Result comparisons - Ok vs Ok
assert Ok(1) < Ok(2)
assert Ok(1) <= Ok(1)
assert Ok(2) > Ok(1)
assert Ok(1) >= Ok(1)

# Result comparisons - Err vs Err
assert Err('a') < Err('b')
assert Err('b') > Err('a')

# Result comparisons - Ok vs Err
# Ok is always less than Err (Ok is preferred/success state)
assert Ok(1) < Err("error")
assert Err("error") > Ok(1)

# TypeError for incompatible comparisons
# Comparing with incompatible types raises TypeError
# Some(1) < "string"  # Raises TypeError
```

### 10. Operator Overloading

Use the `>>` operator for chaining:

```python
from rustymonad import Ok, Some

# Operator chaining
result = (
    Ok(5)
    >> (lambda x: Ok(x * 2))    # Ok(10)
    >> (lambda x: Ok(x + 1))    # Ok(11)
    >> (lambda x: Ok(x))        # Ok(11)
)
```

## API Reference

### Monad Methods

| Method | Description |
|--------|-------------|
| `map(fn)` | Transform the contained value |
| `flatmap(fn)` | Apply a function that returns a Monad |
| `unwrap()` | Extract the contained value |
| `__rshift__(fn)` | Bind operation via `>>` operator |

### Option Methods

| Method | Description |
|--------|-------------|
| `unwrap_or(default)` | Return value or default |
| `and_then(fn)` | Chain operations that return Option |
| `or_else(fn)` | Provide alternative if Nothing |
| `ok_or(err)` | Convert to Result |
| `filter(pred)` | Keep only if predicate matches |

### Result Methods

| Method | Description |
|--------|-------------|
| `unwrap_or(default)` | Return Ok value or default |
| `unwrap_err()` | Extract error value |
| `map_err(fn)` | Transform the error value |
| `and_then(fn)` | Chain operations that return Result |
| `or_else(fn)` | Recover from error |
| `is_ok()`, `is_err()` | Type checks |
| `ok()`, `err()` | Convert to Option |

## Type Annotations and IDE Support

RustyMonad is fully typed with complete generics support:

```python
from rustymonad import Result, Ok, Err, Option, Some

# Generic type parameters
def process() -> Result[str, ValueError]:
    return Ok("success")

# Complex chaining with type safety
def pipeline(x: int) -> Result[int, str]:
    return (
        Ok(x)
        .map(lambda n: n * 2)
        .and_then(lambda n: Ok(n + 1) if n > 0 else Err("negative"))
    )

# Using with mypy
reveal_type(pipeline(5))  # Result[int, str]
```

## Installation

```bash
pip install rustymonad
```

For Python 3.10+ to use pattern matching features.

## Performance

RustyMonad includes optimizations for performance-critical code:

- `__slots__` for memory efficiency
- No external dependencies
- Singleton pattern for `Nothing`
- Copy-on-write semantics where applicable

## Contributing

Contributions are welcome! Please read the contributing guidelines before submitting PRs.

## License

MIT License - see the LICENSE file for details.
