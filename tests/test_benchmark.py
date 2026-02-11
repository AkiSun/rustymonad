"""Benchmark tests for rustymonad core functionality.

This module benchmarks the performance of Option and Result types,
including creation, map, flatmap, unwrap, and other core operations.
"""

import pytest
from rustymonad import Option, Some, Nothing, Result, Ok, Err


class TestOptionCreation:
    """Benchmark Option creation operations."""

    def test_some_creation_int(self, benchmark):
        """Benchmark creating Some with an integer."""
        benchmark(lambda: Some(42))

    def test_some_creation_str(self, benchmark):
        """Benchmark creating Some with a string."""
        benchmark(lambda: Some("hello world"))

    def test_some_creation_list(self, benchmark):
        """Benchmark creating Some with a list."""
        benchmark(lambda: Some([1, 2, 3, 4, 5]))

    def test_nothing_creation(self, benchmark):
        """Benchmark creating Nothing."""
        benchmark(Nothing)


class TestOptionMap:
    """Benchmark Option map operations."""

    def test_some_map(self, benchmark):
        """Benchmark map on Some."""
        opt = Some(10)
        benchmark(opt.map, lambda x: x * 2)

    def test_nothing_map(self, benchmark):
        """Benchmark map on Nothing."""
        nothing = Nothing()
        benchmark(nothing.map, lambda x: x * 2)

    def test_some_map_complex(self, benchmark):
        """Benchmark map with complex transformation."""
        opt = Some(100)
        benchmark(opt.map, lambda x: x ** 2 + x * 3 - 7)


class TestOptionFlatmap:
    """Benchmark Option flatmap operations."""

    def test_some_flatmap(self, benchmark):
        """Benchmark flatmap on Some."""
        opt = Some(5)
        benchmark(opt.flatmap, lambda x: Some(x * 2))

    def test_nothing_flatmap(self, benchmark):
        """Benchmark flatmap on Nothing."""
        nothing = Nothing()
        benchmark(nothing.flatmap, lambda x: Some(x * 2))

    def test_some_flatmap_chain(self, benchmark):
        """Benchmark chained flatmap operations."""
        opt = Some(1)
        benchmark(
            lambda: opt.flatmap(lambda x: Some(x + 1))
                      .flatmap(lambda x: Some(x * 2))
                      .flatmap(lambda x: Some(x ** 2))
        )


class TestOptionUnwrap:
    """Benchmark Option unwrap operations."""

    def test_some_unwrap(self, benchmark):
        """Benchmark unwrap on Some."""
        opt = Some(42)
        benchmark(opt.unwrap)

    def test_nothing_unwrap_or(self, benchmark):
        """Benchmark unwrap_or on Nothing."""
        nothing = Nothing()
        benchmark(nothing.unwrap_or, 0)

    def test_some_unwrap_or(self, benchmark):
        """Benchmark unwrap_or on Some (should return value)."""
        opt = Some(42)
        benchmark(opt.unwrap_or, 0)

    def test_nothing_expect(self, benchmark):
        """Benchmark expect on Nothing (will raise, but measures overhead)."""
        nothing = Nothing()
        # Benchmark the overhead of calling expect on Nothing (raises exception)
        def expect_call():
            try:
                nothing.expect("test message")
            except Exception:
                pass
        benchmark(expect_call)


class TestOptionAndThen:
    """Benchmark Option and_then operations."""

    def test_some_and_then(self, benchmark):
        """Benchmark and_then on Some."""
        opt = Some(10)
        benchmark(opt.and_then, lambda x: Some(x * 2))

    def test_nothing_and_then(self, benchmark):
        """Benchmark and_then on Nothing."""
        nothing = Nothing()
        benchmark(nothing.and_then, lambda x: Some(x * 2))


class TestOptionInspect:
    """Benchmark Option inspect operations."""

    def test_some_inspect(self, benchmark):
        """Benchmark inspect on Some."""
        opt = Some(42)
        benchmark(opt.inspect, lambda x: None)

    def test_nothing_inspect(self, benchmark):
        """Benchmark inspect on Nothing."""
        nothing = Nothing()
        benchmark(nothing.inspect, lambda x: None)


class TestOptionIsSome:
    """Benchmark Option is_some/is_nothing checks."""

    def test_some_is_some(self, benchmark):
        """Benchmark is_some on Some."""
        opt = Some(42)
        benchmark(opt.is_some)

    def test_some_is_nothing(self, benchmark):
        """Benchmark is_nothing on Some."""
        opt = Some(42)
        benchmark(opt.is_nothing)

    def test_nothing_is_some(self, benchmark):
        """Benchmark is_some on Nothing."""
        nothing = Nothing()
        benchmark(nothing.is_some)

    def test_nothing_is_nothing(self, benchmark):
        """Benchmark is_nothing on Nothing."""
        nothing = Nothing()
        benchmark(nothing.is_nothing)


class TestResultCreation:
    """Benchmark Result creation operations."""

    def test_ok_creation_int(self, benchmark):
        """Benchmark creating Ok with an integer."""
        benchmark(lambda: Ok(42))

    def test_ok_creation_str(self, benchmark):
        """Benchmark creating Ok with a string."""
        benchmark(lambda: Ok("success"))

    def test_err_creation_str(self, benchmark):
        """Benchmark creating Err with a string."""
        benchmark(lambda: Err("error"))

    def test_err_creation_exception(self, benchmark):
        """Benchmark creating Err with an exception."""
        benchmark(lambda: Err(ValueError("test error")))


class TestResultMap:
    """Benchmark Result map operations."""

    def test_ok_map(self, benchmark):
        """Benchmark map on Ok."""
        res = Ok(10)
        benchmark(res.map, lambda x: x * 2)

    def test_err_map(self, benchmark):
        """Benchmark map on Err."""
        err = Err("error")
        benchmark(err.map, lambda x: x * 2)

    def test_ok_map_complex(self, benchmark):
        """Benchmark map with complex transformation."""
        res = Ok(100)
        benchmark(res.map, lambda x: x ** 2 + x * 3 - 7)

    def test_ok_map_err(self, benchmark):
        """Benchmark map_err on Ok."""
        res = Ok(42)
        benchmark(res.map_err, lambda e: f"mapped: {e}")


class TestResultFlatmap:
    """Benchmark Result flatmap operations."""

    def test_ok_flatmap(self, benchmark):
        """Benchmark flatmap on Ok."""
        res = Ok(5)
        benchmark(res.flatmap, lambda x: Ok(x * 2))

    def test_err_flatmap(self, benchmark):
        """Benchmark flatmap on Err."""
        err = Err("error")
        benchmark(err.flatmap, lambda x: Ok(x * 2))

    def test_ok_flatmap_chain(self, benchmark):
        """Benchmark chained flatmap operations."""
        res = Ok(1)
        benchmark(
            lambda: res.flatmap(lambda x: Ok(x + 1))
                      .flatmap(lambda x: Ok(x * 2))
                      .flatmap(lambda x: Ok(x ** 2))
        )


class TestResultUnwrap:
    """Benchmark Result unwrap operations."""

    def test_ok_unwrap(self, benchmark):
        """Benchmark unwrap on Ok."""
        res = Ok(42)
        benchmark(res.unwrap)

    def test_err_unwrap_or(self, benchmark):
        """Benchmark unwrap_or on Err."""
        err = Err("error")
        benchmark(err.unwrap_or, "default")

    def test_ok_unwrap_or(self, benchmark):
        """Benchmark unwrap_or on Ok (should return value)."""
        res = Ok(42)
        benchmark(res.unwrap_or, "default")

    def test_err_unwrap_err(self, benchmark):
        """Benchmark unwrap_err on Err."""
        err = Err("error message")
        benchmark(err.unwrap_err)


class TestResultAndThen:
    """Benchmark Result and_then operations."""

    def test_ok_and_then(self, benchmark):
        """Benchmark and_then on Ok."""
        res = Ok(10)
        benchmark(res.and_then, lambda x: Ok(x * 2))

    def test_err_and_then(self, benchmark):
        """Benchmark and_then on Err."""
        err = Err("error")
        benchmark(err.and_then, lambda x: Ok(x * 2))


class TestResultInspect:
    """Benchmark Result inspect operations."""

    def test_ok_inspect(self, benchmark):
        """Benchmark inspect on Ok."""
        res = Ok(42)
        benchmark(res.inspect, lambda x: None)

    def test_err_inspect_err(self, benchmark):
        """Benchmark inspect_err on Err."""
        err = Err("error")
        benchmark(err.inspect_err, lambda x: None)


class TestResultIsOk:
    """Benchmark Result is_ok/is_err checks."""

    def test_ok_is_ok(self, benchmark):
        """Benchmark is_ok on Ok."""
        res = Ok(42)
        benchmark(res.is_ok)

    def test_ok_is_err(self, benchmark):
        """Benchmark is_err on Ok."""
        res = Ok(42)
        benchmark(res.is_err)

    def test_err_is_ok(self, benchmark):
        """Benchmark is_ok on Err."""
        err = Err("error")
        benchmark(err.is_ok)

    def test_err_is_err(self, benchmark):
        """Benchmark is_err on Err."""
        err = Err("error")
        benchmark(err.is_err)


class TestResultConversion:
    """Benchmark Result to Option conversion."""

    def test_ok_to_option(self, benchmark):
        """Benchmark ok() method on Ok."""
        res = Ok(42)
        benchmark(res.ok)

    def test_err_to_option(self, benchmark):
        """Benchmark err() method on Err."""
        err = Err("error")
        benchmark(err.err)


class TestChainedOperations:
    """Benchmark complex chained operations."""

    def test_option_chain_all_some(self, benchmark):
        """Benchmark Option chain where all values are Some."""
        opt = Some(1)
        benchmark(
            lambda: opt.map(lambda x: x + 1)
                      .map(lambda x: x * 2)
                      .flatmap(lambda x: Some(x - 1))
                      .map(lambda x: x ** 2)
        )

    def test_option_chain_with_nothing(self, benchmark):
        """Benchmark Option chain that results in Nothing."""
        opt = Some(1)
        benchmark(
            lambda: opt.map(lambda x: x + 1)
                      .flatmap(lambda x: Nothing())
                      .map(lambda x: x * 2)
        )

    def test_result_chain_all_ok(self, benchmark):
        """Benchmark Result chain where all values are Ok."""
        res = Ok(1)
        benchmark(
            lambda: res.map(lambda x: x + 1)
                      .map(lambda x: x * 2)
                      .and_then(lambda x: Ok(x - 1))
                      .map(lambda x: x ** 2)
        )

    def test_result_chain_with_err(self, benchmark):
        """Benchmark Result chain that results in Err."""
        res = Ok(1)
        benchmark(
            lambda: res.map(lambda x: x + 1)
                      .and_then(lambda x: Err("error"))
                      .map(lambda x: x * 2)
        )

    def test_mixed_option_result(self, benchmark):
        """Benchmark mixed Option and Result operations."""
        opt = Some(Ok(42))
        benchmark(
            lambda: opt.flatmap(lambda x: x.map(lambda y: y * 2))
        )


class TestOperatorSyntax:
    """Benchmark operator syntax (>> for flatmap/bind)."""

    def test_option_rshift(self, benchmark):
        """Benchmark >> operator for Option."""
        opt = Some(5)
        benchmark(lambda: (opt >> (lambda x: Some(x * 2))))

    def test_result_rshift(self, benchmark):
        """Benchmark >> operator for Result."""
        res = Ok(5)
        benchmark(lambda: (res >> (lambda x: Ok(x * 2))))


class TestSingletonBehavior:
    """Benchmark Nothing singleton behavior."""

    def test_nothing_singleton_identity(self, benchmark):
        """Benchmark that Nothing() returns the same instance."""
        nothing1 = Nothing()
        nothing2 = Nothing()
        benchmark(lambda: nothing1 is nothing2)

    def test_nothing_singleton_equality(self, benchmark):
        """Benchmark Nothing equality check."""
        nothing1 = Nothing()
        nothing2 = Nothing()
        benchmark(lambda: nothing1 == nothing2)
