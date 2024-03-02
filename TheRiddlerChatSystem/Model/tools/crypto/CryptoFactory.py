from TheRiddlerChatSystem.Model.tools.crypto.cryptoutils import CryptoTools
from TheRiddlerChatSystem.Model.tools.crypto.opensslutils import OpenSSLCrypto

class CryptoFactory:
    @staticmethod
    def getCryptoTools(type):
        if type == "Pycrypto":
            return CryptoTools()
        elif type == "OpenSSL":
            return OpenSSLCrypto()
        else:
            raise ValueError("Unsupported crypto type")
