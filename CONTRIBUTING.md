# Contributing to RustyMonad

感谢您对 RustyMonad 项目的兴趣！我们欢迎各种形式的贡献，包括代码改进、文档完善、Bug 修复和新功能添加。

## 📋 目录

- [快速开始](#快速开始)
- [贡献方式](#贡献方式)
- [开发环境设置](#开发环境设置)
- [代码规范](#代码规范)
- [提交信息规范](#提交信息规范)
- [测试要求](#测试要求)
- [文档要求](#文档要求)
- [Pull Request 流程](#pull-request-流程)

## 🚀 快速开始

1. **Fork 本仓库**
   
   点击 GitHub 页面右上角的 Fork 按钮。

2. **克隆您的 Fork**
   
   ```bash
   git clone https://github.com/YOUR_USERNAME/rustymonad.git
   cd rustymonad
   ```

3. **创建特性分支**
   
   ```bash
   git checkout -b feature/your-feature-name
   ```

4. **进行开发并提交更改**

5. **推送并创建 Pull Request**

## 🤝 贡献方式

### 🐛 Bug 报告

- 在提交 Bug 报告前，请先搜索 [Issues](https://github.com/AkiSun/rustymonad/issues) 是否已有相关报告
- 使用清晰的标题描述问题
- 提供复现步骤、环境信息（Python 版本、操作系统等）
- 如果可能，提供最小化的复现代码
- 说明预期行为与实际行为的差异

### 💡 功能建议

- 清晰描述您希望添加的功能
- 解释为什么这个功能对项目有价值
- 提供使用场景的示例
- 考虑是否与项目的核心目标（Rust 风格的 Python Monad 工具库）相符

### 🔧 代码贡献

- 遵循本指南中的代码规范
- 确保所有测试通过
- 添加适当的文档字符串
- 保持提交历史整洁

## 🛠 开发环境设置

### 环境要求

- Python 3.10+
- Git
- 推荐使用 virtualenv 或 venv

### 安装开发依赖

```bash
# 创建虚拟环境
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# 或 .venv\Scripts\activate  # Windows

# 安装项目依赖
pip install -e ".[dev]"

# 安装 pre-commit 钩子（推荐）
pre-commit install
```

### 运行测试

```bash
# 运行所有测试
pytest

# 生成测试覆盖率报告
pytest --cov=rustymonad --cov-report=html

# 运行特定测试文件
pytest tests/test_*.py

# 运行特定测试
pytest tests/test_option.py::test_some_unwrap
```

### 代码检查

```bash
# 类型检查
mypy src/rustymonad

# 代码格式化检查
ruff check src/rustymonad

# 导入排序检查
isort --check-only --diff src/rustymonad
```

## 📝 代码规范

### Python 版本支持

- 代码必须兼容 Python 3.10+
- 使用 `from __future__ import annotations` 以支持所有 Python 版本的类型注解

### 类型注解

- **所有公共函数必须有类型注解**
- 使用泛型类型（如 `Option[T]`、`Result[T, E]`）
- 避免使用 `Any`，尽量使用具体类型
- 对复杂类型使用 TypeVar：

```python
from typing import TypeVar, Generic

T = TypeVar('T')
E = TypeVar('E')

class Result(Generic[T, E]):
    def map(self, fn: Callable[[T], U]) -> 'Result[U, E]': ...
```

### 代码风格

- 遵循 [PEP 8](https://pep8.org/) 代码风格指南
- 使用 **4 个空格**缩进（不使用 Tab）
- 行长度限制：**100 字符**
- 函数和类之间使用 **两个空行**
- 方法之间使用 **一个空行**

### 命名规范

| 类型 | 规范 | 示例 |
|------|------|------|
| 类名 | PascalCase | `Option`, `Some`, `Result` |
| 函数/方法 | snake_case | `unwrap_or`, `and_then` |
| 变量 | snake_case | `some_value`, `error_msg` |
| 常量 | UPPER_SNAKE_CASE | `NOTHING_INSTANCE` |
| 类型变量 | PascalCase | `T`, `E`, `ValueT` |
| 私有方法/变量 | `_single_leading_underscore` | `_unwrap_impl` |

### Docstring 规范

所有公共函数、类和方法必须有 docstring：

```python
def unwrap_or(self, default: T) -> T:
    """Return the contained value or a default.
    
    Args:
        self: The Option instance.
        default: The value to return if the Option is Nothing.
    
    Returns:
        The contained value if Some, otherwise the default.
    
    Examples:
        >>> Some(42).unwrap_or(0)
        42
        >>> Nothing().unwrap_or(0)
        0
    """
    ...
```

**注意**：
- 使用中文注释 + 英文 docstring
- 保持注释简洁明了
- 避免明显的注释（如 `# increment i`）

### import 顺序

```python
# 标准库
from __future__ import annotations
from typing import Generic, TypeVar, Callable, Any

# 第三方库（按字母顺序）
from dataclasses import dataclass

# 项目内部
from rustymonad.monad import Monad
```

### 性能考量

- 为所有类添加 `__slots__` 以减少内存占用
- 对于频繁创建的对象，考虑使用 `__new__` 实现单例模式
- 使用惰性求值时注意避免不必要的计算

## 📌 提交信息规范

### 提交信息格式

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Type 类型

| 类型 | 描述 |
|------|------|
| `feat` | 新功能 |
| `fix` | Bug 修复 |
| `docs` | 文档更新 |
| `style` | 代码格式调整（不影响功能） |
| `refactor` | 重构代码 |
| `perf` | 性能优化 |
| `test` | 测试相关 |
| `chore` | 构建工具、辅助功能等 |

### Scope 范围

修改的模块范围，如：
- `monad` - 核心 Monad 类型
- `option` - Option 相关
- `result` - Result 相关
- `do_notation` - Do  notation 功能
- `benchmark` - 基准测试
- `docs` - 文档
- `ci` - CI/CD 配置

### 示例

```
feat(monad): add __copy__ and __deepcopy__ methods

Implement shallow and deep copying support for all monadic types
to allow users to create independent copies of monad instances.

Closes #14
```

```
fix(option): resolve Some.and_then type inconsistency

The return type of Some.and_then was incorrectly typed as Option
instead of the result of the callback function. Fixed to properly
propagate the callback's return type.

Fixes #1
```

### 提交准则

- 使用中文描述提交信息
- 标题不超过 50 个字符
- 描述性主体（如果需要），说明 **为什么** 而不是 **做了什么**
- Footer 中引用相关 Issues（如 `Closes #123`）

## ✅ 测试要求

### 测试覆盖率

- 所有新功能必须包含测试
- 修复 Bug 时，添加回归测试
- 目标：保持测试覆盖率在 **90%+**

### 测试文件结构

```
tests/
├── __init__.py
├── conftest.py          # pytest 配置和 fixtures
├── test_option.py       # Option 类型测试
├── test_result.py       # Result 类型测试
├── test_do_notation.py  # Do notation 测试
└── test_decorators.py   # 装饰器测试
```

### 测试风格

```python
def test_some_unwrap_returns_value():
    """Test that Some.unwrap returns the contained value."""
    some = Some(42)
    assert some.unwrap() == 42


def test_nothing_unwrap_raises_error():
    """Test that Nothing.unwrap raises UnwrapOptionError."""
    nothing = Nothing()
    with pytest.raises(UnwrapOptionError):
        nothing.unwrap()


def test_result_map_transforms_value():
    """Test that map transforms the Ok value."""
    ok = Ok(10)
    mapped = ok.map(lambda x: x * 2)
    assert mapped.unwrap() == 20
```

### 测试原则

- 每个测试一个断言（尽量）
- 测试名称清晰描述测试内容
- 使用 `pytest.raises` 测试异常情况
- 测试边界条件和错误情况

## 📚 文档要求

### README 更新

如果影响用户使用方式，更新 `README.md`：
- 添加新功能的示例代码
- 更新 API 参考表格
- 修改安装和使用说明

### 代码文档

- 所有公共 API 必须有 docstring
- 复杂算法添加行内注释
- 更新类型注解以反映实际功能

### 中文注释

- 使用中文编写注释
- 保持注释简洁、专业
- 避免过时的注释

## 🔄 Pull Request 流程

### 创建 PR 前

1. **确保所有测试通过**
   
   ```bash
   pytest
   ```

2. **运行代码检查**
   
   ```bash
   ruff check src/
   mypy src/
   isort --check-only src/
   ```

3. **保持分支最新**
   
   ```bash
   git fetch origin
   git rebase origin/main
   ```

4. **更新 CHANGELOG.md**（如果存在）

### PR 描述

- 清晰描述 PR 的目的
- 列出主要的更改内容
- 提供测试结果的截图或说明
- 关联相关 Issues（如 `Fixes #123`）

### PR 审查

- 响应审查意见，及时沟通
- 保持提交历史整洁（必要时进行 rebase）
- 不要在 PR 中添加无关的更改

### PR 合并

- 通过所有 CI 检查后，由维护者合并
- 删除特性分支
- 感谢您的贡献！🎉

## 📜 代码行为准则

### 我们的承诺

为了营造一个开放包容的社区，我们承诺让所有人参与此项目时免受骚扰，无论年龄、体型、残疾、种族、性别认同与表达、经验水平、国籍、个人形象、种族、宗教或性取向。

### 我们的标准

- 使用友好和包容的语言
- 尊重不同的观点和经历
- 优雅地接受建设性批评
- 关注对社区最有利的事情
- 对其他社区成员表示同理心

### 不可接受的行为

- 使用性语言或图像
- 跟踪或骚扰任何人
- 任何形式的歧视
- 公开或私下骚扰

## ❓ 有问题？

如果您对贡献流程有任何疑问：

1. 查看 [Issues](https://github.com/AkiSun/rustymonad/issues) 中是否已有讨论
2. 创建新的 Issue 提问
3. 发送邮件给项目维护者

感谢您对 RustyMonad 的贡献！ 🙏
