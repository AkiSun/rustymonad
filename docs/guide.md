# RustyMonad 入门指南

本指南帮助你快速上手 RustyMonad，理解核心概念并掌握最佳实践。

---

## 目录

1. [为什么使用 RustyMonad？](#为什么使用-rustymonad)
2. [安装](#安装)
3. [核心概念](#核心概念)
4. [快速教程](#快速教程)
5. [最佳实践](#最佳实践)
6. [常见模式](#常见模式)
7. [性能考虑](#性能考虑)

---

## 为什么使用 RustyMonad？

### 传统 Python 错误处理的痛点

```python
# 传统方式 - 大量 if 检查
def get_user_email(user_id: int) -> str | None:
    user = database.get(user_id)
    if user is None:
        return None
    email = user.get_email()
    if email is None:
        return None
    if not email.is_verified():
        return None
    return email.address

# 使用时
email = get_user_email(123)
if email is None:
    email = "default@example.com"
send_email(email)
```

### RustyMonad 方式

```python
from rustymonad import Option, Some, Nothing, Result, Ok, Err

# 定义返回类型
def get_user_email(user_id: int) -> Option[Email]:
    user = database.get(user_id)       # Option[User]
    email = user.get_email()           # Option[Email]
    verified = email.is_verified()     # bool
    return Some(email) if verified else Nothing()

# 使用时 - 链式调用
email = get_user_email(123).unwrap_or("default@example.com")
send_email(email)
```

### 主要优势

| 优势 | 说明 |
|------|------|
| **类型安全** | 类型签名明确表示可能失败 |
| **减少错误** | 编译器/mypy 捕获未处理的错误 |
| **可读性** | 链式调用清晰表达数据流向 |
| **可组合** | 易于组合多个操作 |
| **一致性** | 统一的错误处理模式 |

---

## 安装

```bash
pip install rustymonad
```

**要求：**
- Python 3.8+（完整功能）
- Python 3.10+（模式匹配）

---

## 核心概念

### Option[T] - 可选值

表示一个可能存在或不存在的值。

```python
from rustymonad import Option, Some, Nothing

# Some - 包含值
some_int: Option[int] = Some(42)
some_str: Option[str] = Some("hello")

# Nothing - 空值
empty: Option[int] = Nothing()
```

### Result[T, E] - 结果

表示操作的成功或失败。

```python
from rustymonad import Result, Ok, Err

# Ok - 成功
ok: Result[int, str] = Ok(42)

# Err - 失败
err: Result[int, str] = Err("error message")
```

### 链式操作

所有 monadic 类型都支持链式操作：

```python
from rustymonad import Ok, Some

# map - 转换值
Ok(10).map(lambda x: x * 2)    # Ok(20)

# and_then - 链式调用（返回同类型）
Ok(5).and_then(lambda x: Ok(x * 2))   # Ok(10)

# or_else - 错误时恢复
Err("oops").or_else(lambda e: Ok(0))  # Ok(0)
```

---

## 快速教程

### 教程 1：处理可选值

**场景：** 从字典获取嵌套值

```python
from rustymonad import Option, Some, Nothing

def get_nested_value(data: dict, *keys) -> Option:
    result = Some(data)
    for key in keys:
        result = result.and_then(
            lambda r: Some(r.get(key)) if key in r else Nothing()
        )
    return result

# 使用
data = {
    "user": {
        "profile": {
            "name": "Alice"
        }
    }
}

get_nested_value(data, "user", "profile", "name")  # Some("Alice")
get_nested_value(data, "user", "profile", "age")   # Nothing
```

### 教程 2：安全的链式调用

**场景：** 解析配置并验证

```python
from rustymonad import Result, Ok, Err

def parse_port(config: dict) -> Result[int, str]:
    port_raw = config.get("port")
    if port_raw is None:
        return Err("'port' not found in config")
    
    if not isinstance(port_raw, int):
        return Err("'port' must be an integer")
    
    if port_raw < 1 or port_raw > 65535:
        return Err("'port' must be between 1 and 65535")
    
    return Ok(port_raw)

def parse_host(config: dict) -> Result[str, str]:
    host = config.get("host")
    if host is None:
        return Err("'host' not found in config")
    if not isinstance(host, str):
        return Err("'host' must be a string")
    return Ok(host)

def parse_config(config: dict) -> Result[dict, str]:
    port = parse_port(config)
    host = parse_host(config)
    
    # 组合结果
    return port.and_then(lambda p: 
           host.map(lambda h: {"host": h, "port": p}))

# 使用
config = {"port": 8080, "host": "localhost"}
parse_config(config)  # Ok({"host": "localhost", "port": 8080})

config = {"port": "invalid"}
parse_config(config)  # Err("'port' must be an integer")
```

### 教程 3：使用 Do-Notation

**场景：** 顺序执行多个可能失败的操作

```python
from rustymonad import Result, Ok, Err, DoRet, do_notation

@do_notation
def setup_database(config: dict) -> DoRet[Result[Database, str]]:
    """设置数据库连接。"""
    host = yield Ok(config["host"])
    port = yield Ok(config["port"])
    user = yield Ok(config.get("user", "root"))
    password = yield Ok(config.get("password", ""))
    
    # 模拟连接
    if port < 1 or port > 65535:
        return Err("Invalid port")
    
    db = Database(host=host, port=port, user=user, password=password)
    return Ok(db)

# 使用
config = {"host": "localhost", "port": 5432}
setup_database(config)  # Ok(Database(...))
```

### 教程 4：模式匹配

**场景：** 处理不同结果

```python
from rustymonad import Result, Ok, Err, Option, Some, Nothing

def handle_result(result: Result[int, str]) -> str:
    match result:
        case Ok(value) if value > 100:
            return f"Large: {value}"
        case Ok(value):
            return f"Value: {value}"
        case Err(error):
            return f"Error: {error}"
        case _:
            return "Unknown"

handle_result(Ok(200))   # "Large: 200"
handle_result(Ok(50))    # "Value: 50"
handle_result(Err("oops"))  # "Error: oops"
```

---

## 最佳实践

### 1. 明确类型注解

```python
# ✅ 好
def parse_number(s: str) -> Result[int, str]:
    ...

# ❌ 避免
def parse_number(s: str):
    ...
```

### 2. 错误消息要有意义

```python
# ✅ 好
Err("Configuration file 'config.json' not found")

# ❌ 避免
Err("error")
Err("failed")
```

### 3. 避免过度嵌套

```python
# ❌ 避免 - 深层嵌套
result = (
    Ok(data)
    .and_then(lambda d: parse_user(d))
    .and_then(lambda u: 
        Ok(u).and_then(lambda u2: 
            Ok(u2).and_then(lambda u3: 
                validate_user(u3)
            )
        )
    )
)

# ✅ 好 - 扁平化
def process_user(user: User) -> Result[ProcessedUser, str]:
    validated = validate_user(user)
    enriched = enrich_user(validated)
    return format_user(enriched)

result = parse_user(data).and_then(process_user)
```

### 4. 使用适当的默认值

```python
# unwrap_or - 简单默认值
value = Ok(42).unwrap_or(0)

# or_else - 复杂恢复逻辑
value = Err("error").or_else(lambda: fetch_cached_value())
```

### 5. 组合多个 Result

```python
from rustymonad import Ok

def combine_results(results: list[Result[int, str]]) -> Result[list[int], str]:
    """组合多个 Result，任意失败则整体失败。"""
    values = []
    for r in results:
        values.append(r.unwrap())  # 遇到 Err 会抛出
    return Ok(values)

# 或者使用链式
combined = Ok([1, 2, 3]).map(list)  # 确保类型
```

---

## 常见模式

### 模式 1：配置文件解析

```python
from rustymonad import Result, Ok, Err, Option, Some, Nothing

class Config:
    def __init__(self, data: dict):
        self.data = data
    
    def get(self, key: str) -> Option[Any]:
        return Some(self.data[key]) if key in self.data else Nothing()
    
    def get_str(self, key: str) -> Result[str, str]:
        val = self.get(key)
        if val.is_nothing():
            return Err(f"Missing config: {key}")
        value = val.unwrap()
        if not isinstance(value, str):
            return Err(f"Config '{key}' must be a string")
        return Ok(value)
    
    def get_int(self, key: str) -> Result[int, str]:
        val = self.get(key)
        if val.is_nothing():
            return Err(f"Missing config: {key}")
        value = val.unwrap()
        if not isinstance(value, int):
            return Err(f"Config '{key}' must be an integer")
        return Ok(value)
```

### 模式 2：验证链

```python
from rustymonad import Result, Ok, Err

def validate_email(email: str) -> Result[str, str]:
    if "@" not in email:
        return Err("Invalid email: missing @")
    if "." not in email:
        return Err("Invalid email: missing .")
    return Ok(email.lower())

def validate_password(password: str) -> Result[str, str]:
    if len(password) < 8:
        return Err("Password must be at least 8 characters")
    if not any(c.isupper() for c in password):
        return Err("Password must contain uppercase letter")
    return Ok(password)

def validate_user_registration(
    email: str, 
    password: str
) -> Result[dict, list[str]]:
    errors = []
    
    validate_email(email).map_err(lambda e: errors.append(e))
    validate_password(password).map_err(lambda e: errors.append(e))
    
    if errors:
        return Err(errors)
    
    return Ok({"email": email, "password": password})
```

### 模式 3：缓存模式

```python
from rustymonad import Result, Ok, Err, Option, Some

class CachedLoader:
    def __init__(self):
        self.cache: dict[str, Result] = {}
    
    def load(self, key: str) -> Result[Data, str]:
        # 检查缓存
        if key in self.cache:
            return self.cache[key]
        
        # 加载数据
        result = self._fetch_from_db(key)
        
        # 存入缓存
        self.cache[key] = result
        return result
    
    def _fetch_from_db(self, key: str) -> Result[Data, str]:
        # 实现数据库访问...
        return Ok(Data(key=key))
```

---

## 性能考虑

### 开销

使用 rustymonad 会有一定性能开销：

| 操作 | 耗时 | 建议 |
|------|------|------|
| `Some` / `Ok` 创建 | ~0.3-0.8 µs | 缓存复用 |
| `map` / `and_then` | ~0.5-1 µs | 避免过多链式 |
| `unwrap` | ~0.2-0.3 µs | - |

### 性能敏感场景

```python
# ✅ 性能敏感路径使用简单类型
def hot_path(x: int) -> int:
    return x * 2 + 1

# ✅ 边界检查使用 rustymonad
def safe_parse(s: str) -> Result[int, str]:
    return Ok(int(s)) if s.isdigit() else Err("not a number")
```

### Nothing 单例

```python
from rustymonad import Nothing

# ✅ 好 - Nothing() 返回同一实例
n1 = Nothing()
n2 = Nothing()
assert n1 is n2  # True - 零开销
```

---

## 下一步

- 查看 [API 参考](api.md) 了解完整文档
- 查看 [性能测试报告](../BENCHMARK_RESULTS.md) 了解性能数据
- 查看 [GitHub 仓库](https://github.com/AkiSun/rustymonad) 获取最新信息
