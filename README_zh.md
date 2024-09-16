# RustyMonad
Rust-style Monad utils for Python

## 快速开始
### 简介
RustyMonad是一个Python包，旨在将类似Rust风格的异常处理机制引入到Python编程中。这种方法不仅简化了代码，还增强了其可读性和可维护性。

### 特性
- Rust风格的异常处理：基于Monad的`Option`和`Result`模块，提供了一种类似于Rust语言中错误处理机制的方法
- do-notation语法糖：支持装饰器来简化Monad操作的编写
- 支持match-case语句：支持match-case语句的模式匹配功能
- 完整的类型注解：包含全面的类型注解信息和泛型支持，并支持使用mypy来进行类型检查
- 无外部依赖：这个包是独立的，没有外部依赖，轻量且易于集成

### 安装
RustyMonad可以通过pip工具进行安装（来自PyPI）:
```bash
$ python -m pip install RustyMonad
```
为了获得良好的使用体验，建议使用Python 3.10及更高版本，以支持对match-case语句的使用。

### 使用示例
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

### 更多示例
#### Option
`Option[T]`用来表示一个可选(可空)的值，它是一个抽象类，一般用于类型声明。`Option[T]`可以是一个包含具体值的`Some(T)`，或者是不包含任何值的`Nothing()`。Option可以用于替换typing模块的Optional，Nothing类似于None，但与之不同的是它支持通过接口来进行分支选择或空值处理，以避免使用大量if语句进行空值检查。

使用Option处理空值：
```python
def safe_div(x: float, y: float) -> Option[float]:
    if y == 0:
        return Nothing()
    return Some(x / y)

other_method(safe_div(1, 0).unwrap_or(0))

match safe_div(1, 2):
    case Some(x):
        print(f'result is {x}')
    case Nothing():  # also use `case _:` at last case statement
        print('cannot divide by 0')
```

#### Result
`Result[T, E]`通常用来表示一个操作的返回值或是操作中产生的异常，它是一个抽象类，一般用于类型声明。`Result[T, E]`可以是一个包含成功值的`Ok(T)`，或者包含异常的`Err(E)`。

使用Result处理异常：
```python
def safe_div(x: float, y: float) -> Result[float, Exception]:
    try:
        return Ok(x / y)
    expect Exception as e:
        return Err(e)

value = (
    safe_div(1, 2)
    .and_then(lambda x: Ok(x * x))
    .or_else(lambda e: Ok(0))
    .inspect(print)
    .unwrap()
)

match safe_div(10, 2).map(int):
    case Ok(x) if x % 2 == 1:
        print(f'result is a odd')
    case Ok(_):
        print('result is a even')
    case Err(e):
        print('cannot divide by 0')
```

## 许可证
本项目依据 MIT 许可证发布——请参见[LICENSE](LICENSE)文件了解详细信息。
