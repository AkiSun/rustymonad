import unittest
from rustymonad import Result, Ok, Err
from rustymonad import Some, Nothing


class ResultTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.ok_value: Result[int, str] = Ok(100)
        self.err_value: Result[int, str] = Err('something wrong')

    def test_result_unwrap(self):
        self.assertEqual(self.ok_value.expect('opration failed'), 100)
        with self.assertRaises(Exception) as cm:
            self.err_value.expect('opration failed')
        self.assertEqual(str(cm.exception), 'opration failed: something wrong')

        self.assertEqual(self.err_value.expect_err('opration failed'), 'something wrong')
        with self.assertRaises(Exception) as cm:
            self.ok_value.expect_err('opration failed')
        self.assertEqual(str(cm.exception), 'opration failed: 100')
    
        self.assertEqual(self.ok_value.unwrap(), 100)
        with self.assertRaises(Exception) as cm:
            self.err_value.unwrap()
        self.assertEqual(str(cm.exception), 'something wrong')

        self.assertEqual(self.err_value.unwrap_err(), 'something wrong')
        with self.assertRaises(Exception) as cm:
            self.ok_value.unwrap_err()
        self.assertEqual(str(cm.exception), '100')

        self.assertEqual(self.ok_value.unwrap_or(-1), 100)
        self.assertEqual(self.err_value.unwrap_or(-1), -1)

    def test_result_map(self):
        self.assertEqual(self.ok_value.map(lambda x: -x), Ok(-100))
        self.assertEqual(self.ok_value.flatmap(lambda x: Ok(-x)), Ok(-100))

        self.assertEqual(self.err_value.map(lambda x: -x), Err('something wrong'))
        self.assertEqual(self.err_value.flatmap(lambda x: Ok(-x)), Err('something wrong'))

        array: list[int | str] = [1]
        self.ok_value.inspect(lambda x: array.append(x))
        self.assertEqual(array, [1, 100])
        self.err_value.inspect(lambda x: array.append(x))
        self.assertEqual(array, [1, 100])

        self.ok_value.inspect_err(lambda x: array.extend(x.split(' ')))
        self.assertEqual(array, [1, 100])
        self.err_value.inspect_err(lambda x: array.extend(x.split(' ')))
        self.assertEqual(array, [1, 100, 'something', 'wrong'])

        self.assertEqual(self.ok_value.and_then(lambda x: Ok(str(x + 1))), Ok('101'))
        self.assertEqual(self.ok_value.and_then(lambda x: Err('another error')), Err('another error'))
        self.assertEqual(self.ok_value.or_else(lambda x: Ok(str(x + 1))), Ok(100))
        self.assertEqual(self.ok_value.and_then(lambda x: Ok(x + 1)).or_else(lambda x: Ok(f'success {x}')), Ok(101))
        self.assertEqual(self.ok_value.and_then(lambda x: Err(x + 1)).or_else(lambda x: Ok(f'success {x}')), Ok('success 101'))
        
        self.assertEqual(self.err_value.and_then(lambda x: Err('another error')), Err('something wrong'))
        self.assertEqual(self.err_value.or_else(lambda x: Err('another error')), Err('another error'))
        self.assertEqual(self.err_value.or_else(lambda x: Ok(x + ' resolved!')), Ok('something wrong resolved!'))
        self.assertEqual(self.err_value.and_then(lambda x: Ok(x + 1)).or_else(lambda x: Ok(x + ' logged!')), Ok('something wrong logged!'))

    def test_result_identify(self):
        self.assertTrue(self.ok_value.is_ok())
        self.assertFalse(self.ok_value.is_err())
        self.assertFalse(self.err_value.is_ok())
        self.assertTrue(self.err_value.is_err())

        self.assertTrue(self.ok_value.is_ok_and(lambda x: x % 2 == 0))
        self.assertFalse(self.ok_value.is_ok_and(lambda x: x < 0))
        self.assertFalse(self.ok_value.is_err_and(lambda x: x.endswith('wrong')))

        self.assertFalse(self.err_value.is_ok_and(lambda x: x % 2 == 0))
        self.assertTrue(self.err_value.is_err_and(lambda x: x.endswith('wrong')))
        self.assertFalse(self.err_value.is_err_and(lambda x: x.startswith('hello')))

    def test_result_bool(self):
        self.assertTrue(self.ok_value)
        self.assertFalse(not self.ok_value)
        self.assertFalse(self.err_value)
        self.assertTrue(not self.err_value)

        self.assertTrue(Ok(None))
        self.assertTrue(Ok(False))

    def test_result_convert(self):
        self.assertEqual(self.ok_value.ok(), Some(100))
        self.assertEqual(self.ok_value.err(), Nothing())

        self.assertEqual(self.err_value.ok(), Nothing())
        self.assertEqual(self.err_value.err(), Some('something wrong'))


class TestResultComparison(unittest.TestCase):
    """Test Result comparison operations (__lt__, __le__, __gt__, __ge__)"""

    # Ok vs Ok comparisons
    def test_ok_lt_ok(self):
        """Ok(1) < Ok(2) should be True"""
        self.assertTrue(Ok(1) < Ok(2))
        self.assertFalse(Ok(2) < Ok(1))
        self.assertFalse(Ok(1) < Ok(1))

    def test_ok_le_ok(self):
        """Ok(1) <= Ok(2) should be True"""
        self.assertTrue(Ok(1) <= Ok(2))
        self.assertTrue(Ok(1) <= Ok(1))
        self.assertFalse(Ok(2) <= Ok(1))

    def test_ok_gt_ok(self):
        """Ok(2) > Ok(1) should be True"""
        self.assertTrue(Ok(2) > Ok(1))
        self.assertFalse(Ok(1) > Ok(2))
        self.assertFalse(Ok(1) > Ok(1))

    def test_ok_ge_ok(self):
        """Ok(2) >= Ok(1) should be True"""
        self.assertTrue(Ok(2) >= Ok(1))
        self.assertTrue(Ok(1) >= Ok(1))
        self.assertFalse(Ok(1) >= Ok(2))

    # Err vs Err comparisons
    def test_err_lt_err(self):
        """Err('a') < Err('b') should be True"""
        self.assertTrue(Err('a') < Err('b'))
        self.assertFalse(Err('b') < Err('a'))
        self.assertFalse(Err('a') < Err('a'))

    def test_err_le_err(self):
        """Err('a') <= Err('b') should be True"""
        self.assertTrue(Err('a') <= Err('b'))
        self.assertTrue(Err('a') <= Err('a'))
        self.assertFalse(Err('b') <= Err('a'))

    def test_err_gt_err(self):
        """Err('b') > Err('a') should be True"""
        self.assertTrue(Err('b') > Err('a'))
        self.assertFalse(Err('a') > Err('b'))
        self.assertFalse(Err('a') > Err('a'))

    def test_err_ge_err(self):
        """Err('b') >= Err('a') should be True"""
        self.assertTrue(Err('b') >= Err('a'))
        self.assertTrue(Err('a') >= Err('a'))
        self.assertFalse(Err('a') >= Err('b'))

    # Ok vs Err comparisons
    def test_ok_vs_err(self):
        """Ok < Err should always be True"""
        self.assertTrue(Ok(1) < Err("error"))
        self.assertFalse(Ok(1) > Err("error"))
        self.assertTrue(Ok(1) <= Err("error"))
        self.assertFalse(Ok(1) >= Err("error"))

    def test_ok_le_err(self):
        """Ok <= Err should be True (Ok is less than Err)"""
        self.assertTrue(Ok(1) <= Err("error"))

    def test_ok_ge_err(self):
        """Ok >= Err should be False (Ok is less than Err)"""
        self.assertFalse(Ok(1) >= Err("error"))

    # Err vs Ok comparisons
    def test_err_vs_ok(self):
        """Err > Ok should always be True"""
        self.assertTrue(Err("error") > Ok(1))
        self.assertFalse(Err("error") < Ok(1))
        self.assertTrue(Err("error") >= Ok(1))
        self.assertFalse(Err("error") <= Ok(1))

    def test_err_le_ok(self):
        """Err <= Ok should be False (Err is greater than Ok)"""
        self.assertFalse(Err("error") <= Ok(1))

    def test_err_ge_ok(self):
        """Err >= Ok should be True (Err is greater than Ok)"""
        self.assertTrue(Err("error") >= Ok(1))

    # String comparison
    def test_ok_string_comparison(self):
        """Ok string values should be comparable"""
        self.assertTrue(Ok("a") < Ok("b"))
        self.assertTrue(Ok("b") > Ok("a"))
        self.assertTrue(Ok("a") <= Ok("a"))
        self.assertTrue(Ok("a") >= Ok("a"))

    def test_err_string_comparison(self):
        """Err string values should be comparable"""
        self.assertTrue(Err("a") < Err("b"))
        self.assertTrue(Err("b") > Err("a"))
        self.assertTrue(Err("a") <= Err("a"))
        self.assertTrue(Err("a") >= Err("a"))

    # Test with numeric error values
    def test_err_numeric_comparison(self):
        """Err with numeric values should be comparable"""
        self.assertTrue(Err(1) < Err(2))
        self.assertTrue(Err(2) > Err(1))
        self.assertTrue(Err(1) <= Err(1))
        self.assertTrue(Err(1) >= Err(1))

    # Test TypeError for incompatible types
    def test_comparison_type_error(self):
        """Comparison with incompatible types should raise TypeError"""
        with self.assertRaises(TypeError):
            Ok(1) < "string"
        
        with self.assertRaises(TypeError):
            Ok(1) <= 123
        
        with self.assertRaises(TypeError):
            Err("error") > []


if __name__ == '__main__':
    unittest.main()
