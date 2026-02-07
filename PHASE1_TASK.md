# RustyMonad 阶段一开发任务

## 目标
完善 Result 类型，添加 Rust 标准库中的常用方法。

## 需要添加的方法

### 1. unwrap_or_else(self, fn: Callable[[], T]) -> T
当 Result 是 Err 时，调用提供的函数生成默认值。

### 2. map_err(self, fn: Callable[[E], F]) -> Result[T, F]
将 Err 的值映射为另一种错误类型，Ok 保持不变。

### 3. unwrap_unchecked(self) -> T
不安全地解包 Ok 值（仅用于确定是 Ok 的情况）。

### 4. expect_err(self, msg: str) -> E
如果是 Ok 则 panic（抛出异常），如果是 Err 则返回错误值。

### 5. 添加 `__hash__` 支持（如果值可哈希）

## 文件位置
- /root/projects/rustymonad/src/rustymonad/result.py

## 注意事项
- 保持与现有代码风格一致
- 添加完整的类型注解
- 确保 Ok 和 Err 都实现这些方法
- 参考 Rust 文档的行为定义
