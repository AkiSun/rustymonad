"""Additional tests to improve coverage for result.py and utils.py."""
import unittest
from rustymonad import (
    Ok, Err, Result, Some, Nothing,
    do_notation, try_notation, DoRet,
    DoNotationError,
)
from rustymonad.errors import (
    UnwrapError, ExpectError, UnwrapUncheckedError,
)


class TestResultOkMethods(unittest.TestCase):
    """Cover Ok methods that are untested."""

    def test_ok_expect_err(self):
        with self.assertRaises(ExpectError):
            Ok(10).expect_err("should fail")

    def test_ok_unwrap_err(self):
        with self.assertRaises(UnwrapError):
            Ok(10).unwrap_err()

    def test_ok_unwrap_or(self):
        self.assertEqual(Ok(10).unwrap_or(0), 10)

    def test_ok_unwrap_or_else(self):
        self.assertEqual(Ok(10).unwrap_or_else(lambda: 0), 10)

    def test_ok_map_err(self):
        r = Ok(10).map_err(lambda e: e.upper())
        self.assertEqual(r, Ok(10))

    def test_ok_unwrap_unchecked(self):
        self.assertEqual(Ok(42).unwrap_unchecked(), 42)

    def test_ok_and_then(self):
        r = Ok(5).and_then(lambda x: Ok(x * 2))
        self.assertEqual(r, Ok(10))

    def test_ok_or_else(self):
        r = Ok(5).or_else(lambda: Ok(0))
        self.assertEqual(r, Ok(5))

    def test_ok_inspect(self):
        captured = []
        Ok(5).inspect(lambda x: captured.append(x))
        self.assertEqual(captured, [5])

    def test_ok_inspect_err(self):
        captured = []
        Ok(5).inspect_err(lambda x: captured.append(x))
        self.assertEqual(captured, [])

    def test_ok_is_ok_and(self):
        self.assertTrue(Ok(5).is_ok_and(lambda x: x > 0))
        self.assertFalse(Ok(-1).is_ok_and(lambda x: x > 0))

    def test_ok_is_err_and(self):
        self.assertFalse(Ok(5).is_err_and(lambda x: True))

    def test_ok_ok_method(self):
        self.assertEqual(Ok(5).ok(), Some(5))

    def test_ok_err_method(self):
        self.assertEqual(Ok(5).err(), Nothing())

    def test_ok_map(self):
        self.assertEqual(Ok(5).map(lambda x: x + 1), Ok(6))

    def test_ok_flatmap(self):
        self.assertEqual(Ok(5).flatmap(lambda x: Ok(x + 1)), Ok(6))

    def test_ok_bool(self):
        self.assertTrue(bool(Ok(5)))

    def test_ok_eq(self):
        self.assertEqual(Ok(5), Ok(5))
        self.assertNotEqual(Ok(5), Ok(6))
        self.assertNotEqual(Ok(5), Err(5))

    def test_ok_repr(self):
        self.assertEqual(repr(Ok(5)), "Result::Ok(5)")

    def test_ok_rshift(self):
        r = Ok(5) >> (lambda x: Ok(x * 3))
        self.assertEqual(r, Ok(15))

    def test_ok_is_ok(self):
        self.assertTrue(Ok(5).is_ok())

    def test_ok_is_err(self):
        self.assertFalse(Ok(5).is_err())

    def test_ok_hash(self):
        s = {Ok(1), Ok(1), Ok(2)}
        self.assertEqual(len(s), 2)


class TestResultErrMethods(unittest.TestCase):
    """Cover Err methods that are untested."""

    def test_err_expect(self):
        with self.assertRaises(ExpectError):
            Err("bad").expect("should fail")

    def test_err_expect_err(self):
        self.assertEqual(Err("bad").expect_err("msg"), "bad")

    def test_err_unwrap(self):
        with self.assertRaises(UnwrapError):
            Err("bad").unwrap()

    def test_err_unwrap_err(self):
        self.assertEqual(Err("bad").unwrap_err(), "bad")

    def test_err_unwrap_or(self):
        self.assertEqual(Err("bad").unwrap_or(42), 42)

    def test_err_unwrap_or_else(self):
        self.assertEqual(Err("bad").unwrap_or_else(lambda: 42), 42)

    def test_err_map_err(self):
        r = Err("bad").map_err(lambda e: e.upper())
        self.assertEqual(r, Err("BAD"))

    def test_err_unwrap_unchecked(self):
        with self.assertRaises(UnwrapUncheckedError):
            Err("bad").unwrap_unchecked()

    def test_err_and_then(self):
        r = Err("bad").and_then(lambda x: Ok(x * 2))
        self.assertEqual(r, Err("bad"))

    def test_err_or_else(self):
        r = Err("bad").or_else(lambda e: Ok(0))
        self.assertEqual(r, Ok(0))

    def test_err_inspect(self):
        captured = []
        Err("bad").inspect(lambda x: captured.append(x))
        self.assertEqual(captured, [])

    def test_err_inspect_err(self):
        captured = []
        Err("bad").inspect_err(lambda x: captured.append(x))
        self.assertEqual(captured, ["bad"])

    def test_err_is_ok_and(self):
        self.assertFalse(Err("bad").is_ok_and(lambda x: True))

    def test_err_is_err_and(self):
        self.assertTrue(Err("bad").is_err_and(lambda x: x == "bad"))

    def test_err_ok_method(self):
        self.assertEqual(Err("bad").ok(), Nothing())

    def test_err_err_method(self):
        self.assertEqual(Err("bad").err(), Some("bad"))

    def test_err_map(self):
        self.assertEqual(Err("bad").map(lambda x: x + 1), Err("bad"))

    def test_err_flatmap(self):
        self.assertEqual(Err("bad").flatmap(lambda x: Ok(x + 1)), Err("bad"))

    def test_err_bool(self):
        self.assertFalse(bool(Err("bad")))

    def test_err_eq(self):
        self.assertEqual(Err("bad"), Err("bad"))
        self.assertNotEqual(Err("bad"), Err("other"))
        self.assertNotEqual(Err("bad"), Ok("bad"))

    def test_err_repr(self):
        self.assertEqual(repr(Err("bad")), "Result::Err('bad')")

    def test_err_rshift(self):
        r = Err("bad") >> (lambda x: Ok(x * 3))
        self.assertEqual(r, Err("bad"))

    def test_err_is_ok(self):
        self.assertFalse(Err("bad").is_ok())

    def test_err_is_err(self):
        self.assertTrue(Err("bad").is_err())

    def test_err_hash(self):
        s = {Err("a"), Err("a"), Err("b")}
        self.assertEqual(len(s), 2)


class TestResultTryCatch(unittest.TestCase):
    """Cover Result.try_catch static method."""

    def test_try_catch_success(self):
        @Result.try_catch
        def safe_div(a, b):
            return a / b

        self.assertEqual(safe_div(10, 2), Ok(5.0))

    def test_try_catch_failure(self):
        @Result.try_catch
        def safe_div(a, b):
            return a / b

        result = safe_div(10, 0)
        self.assertTrue(result.is_err())


class TestDoNotation(unittest.TestCase):
    """Cover do_notation edge cases."""

    def test_do_notation_ok_chain(self):
        @do_notation
        def compute() -> DoRet[Result]:
            x = yield Ok(1)
            y = yield Ok(2)
            return Ok(x + y)

        self.assertEqual(compute(), Ok(3))

    def test_do_notation_err_short_circuit(self):
        @do_notation
        def compute() -> DoRet[Result]:
            x = yield Ok(1)
            y = yield Err("fail")
            return Ok(x + y)

        self.assertEqual(compute(), Err("fail"))

    def test_do_notation_non_generator(self):
        @do_notation
        def bad():
            return 42

        with self.assertRaises(TypeError):
            bad()

    def test_do_notation_type_error_in_yield(self):
        @do_notation
        def bad() -> DoRet[Result]:
            x = yield "not a monad"
            return Ok(x)

        with self.assertRaises((TypeError, DoNotationError)):
            bad()

    def test_do_notation_exception_in_body(self):
        @do_notation
        def bad() -> DoRet[Result]:
            x = yield Ok(1)
            raise ValueError("boom")
            return Ok(x)

        with self.assertRaises(DoNotationError):
            bad()


class TestTryNotation(unittest.TestCase):
    """Cover try_notation."""

    def test_try_notation_success(self):
        @try_notation
        def add(a, b):
            return a + b

        self.assertEqual(add(1, 2), Ok(3))

    def test_try_notation_failure(self):
        @try_notation
        def fail():
            raise RuntimeError("oops")

        result = fail()
        self.assertTrue(result.is_err())
        self.assertEqual(result.unwrap_err(), "oops")


if __name__ == "__main__":
    unittest.main()
