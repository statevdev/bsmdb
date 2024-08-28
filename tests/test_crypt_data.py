import asyncio
import unittest
from crypt_data import Crypt


class TestCrypt(unittest.TestCase):
    def test_decrypt_data(self):
        encrypt_tuple = asyncio.run(Crypt.encrypt_data("test"))
        decrypt_tuple = Crypt.decrypt_data(encrypt_tuple[0])

        self.assertEqual(decrypt_tuple, "test")


if __name__ == "__main__":
    unittest.main()

