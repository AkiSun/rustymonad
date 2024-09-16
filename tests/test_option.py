import unittest
from src.rustymonad import Option, Some, Nothing
from src.rustymonad import Ok, Err


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


if __name__ == '__main__':
    unittest.main()
