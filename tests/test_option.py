import unittest
from rustymonad import Option, Some, Nothing
from rustymonad import Ok, Err


class OptionTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.some_value: Option[int] = Some(1)
        self.no_value: Option[int] = Nothing()

    def test_option_unwrap(self):
        self.assertEqual(self.some_value.expect('nothing here'), 1)
        with self.assertRaises(Exception) as cm:
            self.no_value.expect('nothing here')
        self.assertEqual(str(cm.exception), 'nothing here')
    
        self.assertEqual(self.some_value.unwrap(), 1)
        with self.assertRaises(Exception) as cm:
            self.no_value.unwrap()
        self.assertEqual(str(cm.exception), 'called `Option::unwrap()` on a `Nothing` value')

        self.assertEqual(self.some_value.unwrap_or(9), 1)
        self.assertEqual(self.no_value.unwrap_or(9), 9)

    def test_option_map(self):
        self.assertEqual(self.some_value.map(lambda x: -x), Some(-1))
        self.assertEqual(self.some_value.flatmap(lambda x: Some(-x)), Some(-1))

        self.assertEqual(self.no_value.map(lambda x: -x), Nothing())
        self.assertEqual(self.no_value.flatmap(lambda x: Some(-x)), Nothing())

        numbers: list[int] = [1]
        self.some_value.inspect(lambda x: numbers.append(x + 1))
        self.assertEqual(numbers, [1, 2])
        self.no_value.inspect(lambda x: numbers.append(x + 1))
        self.assertEqual(numbers, [1, 2])


        self.assertEqual(self.some_value.and_then(lambda x: Some(str(x + 1))), Some('2'))
        self.assertEqual(self.some_value.and_then(lambda x: Nothing()), Nothing())
        self.assertEqual(self.some_value.or_else(lambda: Some(0)), Some(1))
        self.assertEqual(self.some_value.and_then(lambda x: Nothing()).or_else(lambda: Some(-1)), Some(-1))
        
        self.assertEqual(self.no_value.and_then(lambda x: Some(str(x + 1))), Nothing())
        self.assertEqual(self.no_value.or_else(lambda: Some('default value')), Some('default value'))
        self.assertEqual(self.no_value.or_else(lambda: Nothing()), Nothing())
        self.assertEqual(self.no_value.and_then(lambda x: Some(x + 1)).or_else(lambda: Some(0)), Some(0))

        self.assertEqual(self.some_value.filter(lambda x: x % 2 == 1), Some(1))
        self.assertEqual(self.some_value.filter(lambda x: x % 2 == 0), Nothing())

        self.assertEqual(self.no_value.filter(lambda x: x % 2 == 1), Nothing())
        self.assertEqual(self.no_value.filter(lambda x: x % 2 == 0), Nothing())


    def test_option_identify(self):
        self.assertTrue(self.some_value.is_some())
        self.assertFalse(self.some_value.is_nothing())
        self.assertFalse(self.no_value.is_some())
        self.assertTrue(self.no_value.is_nothing())

        self.assertTrue(self.some_value.is_some_and(lambda x: x % 2 == 1))
        self.assertFalse(self.some_value.is_some_and(lambda x: x > 1))
        self.assertFalse(self.no_value.is_some_and(lambda x: x % 2 == 1))
        self.assertFalse(self.no_value.is_some_and(lambda x: True))

    def test_option_bool(self):
        self.assertTrue(self.some_value)
        self.assertFalse(not self.some_value)
        self.assertFalse(self.no_value)
        self.assertTrue(not self.no_value)

        self.assertTrue(Some(None))
        self.assertTrue(Some(False))

    def test_option_convert(self):
        self.assertEqual(self.some_value.ok_or('error'), Ok(1))
        self.assertEqual(self.no_value.ok_or('error'), Err('error'))


class TestAndThenTypeConsistency(unittest.TestCase):
    """Test 1.1: Some.and_then type consistency"""

    def test_and_then_returns_option_type(self):
        """and_then should only accept fn that returns Option type"""
        some = Some(5)
        
        # Valid: fn returns Option
        result = some.and_then(lambda x: Some(x * 2))
        self.assertEqual(result, Some(10))
        
        result = some.and_then(lambda x: Nothing())
        self.assertEqual(result, Nothing())

    def test_and_then_type_annotation(self):
        """and_then should be annotated to return Option[U]"""
        import inspect
        sig = inspect.signature(Some.and_then)
        return_annotation = sig.return_annotation
        self.assertEqual(return_annotation, 'Option[U]')

    def test_and_then_should_not_wrap_non_option(self):
        """and_then should NOT wrap non-Option returns - fn must return Option"""
        some = Some(5)
        
        # According to the type signature, fn should return Option[U]
        # The current buggy implementation wraps non-Option values in Some()
        # This should NOT be allowed - fn must return Option
        with self.assertRaises((TypeError, AttributeError)):
            some.and_then(lambda x: x * 2)  # Returns int, not Option


class TestNothingSingleton(unittest.TestCase):
    """Test 1.2: Nothing singleton optimization"""

    def test_nothing_returns_same_instance(self):
        """Nothing() should always return the same instance"""
        n1 = Nothing()
        n2 = Nothing()
        self.assertIs(n1, n2)

    def test_nothing_multiple_calls_same_instance(self):
        """Multiple calls to Nothing() should return identical instance"""
        n1 = Nothing()
        n2 = Nothing()
        n3 = Nothing()
        self.assertIs(n1, n2)
        self.assertIs(n2, n3)

    def test_nothing_is_singleton(self):
        """Nothing should be a true singleton"""
        from rustymonad.option import Nothing
        instances = [Nothing() for _ in range(10)]
        first = instances[0]
        for inst in instances[1:]:
            self.assertIs(first, inst)

    def test_nothing_init_called_once(self):
        """__init__ should only be called once, not on every Nothing() call"""
        import subprocess
        import sys
        
        # Test in a fresh Python process where module loads fresh
        test_code = '''
import sys
from rustymonad.option import Nothing

# Track __init__ calls
init_count = 0
original_init = Nothing.__init__

def counting_init(self):
    global init_count
    init_count += 1
    original_init(self)

Nothing.__init__ = counting_init

# Create multiple instances - all should return same object
n1 = Nothing()
n2 = Nothing()
n3 = Nothing()

# Verify singleton
assert n1 is n2, "Not singleton!"
assert n2 is n3, "Not singleton!"

# __init__ should only be called once
if init_count != 1:
    print(f"FAIL: __init__ called {init_count} times, expected 1", file=sys.stderr)
    sys.exit(1)
else:
    print(f"OK: __init__ called {init_count} time")
    sys.exit(0)
'''
        
        result = subprocess.run([sys.executable, '-c', test_code], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, f"Singleton test failed: {result.stderr}{result.stdout}")


class TestOptionHash(unittest.TestCase):
    """Test Option __hash__ implementation"""

    def test_some_hash(self):
        """Some should return hash of its wrapped value"""
        self.assertEqual(hash(Some(42)), hash(42))
        self.assertEqual(hash(Some("hello")), hash("hello"))
        self.assertEqual(hash(Some((1, 2, 3))), hash((1, 2, 3)))

    def test_nothing_hash(self):
        """Nothing should return hash(None)"""
        self.assertEqual(hash(Nothing()), hash(None))

    def test_some_hash_consistency(self):
        """Same value should have same hash"""
        self.assertEqual(hash(Some(5)), hash(Some(5)))
        self.assertEqual(hash(Some("test")), hash(Some("test")))

    def test_hash_equality_with_value(self):
        """Some(value)._value should have same hash as Some(value)"""
        some = Some(100)
        self.assertEqual(hash(some), hash(some._value))

    def test_hashable_values(self):
        """Hash should work with various hashable types"""
        # Integer
        self.assertEqual(hash(Some(1)), hash(1))
        # String
        self.assertEqual(hash(Some("a")), hash("a"))
        # Tuple
        self.assertEqual(hash(Some((1, 2))), hash((1, 2)))
        # Frozen set
        self.assertEqual(hash(Some(frozenset([1, 2]))), hash(frozenset([1, 2])))

    def test_nothing_singleton_hash(self):
        """All Nothing instances should have the same hash"""
        n1 = Nothing()
        n2 = Nothing()
        self.assertEqual(hash(n1), hash(n2))


class TestOptionComparison(unittest.TestCase):
    """Test Option comparison operations (__lt__, __le__, __gt__, __ge__)"""

    # Some vs Some comparisons
    def test_some_lt_some(self):
        """Some(1) < Some(2) should be True"""
        self.assertTrue(Some(1) < Some(2))
        self.assertFalse(Some(2) < Some(1))
        self.assertFalse(Some(1) < Some(1))

    def test_some_le_some(self):
        """Some(1) <= Some(2) should be True"""
        self.assertTrue(Some(1) <= Some(2))
        self.assertTrue(Some(1) <= Some(1))
        self.assertFalse(Some(2) <= Some(1))

    def test_some_gt_some(self):
        """Some(2) > Some(1) should be True"""
        self.assertTrue(Some(2) > Some(1))
        self.assertFalse(Some(1) > Some(2))
        self.assertFalse(Some(1) > Some(1))

    def test_some_ge_some(self):
        """Some(2) >= Some(1) should be True"""
        self.assertTrue(Some(2) >= Some(1))
        self.assertTrue(Some(1) >= Some(1))
        self.assertFalse(Some(1) >= Some(2))

    # Some vs Nothing comparisons
    def test_some_vs_nothing(self):
        """Some > Nothing should always be True"""
        self.assertTrue(Some(1) > Nothing())
        self.assertTrue(Some(100) > Nothing())
        self.assertFalse(Some(1) < Nothing())
        self.assertTrue(Some(1) >= Nothing())
        self.assertTrue(Some(1) <= Some(1))  # Equal should be True

    def test_some_le_nothing(self):
        """Some <= Nothing should be False"""
        self.assertFalse(Some(1) <= Nothing())

    def test_some_ge_nothing(self):
        """Some >= Nothing should be True"""
        self.assertTrue(Some(1) >= Nothing())

    # Nothing vs Some comparisons
    def test_nothing_vs_some(self):
        """Nothing < Some should always be True"""
        self.assertTrue(Nothing() < Some(1))
        self.assertFalse(Nothing() > Some(1))
        self.assertTrue(Nothing() <= Some(1))
        self.assertFalse(Nothing() >= Some(1))

    def test_nothing_le_some(self):
        """Nothing <= Some should be True"""
        self.assertTrue(Nothing() <= Some(1))

    def test_nothing_ge_some(self):
        """Nothing >= Some should be False"""
        self.assertFalse(Nothing() >= Some(1))

    # Nothing vs Nothing comparisons
    def test_nothing_lt_nothing(self):
        """Nothing < Nothing should be False"""
        self.assertFalse(Nothing() < Nothing())

    def test_nothing_le_nothing(self):
        """Nothing <= Nothing should be True (equal)"""
        self.assertTrue(Nothing() <= Nothing())

    def test_nothing_gt_nothing(self):
        """Nothing > Nothing should be False"""
        self.assertFalse(Nothing() > Nothing())

    def test_nothing_ge_nothing(self):
        """Nothing >= Nothing should be True (equal)"""
        self.assertTrue(Nothing() >= Nothing())

    # String comparison
    def test_some_string_comparison(self):
        """String Some values should be comparable"""
        self.assertTrue(Some("a") < Some("b"))
        self.assertTrue(Some("b") > Some("a"))
        self.assertTrue(Some("a") <= Some("a"))
        self.assertTrue(Some("a") >= Some("a"))

    # Test with custom objects that support comparison
    def test_some_custom_comparison(self):
        """Some with custom comparable objects"""
        self.assertTrue(Some(5) < Some(10))
        self.assertTrue(Some(10) > Some(5))
        self.assertTrue(Some(5) <= Some(10))
        self.assertTrue(Some(10) >= Some(5))

    # Test TypeError for incompatible types
    def test_comparison_type_error(self):
        """Comparison with incompatible types should raise TypeError"""
        with self.assertRaises(TypeError):
            Some(1) < "string"
        
        with self.assertRaises(TypeError):
            Some(1) <= 123
        
        with self.assertRaises(TypeError):
            Nothing() > []


if __name__ == '__main__':
    unittest.main()
