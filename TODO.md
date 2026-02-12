# rustymonad 分步实施计划

## 基本信息
- 项目：rustymonad
- GitHub：AkiSun/rustymonad
- 类型：Python Monad 工具库
- 最后更新：2026-02-10
- 当前阶段：P0 紧急修复

## P0 - 紧急修复
- [x] #1 Some.and_then 类型不一致 - [负责人: subagent] - [状态: 已完成 2026-02-10]
- [x] #2 Nothing 单例问题 - [负责人: subagent] - [状态: 已完成 2026-02-10]

## P1 - 重要优化
- [x] #3 Ok/Err 代码重复问题 - [负责人: subagent] - [状态: 已完成 2026-02-10]
- [x] #4 注释语言不一致 - [负责人: subagent] - [状态: 已完成]
- [ ] #5 空行风格不一致 - [负责人: subagent] - [状态: 已完成 2026-02-11]
- [ ] #6 缺少错误类型继承 - [负责人: subagent] - [状态: 已完成 2026-02-11]
- [x] #7 TypeVar 污染 - [负责人: subagent] - [状态: 已完成 2026-02-11]
- [x] #8 do_notation 错误提示不清晰 - [负责人: subagent] - [状态: 已完成 2026-02-11]

## P2 - 一般改进
- [x] #9 缺少 __slots__ - [负责人: subagent] - [状态: 已完成 2026-02-11]
- [ ] #10 缺少文档字符串 - [负责人: subagent] - [状态: 已完成 2026-02-11]
- [x] #11 测试覆盖率未知 - [负责人: subagent] - [状态: 已完成 2026-02-11]
- [x] #12 缺少基准测试 - [负责人: subagent] - [状态: 已完成 2026-02-11]
- [x] #13 Err.__hash__ 潜在问题 - [负责人: subagent] - [状态: 已完成 2026-02-11]
- [x] #14 缺少 copy/deepcopy - [负责人: subagent] - [状态: 已完成 2026-02-11]

## 文档完善
- [x] #15 README.md 补充英文注释 - [负责人: subagent] - [状态: 已完成 2026-02-11]
- [ ] #16 添加 CONTRIBUTING.md - [负责人: subagent] - [状态: 已完成 2026-02-11]
- [ ] #17 添加 CHANGELOG.md - [负责人: subagent] - [状态: 已完成 2026-02-11]

## 阶段性工作清单
每个阶段完成后必须完成：
- [x] 测试验证 - Some.and_then 修复已包含测试
- [x] 代码审查 - PR 已创建，等待审核 https://github.com/AkiSun/rustymonad/compare/main...feature/rustymonad-optimizations?expand=1
- [x] 文档完善 - README.md、CONTRIBUTING.md、CHANGELOG.md 已更新
- [ ] 远程推送 - PR 审核通过后执行

---

# rustymonad 第二阶段优化（2026-02-11 新增，2026-02-12 确认）

## 需求文档

### 1. 泛型命名改进
| TypeVar | 含义 |
|---------|------|
| `T` | 被 Ok/Some 包裹的普通类型 |
| `U` | 被 Ok/Some 包裹的普通类型（可与 T 不同） |
| `E` | 被 Err 包裹的类型（普通类型或异常类型） |
| `F` | 被 Err 包裹的类型（可与 E 不同） |

### 2. Option Hash 实现
| 类型 | hash 实现 |
|------|----------|
| `Some` | `hash(_value)` |
| `Nothing` | `hash(None)` |

### 3. 比较运算
直接比较内部值，类型不一致或不可比较时抛出错误：
- `Some(5) < Some(10)` → `True`
- `Nothing() < Some(5)` → `True`（Nothing 视为最小值）

### 4. 性能基准测试
分别测试以下场景的性能开销：
- 基础计算脚本（无 Monad）
- 引入 Result 的脚本
- 引入 Option 的脚本
- 引入 do_notation 的脚本
- 三者混用的脚本

---

## P0 - 核心改进
- [x] #1 改进 monad.py 泛型命名（`TMonad` → `T`, `UMonad` → `U`） - [负责人: subagent] - [状态: 已完成 2026-02-12]
- [x] #2 改进 option.py 泛型命名（`TOption` → `T`, `UOption` → `U`, `EOption` → `E`） - [负责人: subagent] - [状态: 已完成 2026-02-12]
- [x] #3 改进 result.py 泛型命名（`TResult` → `T`, `UResult` → `U`, `EResult` → `E`, `FResult` → `F`） - [负责人: subagent] - [状态: 已完成 2026-02-12]

## P1 - 新特性
- [x] #4 实现 Option 的 `__hash__`（Some → hash(value), Nothing → hash(None)） - [负责人: subagent] - [状态: 已完成 2026-02-12]
- [x] #5 实现 Option 比较运算（`__lt__`, `__le__`, `__gt__`, `__ge__`） - [负责人: subagent] - [状态: 已完成 2026-02-12]
- [x] #6 实现 Result 比较运算（`__lt__`, `__le__`, `__gt__`, `__ge__`） - [负责人: subagent] - [状态: 已完成 2026-02-12]

## P2 - 性能测试
- [x] #7 创建性能基准测试脚本 - [负责人: subagent] - [状态: 已完成 2026-02-12]
- [x] #8 单独测试 Result 性能开销 - [负责人: subagent] - [状态: 已完成 2026-02-12]
- [x] #9 单独测试 Option 性能开销 - [负责人: subagent] - [状态: 已完成 2026-02-12]
- [x] #10 单独测试 do_notation 性能开销 - [负责人: subagent] - [状态: 已完成 2026-02-12]
- [x] #11 测试三者混用性能 - [负责人: subagent] - [状态: 已完成 2026-02-12]
- [x] #12 生成性能报告 - [负责人: subagent] - [状态: 已完成 2026-02-12]

## 阶段性工作清单
- [x] 测试验证 - 所有新功能必须包含单元测试
- [x] 代码审查 - 审核通过
- [x] README.md 更新 - 添加 __hash__ 和比较运算说明
- [x] 测试用例修复 - 将 NotImplemented 预期改为 TypeError
- [ ] 远程推送 - 推送到远程仓库
