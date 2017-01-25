###############################################################################
# System LIB
###############################################################################
import base64
import hashlib
import unittest
###############################################################################
# PyCrypto LIB
###############################################################################
from Crypto import Random
from Crypto.Cipher import AES
"""
Need to install on linux
1. gcc (installed by yum)
2. python-devel (installed by yum)
3. libevent-devel (installed by yum)
4. PyCrypto (installed by pip)
Need to install on Window
1. http://www.voidspace.org.uk/python/modules.shtml#pycrypto
"""


# References
# http://www.imcore.net/encrypt-decrypt-aes256-c-objective-ios-iphone-ipad-php-java-android-perl-javascript/
# http://stackoverflow.com/questions/12562021/aes-decryption-padding-with-pkcs5-python
# http://stackoverflow.com/questions/12524994/encrypt-decrypt-using-pycrypto-aes-256
# http://www.di-mgt.com.au/cryptopad.html
# https://github.com/dlitz/pycrypto
BS = 16
pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS).encode()
unpad = lambda s: s[:-ord(s[len(s)-1:])]
def iv():
    """
    The initialization vector to use for encryption or decryption.
    It is ignored for MODE_ECB and MODE_CTR.
    """
    return chr(0) * 16



class MongAESCipher(object):
    """
    https://github.com/dlitz/pycrypto
    """
    def __init__(self, key):
        # key MUST be 32 lenth
        if len(key) > 32:
            key = key[0:32]
        else:
            key = key.rjust(32,'0')
        self.key = key
        #self.key = hashlib.sha256(key.encode()).digest()
    def encrypt(self, message):
        """
        It is assumed that you use Python 3.0+
        , so plaintext's type must be str type(== unicode).
        """
        message = message.encode()
        raw = pad(message)
        cipher = AES.new(self.key, AES.MODE_CBC, iv())
        enc = cipher.encrypt(raw)
        return base64.b64encode(enc).decode('utf-8')
    def decrypt(self, enc):
        enc = base64.b64decode(enc)
        cipher = AES.new(self.key, AES.MODE_CBC, iv())
        dec = cipher.decrypt(enc)
        return unpad(dec).decode('utf-8')


###############################################################################
## For Testing
###############################################################################
class MongCryptTestCase(unittest.TestCase):
    
    cipher1 = None
    cipher2 = None
    
    key1 = "123456"
    key2 = "1234567890123456789012345678901234567890"
    data = "data=1;\ndata2&\n"
        
    def setUp(self):
        self.cipher1 = MongAESCipher(self.key1)
        self.cipher2 = MongAESCipher(self.key2)
        
    def test_1_encrypt_decrypt(self):
        enc_data1 = self.cipher1.encrypt(self.data)
        self.assertEquals(self.cipher1.decrypt(enc_data1), self.data)
        
        enc_data2 = self.cipher2.encrypt(self.data)
        self.assertEquals(self.cipher2.decrypt(enc_data2), self.data)
        
        self.assertNotEquals(enc_data1, enc_data2)
            
if __name__ == "__main__":
    unittest.main()
