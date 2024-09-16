import unittest
from src.rustymonad import Monad


class MonadTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.number_monad = Monad(1)

    def test_monad_unwrap(self):
        self.assertEqual(self.number_monad.unwrap(), 1)

    def test_monad_map(self):
        self.assertEqual(self.number_monad.map(lambda x: x + 1), Monad(2))
        self.assertEqual(self.number_monad.map(lambda x: 10), Monad(10))

        self.assertEqual(self.number_monad.flatmap(lambda x: Monad(x - 1)), Monad(0))
        self.assertEqual(self.number_monad.flatmap(lambda x: Monad(5)), Monad(5))

    def test_monad_magic(self):
        self.assertTrue(self.number_monad)
        self.assertFalse(not self.number_monad)

        self.assertEqual(self.number_monad, Monad(1))
        self.assertNotEqual(self.number_monad, Monad(0))

        self.assertEqual(self.number_monad >> (lambda x: Monad(x + 2)) >> (lambda x: Monad(x * x)), Monad(9))
        

if __name__ == '__main__':
    unittest.main()
