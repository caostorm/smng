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
        self._key = m.digest()
        self._mode = AES.MODE_CBC
        self._crypto = AES.new(self._key, self._mode, self._key)

    def _zero_padding(self, text):
        keylen = len(self._key)
        pading_count = keylen - len(text) % keylen
        text += '\0' * pading_count
        return text

    def encrypt(self, text):
        text = self._zero_padding(text)
        crypt_data = self._crypto.encrypt(text)
        if sys.version_info.major == 2:
            return str(base64.b64encode(crypt_data))
        else:
            return str(base64.b64encode(crypt_data), 'utf-8')

    def decrypt(self, text):
        crypt_data = base64.b64decode(text)
        plan_text = self._crypto.decrypt(crypt_data)
        if sys.version_info.major == 2:
            return str(plan_text).rstrip('\0')
        else:
            return str(plan_text, 'utf-8').rstrip('\0')

