# RustyMonad API 参考

本文档提供 RustyMonad 所有公共 API 的详细说明。

---

## 目录

- [Option 类型](#option-类型)
- [Result 类型](#result-类型)
- [Do-Notation](#do-notation)
- [Try-装饰器](#try-装饰器)
- [工具函数](#工具函数)
- [异常类](#异常类)

---

## Option 类型

### 基类

```python
from rustymonad import Option, Some, Nothing
```

#### `Option[T]`

Option 抽象基类，表示可选值。

**类型参数：**
- `T`: Option 包含的值的类型

**子类：**
- `Some[T]`: 包含具体值
- `Nothing`: 空值（单例）

---

### Some[T]

包含具体值的 Option。

```python
from rustymonad import Some

# 创建 Some
some: Some[int] = Some(42)
some_str: Some[str] = Some("hello")
```

#### 方法

##### `unwrap() -> T`

取出包含的值。

```python
val = Some(42).unwrap()  # 42
# Nothing().unwrap()  # 抛出 UnwrapOptionError
```

##### `unwrap_or(default: T | U) -> T | U`

返回包含的值或默认值。

```python
val = Some(42).unwrap_or(0)   # 42
val = Some(42).unwrap_or("")   # 42
val = Nothing().unwrap_or(0)   # 0
```

##### `expect(message: str) -> T`

返回包含的值，失败时抛出带自定义消息的异常。

```python
val = Some(42).expect("should have value")  # 42
# Nothing().expect("no value")  # 抛出 ExpectOptionError: no value
```

##### `map(fn: Callable[[T], U]) -> Option[U]`

转换包含的值。

```python
result = Some(10).map(lambda x: x * 2)   # Some(20)
result = Some("hello").map(len)          # Some(5)
result = Nothing().map(lambda x: x * 2)  # Nothing
```

##### `flatmap(fn: Callable[[T], Option[U]]) -> Option[U]`

应用返回 Option 的函数。

```python
result = Some(5).flatmap(lambda x: Some(x * 2))   # Some(10)
result = Some(5).flatmap(lambda x: Nothing())     # Nothing
```

##### `and_then(fn: Callable[[T], Option[U]]) -> Option[U]`

与 `flatmap` 相同，链式调用。

```python
result = Some(5).and_then(lambda x: Some(x + 1))   # Some(6)
```

##### `or_else(fn: Callable[[], Option[T]]) -> Option[T]`

空值时提供替代 Option。

```python
result = Nothing().or_else(lambda: Some(0))   # Some(0)
result = Some(42).or_else(lambda: Some(0))   # Some(42)
```

##### `filter(pred: Callable[[T], bool]) -> Option[T]`

根据条件过滤。

```python
result = Some(10).filter(lambda x: x > 5)   # Some(10)
result = Some(3).filter(lambda x: x > 5)     # Nothing
```

##### `inspect(fn: Callable[[T], Any]) -> Option[T]`

调试时查看值（不修改）。

```python
Some(42).inspect(lambda x: print(f"debug: {x}"))  # 打印: debug: 42
```

##### `ok_or(err: E) -> Result[T, E]`

转换为 Result。

```python
result = Some(42).ok_or("no value")   # Ok(42)
result = Nothing().ok_or("no value")  # Err("no value")
```

##### `is_some() -> bool`

检查是否包含值。

```python
Some(42).is_some()   # True
Nothing().is_some()  # False
```

##### `is_nothing() -> bool`

检查是否为空。

```python
Some(42).is_nothing()  # False
Nothing().is_nothing() # True
```

##### `__hash__() -> int`

哈希值（可用于集合和字典）。

```python
hash(Some(42))   # 等于 hash(42)
hash(Nothing())  # 等于 hash(None)
```

##### 比较运算

```python
# Some 之间
Some(1) < Some(2)       # True
Some(1) <= Some(1)      # True
Some(2) > Some(1)       # True
Some(1) >= Some(1)      # True

# Some vs Nothing
Some(1) > Nothing()     # True
Nothing() < Some(1)     # True
```

---

### Nothing

空值（单例模式）。

```python
from rustymonad import Nothing

empty: Option[int] = Nothing()
```

**特性：**
- 多次调用 `Nothing()` 返回同一实例
- `Nothing() is Nothing()` 总是 `True`
- 所有链式操作都会短路返回 `Nothing`

---

## Result 类型

### 基类

```python
from rustymonad import Result, Ok, Err
```

#### `Result[T, E]`

Result 抽象基类，表示成功或失败。

**类型参数：**
- `T`: 成功值的类型
- `E`: 错误值的类型

**子类：**
- `Ok[T]`: 包含成功值
- `Err[E]`: 包含错误值

---

### Ok[T]

包含成功值的 Result。

```python
from rustymonad import Ok

ok: Ok[int] = Ok(42)
ok_str: Ok[str] = Ok("success")
```

#### 方法

##### `unwrap() -> T`

取出成功值。

```python
val = Ok(42).unwrap()  # 42
# Err("error").unwrap()  # 抛出 UnwrapError
```

##### `unwrap_or(default: T) -> T`

返回成功值或默认值。

```python
val = Ok(42).unwrap_or(0)    # 42
val = Err("error").unwrap_or(0)  # 0
```

##### `unwrap_err() -> E`

取出错误值（Ok 上抛出异常）。

```python
# Ok(42).unwrap_err()  # 抛出 UnwrapError
err = Err("error").unwrap_err()  # "error"
```

##### `expect(message: str) -> T`

返回成功值，失败时抛出带自定义消息的异常。

```python
val = Ok(42).expect("should be ok")  # 42
# Err("oops").expect("should be ok")  # 抛出 ExpectError: should be ok
```

##### `map(fn: Callable[[T], U]) -> Result[U, E]`

转换成功值。

```python
result = Ok(10).map(lambda x: x * 2)   # Ok(20)
result = Err("error").map(lambda x: x * 2)  # Err("error") - 短路
```

##### `map_err(fn: Callable[[E], F]) -> Result[T, F]`

转换错误值。

```python
result = Err("error").map_err(lambda e: f"Error: {e}")  # Err("Error: error")
```

##### `flatmap(fn: Callable[[T], Result[U, E]]) -> Result[U, E]`

应用返回 Result 的函数。

```python
result = Ok(5).flatmap(lambda x: Ok(x * 2))   # Ok(10)
result = Ok(5).flatmap(lambda x: Err("fail")) # Err("fail")
```

##### `and_then(fn: Callable[[T], Result[U, E]]) -> Result[U, E]`

与 `flatmap` 相同。

```python
result = Ok(5).and_then(lambda x: Ok(x + 1))   # Ok(6)
```

##### `or_else(fn: Callable[[E], Result[T, F]]) -> Result[T, F]`

错误时提供替代结果。

```python
result = Err("error").or_else(lambda e: Ok(0))   # Ok(0)
result = Ok(42).or_else(lambda e: Ok(0))         # Ok(42)
```

##### `inspect(fn: Callable[[T], Any]) -> Result[T, E]`

调试查看成功值。

```python
Ok(42).inspect(lambda x: print(f"success: {x}"))
```

##### `inspect_err(fn: Callable[[E], Any]) -> Result[T, E]`

调试查看错误值。

```python
Err("error").inspect_err(lambda e: print(f"failed: {e}"))
```

##### `ok() -> Option[T]`

转换为 Option。

```python
result = Ok(42).ok()   # Some(42)
result = Err("error").ok()  # Nothing
```

##### `err() -> Option[E]`

错误值转换为 Option。

```python
result = Ok(42).err()   # Nothing
result = Err("error").err()  # Some("error")
```

##### `is_ok() -> bool`

检查是否成功。

```python
Ok(42).is_ok()     # True
Err("error").is_ok()  # False
```

##### `is_err() -> bool`

检查是否失败。

```python
Ok(42).is_err()    # False
Err("error").is_err()  # True
```

##### `is_ok_and(pred: Callable[[T], bool]) -> bool`

成功且满足条件。

```python
Ok(100).is_ok_and(lambda x: x > 50)   # True
Ok(10).is_ok_and(lambda x: x > 50)      # False
```

##### `is_err_and(pred: Callable[[E], bool]) -> bool`

失败且满足条件。

```python
Err("not found").is_err_and(lambda e: "not found" in e)  # True
```

##### `__hash__() -> int`

哈希值（Ok 的哈希基于包含的值）。

```python
hash(Ok(42))    # 等于 hash(42)
hash(Err("e"))  # 等于 hash("e")
```

##### 比较运算

```python
# Ok 之间
Ok(1) < Ok(2)       # True
Ok(1) <= Ok(1)      # True
Ok(2) > Ok(1)       # True
Ok(1) >= Ok(1)      # True

# Err 之间
Err('a') < Err('b')     # True
Err('b') > Err('a')     # True

# Ok vs Err - Ok 总是更小
Ok(1) < Err("error")    # True
Err("error") > Ok(1)    # True
```

---

### Err[E]

包含错误值的 Result。

```python
from rustymonad import Err

err: Err[str] = Err("error message")
err_exc: Err[Exception] = Err(ValueError("invalid"))
```

**所有方法与 Ok 类似，但操作在错误值上：**
- `map` / `flatmap` / `and_then` 会短路返回自身
- `map_err` 转换错误值
- `or_else` 可以恢复错误

---

## Do-Notation

### 装饰器

```python
from rustymonad import do_notation, DoRet
```

#### `@do_notation`

将函数转换为支持 `yield` 的 do-notation 风格。

```python
from rustymonad import Result, Ok, Err, DoRet, do_notation

@do_notation
def process(a: float, b: float) -> DoRet[Result[float, str]]:
    root = yield Ok(a ** 0.5)
    quotient = yield Ok(root / b)
    return Ok(quotient)

# 使用
result = process(16, 4)  # Ok(1.0)
```

**类型注解：**
- 返回类型必须写作 `DoRet[Result[T, E]]`
- `yield` 后面必须跟 `Ok(...)` 或 `Err(...)`
- 最终 `return` 必须是 `Ok(...)`

---

## Try-装饰器

### `@try_notation`

自动捕获异常并返回 Result。

```python
from rustymonad import try_notation

@try_notation
def parse_int(s: str) -> int:
    return int(s)

# 使用
parse_int("42")   # Ok(42)
parse_int("abc")  # Err("invalid literal for int()...")
```

---

## 工具函数

### `DoRet`

Do-notation 的返回类型标记（用于类型注解）。

```python
from rustymonad import DoRet

@do_notation
def example() -> DoRet[Result[int, str]]:
    value = yield Ok(42)
    return Ok(value)
```

---

## 异常类

### 基类

```python
from rustymonad import (
    RustyMonadError,
    UnwrapError,
    ExpectError,
    UnwrapOptionError,
    ExpectOptionError
)
```

#### `RustyMonadError`

所有 rustymonad 异常的基类。

```python
try:
    ...
except RustyMonadError:
    ...
```

#### `UnwrapError`

在 Result 上调用 `unwrap()` 但结果为 Err 时抛出。

```python
from rustymonad import Err, UnwrapError

try:
    Err("error").unwrap()
except UnwrapError as e:
    print(e)  # "Tried to unwrap an Err value: 'error'"
```

#### `ExpectError`

在 Result 上调用 `expect()` 但结果为 Err 时抛出。

```python
from rustymonad import Err, ExpectError

try:
    Err("error").expect("custom message")
except ExpectError as e:
    print(e)  # "custom message: 'error'"
```

#### `UnwrapOptionError`

在 Option 上调用 `unwrap()` 但结果为 Nothing 时抛出。

```python
from rustymonad import Nothing, UnwrapOptionError

try:
    Nothing().unwrap()
except UnwrapOptionError as e:
    print(e)  # "Tried to unwrap a Nothing value"
```

#### `ExpectOptionError`

在 Option 上调用 `expect()` 但结果为 Nothing 时抛出。

```python
from rustymonad import Nothing, ExpectOptionError

try:
    Nothing().expect("custom message")
except ExpectOptionError as e:
    print(e)  # "custom message"
```

---

## 类型注解示例

### 泛型用法

```python
from rustymonad import Result, Ok, Err, Option, Some, Nothing

# Result 泛型
def process() -> Result[str, ValueError]:
    return Ok("success")

# Option 泛型
def maybe_value() -> Option[int]:
    return Some(42)

# 链式调用保持类型安全
def pipeline(x: int) -> Result[int, str]:
    return (
        Ok(x)
        .map(lambda n: n * 2)
        .and_then(lambda n: Ok(n + 1) if n > 0 else Err("negative"))
    )
```

### 与 mypy/Pyright 配合

```python
from rustymonad import Result, Ok, Err

def process() -> Result[int, str]:
    return Ok(42)

# mypy 会推断出 Result[int, str]
reveal_type(process())  # Result[int, str]
```
