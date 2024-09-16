import unittest
from src.rustymonad import Result, Ok, Err
from src.rustymonad import DoRet, do_notation, try_notation


number = int | float


class ResultUtils:
    @staticmethod
    def safe_div(x: number, y: number) -> Result[float, str]:
        if y == 0:
            return Err('division by zero')
        return Ok(x / y)

    @staticmethod
    def safe_sqrt(x: number) -> Result[float, str]:
        import math
        if x < 0:
            return Err('sqrt negative')
        return Ok(math.sqrt(x))
    

class UtilsTestCase(unittest.TestCase):
    def test_utils_do_notation(self):

        @do_notation
        def calc_process(a: number, b: number) -> DoRet[Result[float, str]]:
            root = yield ResultUtils.safe_sqrt(a)
            quotient = yield ResultUtils.safe_div(root, b)
            return Ok(quotient)
        
        self.assertEqual(calc_process(9, 2), Ok(1.5))
        self.assertEqual(calc_process(9, 0), Err('division by zero'))
        self.assertEqual(calc_process(-9, 2), Err('sqrt negative'))
        self.assertEqual(calc_process(-9, 0), Err('sqrt negative'))

    def test_utils_try_notation(self):

        @try_notation
        def div_with_try(x: number, y: number) -> float:
            return x / y
        
        self.assertEqual(div_with_try(1, 2), Ok(0.5))
        self.assertEqual(div_with_try(1, 0), Err('division by zero'))


if __name__ == '__main__':
    unittest.main()
