# RustyMonad
Rust 风格的 Python Monad 工具库

## 📖 简介

RustyMonad 是一个 Python 包，将 Rust 强大的错误处理模式引入 Python。它提供受 Rust 标准库启发的 `Option` 和 `Result` 类型，支持函数式编程模式和显式错误处理。

## ✨ 核心特性

| 特性 | 描述 |
|------|------|
| **Option 类型** | 处理可选值（Some / Nothing） |
| **Result 类型** | 处理成功/失败结果（Ok / Err） |
| **链式操作** | `map`、`flatmap`、`and_then`、`or_else` |
| **Do-Notation** | 线性风格的Monad绑定语法 |
| **Try-装饰器** | 自动将函数转换为 Result 类型 |
| **模式匹配** | Python 3.10+ match-case 支持 |
| **比较运算** | 支持 `<`、`<=`、`>`、`>=` |
| **哈希支持** | 可用于集合和字典键 |
| **复制支持** | `__copy__` / `__deepcopy__` |
| **类型注解** | 完整的泛型支持，兼容 mypy |

## 🚀 快速开始

### 安装

```bash
pip install rustymonad
```

建议使用 Python 3.10+ 以支持模式匹配功能。

### 基本用法

```python
from rustymonad import Option, Some, Nothing, Result, Ok, Err

# Option 示例
value: Option[int] = Some(42)
empty: Option[int] = Nothing()

result = value.unwrap()        # 42
result = empty.unwrap_or(0)    # 0

# Result 示例
def divide(a: int, b: int) -> Result[int, str]:
    if b == 0:
        return Err("division by zero")
    return Ok(a // b)

result = divide(10, 2)
result.unwrap()               # 5
```

---

## 📚 详细文档

### [📖 用户指南](docs/guide.md)
- 安装和配置
- 核心概念介绍
- 最佳实践

### [📖 API 参考](docs/api.md)
- 完整的 API 文档
- 类型注解说明
- 方法列表

### [📖 性能测试报告](BENCHMARK_RESULTS.md)
- 性能基准测试结果
- 普通代码 vs rustymonad 对比

---

## 📖 Option 类型详解

`Option[T]` 表示一个可能存在也可能不存在的值：

### 创建 Option

```python
from rustymonad import Option, Some, Nothing

# 包含值
some_val: Option[int] = Some(42)
some_str: Option[str] = Some("hello")
some_list: Option[list] = Some([1, 2, 3])

# 空值
empty: Option[int] = Nothing()
```

### 安全取值

```python
# unwrap - 取出值，如果为空则抛出异常
value = Some(42).unwrap()        # 42
# Nothing().unwrap()  # 抛出 UnwrapOptionError

# unwrap_or - 提供默认值
value = Some(42).unwrap_or(0)    # 42
value = Nothing().unwrap_or(0)   # 0

# unwrap_err - Option 没有此方法
```

### 链式操作

```python
from rustymonad import Some, Nothing

# map - 转换包含的值
result = Some(10).map(lambda x: x * 2)   # Some(20)
result = Nothing().map(lambda x: x * 2)  # Nothing

# and_then - 链式调用返回 Option 的函数
result = Some(5).and_then(lambda x: Some(x * 2))   # Some(10)
result = Some(5).and_then(lambda x: Nothing())     # Nothing

# or_else - 空值时提供替代值
result = Nothing().or_else(lambda: Some(0))   # Some(0)
result = Some(42).or_else(lambda: Some(0))   # Some(42)

# filter - 根据条件过滤
result = Some(10).filter(lambda x: x > 5)   # Some(10)
result = Some(3).filter(lambda x: x > 5)    # Nothing

# inspect - 调试时查看值（不修改）
Some(42).inspect(lambda x: print(f"debug: {x}"))  # 打印: debug: 42
```

### 模式匹配

```python
from rustymonad import Some, Nothing

def describe(opt: Option[str]) -> str:
    match opt:
        case Some(s) if len(s) > 10:
            return "长字符串"
        case Some(s):
            return f"字符串: {s}"
        case Nothing():
            return "无值"
```

### 比较运算

```python
from rustymonad import Some, Nothing

# Some 之间比较
assert Some(1) < Some(2)       # 值小的更小
assert Some(1) <= Some(1)     # 相等
assert Some(2) > Some(1)      # 值大的更大
assert Some(1) >= Some(1)      # 相等

# Some vs Nothing - Some 总是更大
assert Some(1) > Nothing()
assert Nothing() < Some(1)

# 类型不兼容时抛出 TypeError
# Some(1) < "string"  # TypeError
```

### 哈希支持

```python
from rustymonad import Some, Nothing

# Some 的哈希值是包含值的哈希
hash(Some(42))        # 等于 hash(42)
hash(Some("hello"))   # 等于 hash("hello")

# Nothing 的哈希值是 hash(None)
hash(Nothing())        # 等于 hash(None)

# 可用于集合和字典
seen = {Some(1), Some(2), Some(1)}  # {Some(1), Some(2)}
value_map = {Some(10): "ten"}        # 可作为字典键
```

---

## 📖 Result 类型详解

`Result[T, E]` 表示操作的成功或失败：

### 创建 Result

```python
from rustymonad import Result, Ok, Err

# 成功结果
ok_val: Result[int, str] = Ok(42)
ok_str: Result[str, str] = Ok("success")

# 错误结果
err_val: Result[int, str] = Err("error message")
err_exc: Result[int, Exception] = Err(ValueError("invalid input"))
```

### 安全取值

```python
# unwrap - 取出成功值，失败则抛出异常
value = Ok(42).unwrap()           # 42
# Err("error").unwrap()  # 抛出 UnwrapError

# unwrap_or - 失败时提供默认值
value = Ok(42).unwrap_or(0)       # 42
value = Err("error").unwrap_or(0)  # 0

# unwrap_err - 取出错误值，成功则抛出异常
error = Err("oops").unwrap_err()  # "oops"
# Ok(42).unwrap_err()  # 抛出 UnwrapError

# expect - 类似 unwrap，但可以自定义错误消息
value = Ok(42).expect("should be ok")  # 42
# Err("oops").expect("should be ok")   # 抛出 ExpectError: should be ok
```

### 链式操作

```python
from rustymonad import Ok, Err

# map - 转换成功值
result = Ok(10).map(lambda x: x * 2)   # Ok(20)
result = Err("error").map(lambda x: x * 2)  # Err("error") - 短路

# map_err - 转换错误值
result = Err("error").map_err(lambda e: f"Error: {e}")  # Err("Error: error")

# and_then - 链式调用返回 Result 的函数
result = Ok(5).and_then(lambda x: Ok(x * 2))   # Ok(10)
result = Ok(5).and_then(lambda x: Err("fail"))  # Err("fail")

# or_else - 错误时提供替代结果
result = Err("error").or_else(lambda e: Ok(0))   # Ok(0)
result = Ok(42).or_else(lambda e: Ok(0))         # Ok(42)

# inspect / inspect_err - 调试查看
Ok(42).inspect(lambda x: print(f"success: {x}"))
Err("error").inspect_err(lambda e: print(f"failed: {e}"))
```

### 类型检查

```python
from rustymonad import Ok, Err

# is_ok / is_err
Ok(42).is_ok()      # True
Ok(42).is_err()     # False
Err("error").is_ok()   # False
Err("error").is_err()  # True

# is_ok_and / is_err_and - 带条件
Ok(100).is_ok_and(lambda x: x > 50)   # True
Ok(10).is_ok_and(lambda x: x > 50)    # False
Err("error").is_err_and(lambda e: "not found" in e)  # True
```

### 转换方法

```python
from rustymonad import Ok, Err

# ok() - 转换为 Option
Ok(42).ok()   # Some(42)
Err("error").ok()  # Nothing

# err() - 转换为 Option
Ok(42).err()   # Nothing
Err("error").err()  # Some("error")

# ok_or - 带错误消息转换为 Option
Ok(42).ok_or("no value")   # Some(42)
Err("error").ok_or("no value")  # Nothing
```

### 比较运算

```python
from rustymonad import Ok, Err

# Ok 之间比较
assert Ok(1) < Ok(2)
assert Ok(1) <= Ok(1)
assert Ok(2) > Ok(1)
assert Ok(1) >= Ok(1)

# Err 之间比较
assert Err('a') < Err('b')
assert Err('b') > Err('a')

# Ok vs Err - Ok 总是更小（表示成功优先）
assert Ok(1) < Err("error")
assert Err("error") > Ok(1)
```

### 模式匹配

```python
from rustymonad import Ok, Err

def process(result: Result[int, str]) -> str:
    match result:
        case Ok(x) if x > 100:
            return "大数字"
        case Ok(x):
            return f"数字: {x}"
        case Err(e):
            return f"错误: {e}"
```

---

## 🔗 Do-Notation（do 语法糖）

用线性风格编写顺序操作：

```python
from rustymonad import Result, Ok, Err, DoRet, do_notation

@do_notation
def calculate(a: float, b: float) -> DoRet[Result[float, str]]:
    """计算 sqrt(a) / b，带错误处理。"""
    root = yield Ok(a ** 0.5)       # 开平方
    quotient = yield Ok(root / b)    # 除法
    return Ok(quotient)

# 使用
calculate(16, 4)   # Ok(1.0)
calculate(-1, 4)   # Ok(0.5)
```

---

## 🎯 Try-装饰器

自动将函数转换为返回 Result：

```python
from rustymonad import try_notation

@try_notation
def parse_int(s: str) -> int:
    return int(s)

# 使用
parse_int("42")    # Ok(42)
parse_int("abc")   # Err("invalid literal for int()...")
```

---

## 📊 性能对比

| 场景 | 普通 Python | rustymonad | 开销 |
|------|-------------|------------|------|
| 流水线计算 | ~237 ns | ~2,289 ns | ~9.7x |
| None 短路 | ~126 ns | ~644 ns | ~5.1x |
| 安全除法 | ~261 ns | ~1,655 ns | ~6.3x |

详细对比：[BENCHMARK_RESULTS.md](BENCHMARK_RESULTS.md)

---

## 🛠️ 开发

### 运行测试

```bash
pytest tests/ -v
```

### 运行基准测试

```bash
pytest tests/test_benchmark.py --benchmark-only
```

### 代码风格

```bash
ruff check src/
ruff check tests/
```

---

## 📄 许可证

MIT License - 详见 [LICENSE](LICENSE) 文件。

---

## 🤝 贡献

欢迎贡献！请阅读 [CONTRIBUTING.md](CONTRIBUTING.md) 了解详情。
