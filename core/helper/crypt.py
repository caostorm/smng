#coding=utf-8
from Crypto.Cipher import AES
import hashlib
import base64
import binascii
import sys

class pwd_crypt:
    def __init__(self):
        m = hashlib.md5()
        m.update("a(7s.a^&m,1".encode('utf-8'))
        self.__key__ = m.digest()
        self.__mode__ = AES.MODE_CBC
        self.__crypto__ = AES.new(self.__key__, self.__mode__, self.__key__)

    def __zero_padding__(self, text):
        keylen = len(self.__key__)
        pading_count = keylen - len(text) % keylen
        text += '\0' * pading_count
        return text

    def encrypt(self, text):
        text = self.__zero_padding__(text)
        crypt_data = self.__crypto__.encrypt(text)
        if sys.version_info.major == 2:
            return str(base64.b64encode(crypt_data))
        else:
            return str(base64.b64encode(crypt_data), 'utf-8')

    def decrypt(self, text):
        crypt_data = base64.b64decode(text)
        plan_text = self.__crypto__.decrypt(crypt_data)
        if sys.version_info.major == 2:
            return str(plan_text).rstrip('\0')
        else:
            return str(plan_text, 'utf-8').rstrip('\0')

