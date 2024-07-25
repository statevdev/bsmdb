from cryptography.fernet import Fernet
from bsmdb.config import config


class Crypt:
    @staticmethod
    def decrypt_data(data):
        fernet = Fernet(config['db']['key'])
        return fernet.decrypt(data.encode()).decode()

    @staticmethod
    async def tuple_encrypter(*args):
        fernet = Fernet(config['db']['key'])
        return tuple(fernet.encrypt(str(arg).encode()).decode() for arg in args)
