import unittest
from src.rustymonad import Result, Ok, Err
from src.rustymonad import Some, Nothing


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


if __name__ == '__main__':
    unittest.main()
