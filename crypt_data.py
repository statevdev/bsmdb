from cryptography.fernet import Fernet
try:
    from config import config
except ImportError:
    from test_config import test_config
    config = test_config


class Crypt:
    """
    Класс для шифрования и дешифрования данных с использованием Fernet.
    """
    @staticmethod
    def decrypt_data(data: str) -> str:
        """
        Дешифрует зашифрованные данные.

        Этот метод принимает зашифрованные данные в виде строки и возвращает
        их в расшифрованном виде.

        Параметры:
        data (str): Зашифрованные данные в виде строки.

        Возвращает:
        str: Расшифрованные данные в виде строки.
        """
        fernet = Fernet(config['db']['key'])
        return fernet.decrypt(data.encode()).decode()

    @staticmethod
    async def encrypt_data(*args: str) -> tuple:
        """
        Шифрует данные.

        Этот метод принимает произвольное количество аргументов и возвращает
        их в зашифрованном виде в виде кортежа.

        Параметры:
        *args (str): Данные для шифрования.

        Возвращает:
        tuple: Кортеж зашифрованных данных.
        """
        fernet = Fernet(config['db']['key'])
        return tuple(fernet.encrypt(str(arg).encode()).decode() for arg in args)
