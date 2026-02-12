"""性能对比测试：普通 Python vs rustymonad Option/Result

这个测试对比同一个逻辑在使用和不使用 rustymonad 时的性能差异。
"""

import pytest
from rustymonad import Option, Some, Nothing, Result, Ok, Err


# ============== 基础计算（无 Monad）==============

def pipeline_plain(x: int) -> int:
    """普通流水线计算"""
    x = x + 1
    x = x * 2
    x = x - 1
    x = x ** 2
    return x


def pipeline_with_none(x: int | None) -> int | None:
    """处理可能为 None 的值"""
    if x is None:
        return None
    x = x + 1
    x = x * 2
    x = x - 1
    x = x ** 2
    return x


def safe_divide_plain(a: float, b: float) -> float | None:
    """安全除法"""
    if b == 0:
        return None
    return a / b


class TestPlainPython:
    """普通 Python 代码性能测试"""

    def test_pipeline(self, benchmark):
        """基准：普通流水线计算"""
        benchmark(pipeline_plain, 10)

    def test_pipeline_none_check(self, benchmark):
        """基准：带 None 检查的流水线"""
        benchmark(pipeline_with_none, 10)

    def test_pipeline_none_shortcut(self, benchmark):
        """基准：None 短路"""
        benchmark(pipeline_with_none, None)

    def test_safe_divide_normal(self, benchmark):
        """基准：正常除法"""
        benchmark(safe_divide_plain, 10, 2)

    def test_safe_divide_by_zero(self, benchmark):
        """基准：除零处理"""
        benchmark(safe_divide_plain, 10, 0)


# ============== 使用 Option ==============

def pipeline_option(x: Option[int]) -> Option[int]:
    """Option 流水线"""
    return x.map(lambda v: v + 1) \
            .map(lambda v: v * 2) \
            .map(lambda v: v - 1) \
            .map(lambda v: v ** 2)


def safe_divide_option(a: float, b: float) -> Option[float]:
    """Option 安全除法"""
    return Ok(b).and_then(lambda b_val: 
               Nothing() if b_val == 0 else 
               Some(a / b_val))


class TestWithOption:
    """使用 Option 的性能测试"""

    def test_option_pipeline(self, benchmark):
        """Option 流水线"""
        opt = Some(10)
        benchmark(pipeline_option, opt)

    def test_option_pipeline_nothing(self, benchmark):
        """Option 流水线 - Nothing 短路"""
        opt = Nothing()
        benchmark(pipeline_option, opt)

    def test_option_safe_divide(self, benchmark):
        """Option 安全除法"""
        benchmark(safe_divide_option, 10, 2)

    def test_option_safe_divide_by_zero(self, benchmark):
        """Option 除零 - 返回 Nothing"""
        benchmark(safe_divide_option, 10, 0)


# ============== 使用 Result ==============

def pipeline_result(x: Result[int, str]) -> Result[int, str]:
    """Result 流水线"""
    return x.map(lambda v: v + 1) \
            .map(lambda v: v * 2) \
            .map(lambda v: v - 1) \
            .map(lambda v: v ** 2)


def safe_divide_result(a: float, b: float) -> Result[float, str]:
    """Result 安全除法"""
    return Ok(b).and_then(lambda b_val: 
               Err("division by zero") if b_val == 0 else 
               Ok(a / b_val))


class TestWithResult:
    """使用 Result 的性能测试"""

    def test_result_pipeline(self, benchmark):
        """Result 流水线"""
        res = Ok(10)
        benchmark(pipeline_result, res)

    def test_result_pipeline_err(self, benchmark):
        """Result 流水线 - Err 短路"""
        res = Err("error")
        benchmark(pipeline_result, res)

    def test_result_safe_divide(self, benchmark):
        """Result 安全除法"""
        benchmark(safe_divide_result, 10, 2)

    def test_result_safe_divide_by_zero(self, benchmark):
        """Result 除零 - 返回 Err"""
        benchmark(safe_divide_result, 10, 0)


# ============== 混合使用 ==============

def mixed_pipeline(value: int) -> Option[int]:
    """混合使用 Option（仅 Option）"""
    opt = Some(value)
    return opt.map(lambda x: x + 10) \
              .map(lambda x: x * 2) \
              .and_then(lambda x: Nothing() if x > 50 else Some(x))


class TestMixedUsage:
    """混合使用的性能测试"""

    def test_mixed_normal(self, benchmark):
        """混合流水线 - 正常"""
        benchmark(mixed_pipeline, 10)

    def test_mixed_error(self, benchmark):
        """混合流水线 - 错误情况"""
        benchmark(mixed_pipeline, -5)
