import os
from typing import Union

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding as asym_padding
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM


# Note: AES EAX mode specifically might not be directly supported by the `cryptography` library as of the last update.
# As an alternative, AES GCM can be used, which is another AEAD mode with similar properties.
# The following example will use AES GCM for demonstration purposes, adjusting as needed for your use case.
# from cryptography.hazmat.primitives import constant_time


class OpenSSLCrypto:
    def __init__(self):
        self.key: Union[bytes, None] = None
        self.public_key: Union[bytes, None] = None
        self.private_key: Union[bytes, None] = None
        self.iv = None
        self.mode = None
        self.cipher = None
        self.backend = default_backend()

    @staticmethod
    def load_rsa_private_key_from_pem(file_path, password=None):
        """
        Load an RSA private key from a PEM file.
        """
        with open(file_path, "rb") as key_file:
            private_key = serialization.load_pem_private_key(
                key_file.read(),
                password=password,
                backend=default_backend()
            )
        return private_key

    @staticmethod
    def load_rsa_public_key_from_pem(file_path):
        """
        Load an RSA public key from a PEM file.
        """
        with open(file_path, "rb") as key_file:
            public_key = serialization.load_pem_public_key(
                key_file.read(),
                backend=default_backend()
            )
        return public_key

    @staticmethod
    def load_rsa_private_key_from_der(file_path, password=None):
        """
        Load an RSA private key from a DER file.
        """
        with open(file_path, "rb") as key_file:
            private_key = serialization.load_der_private_key(
                key_file.read(),
                password=password,
                backend=default_backend()
            )
        return private_key

    @staticmethod
    def load_rsa_public_key_from_der(file_path):
        """
        Load an RSA public key from a DER file.
        """
        with open(file_path, "rb") as key_file:
            public_key = serialization.load_der_public_key(
                key_file.read(),
                backend=default_backend()
            )
        return public_key

    def secure_erase(self, attribute_name):
        """
        Securely erases a key stored in the attribute specified by attribute_name.
        The attribute is expected to be of type bytes.
        """
        attribute = getattr(self, attribute_name, None)
        if attribute is not None:
            # Overwrite the memory area with the same length of zeros
            # Note: This is an attempt to reduce the risk but may not be completely effective
            # due to Python's memory management.
            zeroed_bytes = bytes(len(attribute))
            setattr(self, attribute_name, zeroed_bytes)
            del attribute

    def clear_keys(self):
        """
        Attempts to clear keys more securely by overwriting them with zeros.
        """
        self.secure_erase('key')
        self.secure_erase('publicKey')
        self.secure_erase('privateKey')
        # After overwriting, set them to None
        self.key = None
        self.public_key = None
        self.private_key = None

    @staticmethod
    def random_key256():
        """
        Generates a Random key of 256 bits
        Returns 256-bit random key
        """
        return os.urandom(32)

    @staticmethod
    def random_key128():
        """
        Generates a Random key of 128 bits
        returns 128-bit random key
        """
        return os.urandom(16)

    def sha256(self, msg):
        """
        SHA256 digest
        @mesg is the data to hash
        returns SHA256 of a message
        """
        digest = hashes.Hash(hashes.SHA256(), backend=self.backend)
        digest.update(msg)
        return digest.finalize()

    def aes_encrypt_cbc(self, key, plaintext):
        """
        AES-CBC encryption, encrypts data
        """
        iv = os.urandom(16)
        padder = padding.PKCS7(128).padder()
        padded_data = padder.update(plaintext) + padder.finalize()
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=self.backend)
        encryptor = cipher.encryptor()
        cipher_text = encryptor.update(padded_data) + encryptor.finalize()
        return iv + cipher_text  # Prepend IV for use in decryption

    def aes_decrypt_cbc(self, key, cipherdata):
        """
        AES-CBC decryption, decrypts data
        """
        iv = cipherdata[:16]
        cipher_text = cipherdata[16:]
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=self.backend)
        decryptor = cipher.decryptor()
        padded_plaintext = decryptor.update(cipher_text) + decryptor.finalize()
        unpadder = padding.PKCS7(128).unpadder()
        plaintext = unpadder.update(padded_plaintext) + unpadder.finalize()
        return plaintext

    @staticmethod
    def aes_encrypt_eax(key, plaintext, associated_data=None):
        """
        AES encryption in EAX mode (using GCM as a stand-in for this example)
        @key should be a 128, 192, or 256-bit key (16, 24, or 32 bytes)
        @plaintext is the data to encrypt
        @associated_data is additional data authenticated but not encrypted,
        can be None
        Returns a tuple of (nonce, ciphertext, tag)
        """
        # AES GCM mode is used here as an example. Adjust according to your needs
        aesgcm = AESGCM(key)
        nonce = os.urandom(12)  # GCM standard nonce size
        ciphertext = aesgcm.encrypt(nonce, plaintext, associated_data)
        return nonce, ciphertext

    @staticmethod
    def aes_decrypt_eax(key, nonce, ciphertext, associated_data=None):
        """
        AES decryption in EAX mode (using GCM as a stand-in for this example)
        @key should be a 128, 192, or 256-bit key (16, 24, or 32 bytes)
        @nonce is the nonce value used during encryption
        @ciphertext is the encrypted data
        @associated_data is additional data authenticated but not encrypted,
        must be the same as what was passed to the encrypt function
        Returns the plaintext if the authentication tag is valid, raises an
        exception otherwise
        """
        aesgcm = AESGCM(key)
        plaintext = aesgcm.decrypt(nonce, ciphertext, associated_data)
        return plaintext

    def rsa_generate_key(self, key_length=2048):
        """
        Generates an RSA key pair
        """
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=key_length,
            backend=self.backend
        )
        return private_key

    @staticmethod
    def rsa_encrypt(public_key, plaintext):
        """
        Encrypts plaintext using RSA public key and OAEP padding.
        """
        ciphertext = public_key.encrypt(
            plaintext,
            asym_padding.OAEP(
                mgf=asym_padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        return ciphertext

    @staticmethod
    def rsa_decrypt(private_key, ciphertext):
        """
        Decrypts ciphertext using RSA private key and OAEP padding.
        """
        plaintext = private_key.decrypt(
            ciphertext,
            asym_padding.OAEP(
                mgf=asym_padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )

        return plaintext
