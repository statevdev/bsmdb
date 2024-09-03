from cryptography.fernet import Fernet
try:
    from config import config
except ImportError:
    from test_config import test_config
    config = test_config


class Crypt:
    @staticmethod
    def decrypt_data(data):
        fernet = Fernet(config['db']['key'])
        return fernet.decrypt(data.encode()).decode()

    @staticmethod
    async def encrypt_data(*args):
        fernet = Fernet(config['db']['key'])
        return tuple(fernet.encrypt(str(arg).encode()).decode() for arg in args)
