# rustymonad Optimization Plan

## 项目概述

**rustymonad** - Python Monad 工具库，模仿 Rust 的 Option 和 Result 特性

---

## 分步实施计划

### Phase 1: P0 - 紧急修复 ⚠️

#### 1.1 Some.and_then 类型不一致
**文件**: `src/option.py` 第62行  
**问题**: 返回类型声明为 `Option[U]`，但实际可能返回非 Option 值  
**修复**:
```python
def and_then(self, fn: Callable[[T], Option[U]]) -> Option[U]:
    # 确保 fn 返回的是 Option 类型
```
**优先级**: P0

#### 1.2 Nothing 单例问题
**文件**: `src/option.py` 第96行、171行  
**问题**: `Nothing.__init__` 每次调用都初始化，底部调用 `Nothing()` 确保单例  
**修复**: 优化单例实现，确保 `Nothing()` 始终返回同一实例  
**优先级**: P0

---

### Phase 2: P1 - 重要改进 🔧

#### 2.1 Ok/Err 代码重复
**文件**: `src/result.py`  
**问题**: `Ok` 和 `Err` 中有大量重复的 `map/flatmap/inspect` 实现  
**修复**: 使用 mixin 类或工厂函数减少重复  
**优先级**: P1

#### 2.2 注释语言不一致
**文件**: 全部文件  
**问题**: 注释中英混用  
**修复**: 统一使用英文，便于国际化维护  
**优先级**: P1

#### 2.3 空行风格不一致
**文件**: 多处  
**问题**: 类方法之间空行数量不一致  
**修复**: 按 PEP 8 统一：类定义后空2行，方法间空1行  
**优先级**: P1

#### 2.4 缺少错误类型继承
**文件**: `src/result.py`  
**问题**: `Err` 的 `unwrap` 抛出通用 `Exception`  
**修复**: 创建自定义异常类 `RustyMonadError`  
**优先级**: P1

#### 2.5 TypeVar 污染
**文件**: `src/monad.py`  
**问题**: 全局定义的 `T`, `U` 可能与用户代码冲突  
**修复**: 使用本地 TypeVar 或添加后缀如 `TMonad`  
**优先级**: P1

#### 2.6 do_notation 错误提示不清晰
**文件**: `src/utils.py` 第31行  
**问题**: 错误信息未指出具体问题  
**修复**: 增强错误信息，提示期望的返回类型  
**优先级**: P1

---

### Phase 3: P2 - 一般优化 📝

#### 3.1 缺少 `__slots__`
**文件**: `src/monad.py`  
**问题**: 未使用 `__slots__` 会增加内存开销  
**修复**: Monad 基类添加 `__slots__ = ()`（子类自动继承）  
**优先级**: P2

#### 3.2 缺少文档字符串
**文件**: 所有类和方法  
**修复**: 为所有公开方法添加 docstring  
**优先级**: P2

#### 3.3 测试覆盖率未知
**文件**: 项目根目录  
**修复**: 添加 `pytest-cov` 配置  
**优先级**: P2

#### 3.4 缺少基准测试
**文件**: 项目根目录  
**修复**: 添加 `pytest-benchmark`  
**优先级**: P2

#### 3.5 Err.__hash__ 潜在问题
**文件**: `src/result.py` 第217行  
**问题**: 如果 `E` 不可哈希（如 list），会抛出 `TypeError`  
**修复**: 文档说明或使用 `try/except` 处理  
**优先级**: P2

#### 3.6 缺少 copy/deepcopy
**文件**: 所有 Monad 类  
**问题**: 无法复制 monad 实例  
**修复**: 实现 `__copy__` / `__deepcopy__`  
**优先级**: P2

---

## 实施顺序

```
Phase 1 (P0) → Phase 2 (P1) → Phase 3 (P2)
```

---

## 备注

- 专注于 Rust 的 Option 和 Result 特性
- 不需要添加 Either 类型
- `__slots__` 只需在 Monad 基类添加一次
