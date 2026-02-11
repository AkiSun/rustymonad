# RustyMonad 基准测试结果

**测试日期**: 2026-02-11  
**测试环境**: Linux (x86_64), Python 3.11.6  
**测试工具**: pytest-benchmark 5.2.3

## 测试概述

共执行 **56** 个基准测试，涵盖以下类别：
- Option 创建与操作
- Result 创建与操作
- Map/Flatmap 性能
- Unwrap 操作
- 链式操作
- 单例行为

## 性能摘要 (纳秒)

### 最快操作 (Top 10)

| 操作 | 平均时间 (ns) | OPS (Kops/s) |
|------|--------------|--------------|
| Ok.is_ok | 155.87 | 6,415.55 |
| Err.is_err | 136.22 | 7,341.12 |
| Some.is_some | 127.46 | 7,845.54 |
| Some.is_nothing | 126.18 | 7,925.34 |
| Ok.is_err | 125.00 | 7,999.75 |
| Err.is_ok | 133.35 | 7,499.14 |
| Some.unwrap | 135.81 | 7,363.03 |
| Ok.unwrap | 137.03 | 7,297.52 |
| Nothing.is_nothing | 164.48 | 6,079.61 |
| Nothing.is_some | 129.42 | 7,727.06 |

### 最慢操作 (Bottom 10)

| 操作 | 平均时间 (ns) | OPS (Kops/s) |
|------|--------------|--------------|
| Result.chain_all_ok | 3,651.88 | 273.83 |
| Ok.flatmap_chain | 2,898.80 | 344.97 |
| Option.chain_all_some | 2,391.34 | 418.18 |
| Result.chain_with_err | 2,420.58 | 413.12 |
| Some.flatmap_chain | 2,029.71 | 492.68 |
| Option.chain_with_nothing | 1,706.82 | 585.89 |
| Mixed.option_result | 1,629.76 | 613.59 |
| Result.rshift | 1,498.99 | 667.12 |
| Option.chain_with_nothing | 1,417.01 | - |
| Ok.and_then | 1,140.60 | 876.73 |

## 详细结果

### Option 创建性能

| 操作 | Min (ns) | Max (ns) | Mean (ns) | Median (ns) |
|------|----------|----------|-----------|-------------|
| Some(字符串) | 300.45 | 25,496.05 | 333.75 | 305.50 |
| Some(列表) | 245.68 | 21,277.17 | 452.55 | 411.33 |
| Some(整数) | 467.00 | 614,585.01 | 796.42 | 718.98 |
| Nothing() | 0.00 | 28,237.00 | 661.76 | 641.04 |

### Result 创建性能

| 操作 | Min (ns) | Max (ns) | Mean (ns) | Median (ns) |
|------|----------|----------|-----------|-------------|
| Ok(整数) | 924.98 | 50,168.02 | 1,082.02 | 983.01 |
| Ok(字符串) | 907.05 | 309,435.01 | 1,075.11 | 988.02 |
| Err(字符串) | 923.99 | 69,778.99 | 1,111.33 | 987.96 |
| Err(Exception) | 758.04 | 96,680.01 | 1,165.82 | 1,095.00 |

### Map/Flatmap 性能

| 操作 | Mean (ns) | 说明 |
|------|-----------|------|
| Some.map | 402.18 | 简单转换 |
| Some.map(复杂) | 1,025.11 | 复杂计算 |
| Err.map | 132.71 | Err 上调用 map |
| Ok.map | 679.06 | Ok 上调用 map |
| Some.flatmap | 418.45 | 链式转换 |
| Ok.flatmap | 1,192.84 | Result flatmap |

### Unwrap 操作性能

| 操作 | Mean (ns) | 说明 |
|------|-----------|------|
| Some.unwrap | 135.81 | 获取 Some 值 |
| Ok.unwrap | 137.03 | 获取 Ok 值 |
| Nothing.unwrap_or | 127.08 | Nothing 提供默认值 |
| Ok.unwrap_or | 160.61 | Ok 返回自身值 |
| Err.unwrap_or | 132.75 | Err 返回默认值 |

## 关键发现

1. **状态检查极快**: `is_some()`/`is_ok()` 等检查操作耗时约 125-165 ns
2. **链式操作开销**: 3-4 个操作的链式调用约需 2-3 μs
3. **Nothing 单例**: 多次调用 `Nothing()` 返回相同实例（符合预期）
4. **异常处理开销**: `expect()` 在 Nothing 上触发异常的开销较高

## 改进建议

1. 对于性能敏感场景，优先使用 `is_some()`/`is_ok()` 进行检查
2. 避免在热代码路径中进行过多链式操作
3. 对于已知的 Ok/Some 场景，使用 `unwrap_unchecked()` 可减少检查开销

## 运行基准测试

```bash
# 运行所有基准测试
pytest tests/test_benchmark.py --benchmark-only

# 运行特定测试类别
pytest tests/test_benchmark.py::TestOptionCreation --benchmark-only

# 保存基准数据
pytest tests/test_benchmark.py --benchmark-save=benchmark_name
```
