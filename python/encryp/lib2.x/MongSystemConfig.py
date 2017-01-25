###############################################################################
## System LIB
###############################################################################
import sys, os
from subprocess import Popen, PIPE
from ConfigParser import ConfigParser, NoSectionError
import unittest
from StringIO import StringIO
###############################################################################
## Mong LIB
###############################################################################
from MongCommon import file_write, file_read
from MongClass import MongClass
from MongConfig import MongConfig
from MongCrypt import MongAESCipher
################################################################################
## rubin_system.config sample (encrypted)
## IMPORTANT : MUST include "Head" Section and "ver" value
################################################################################
#[{SectionName}]
#{Name}:{Value}
################################################################################


"""
[Head]  ==> mandatory
ver:0.99  ==> mandatory

[S3]
s3_access_key:abcdef
s3_secret_key:12394840329043294230948230948092348093284032

[MySql]
db_user:user1
db_password:password1
db_name:db1
"""

################################################################################
## Mong System Config Class
################################################################################
class MongSystemConfig(MongClass):
    config = None
    ver = None
    is_load = False      

    ###########################################################################
    ## init
    ###########################################################################
    def __init__(self, config_file_name, key, server_type=None, logger=None):
        try:
            MongClass.__init__(self, logger=logger)
            
            if server_type is not None:
                config_file_name = config_file_name + "." + server_type
        
            self.config = ConfigParser()
            output = MongSystemConfig.decrypt(self, config_file_name, key)
            
            self.config.readfp(StringIO(output))        
            self.ver = self.get("Head", "ver")
            if self.ver is None:
                self.log_error("Failed Load System Config")
            else:
                self.is_load = True
                self.log_info("system config load success : " + __name__ + ".__init__" + config_file_name)
        except Exception, e:
            self.log_error("Exception occurred in the initializer " + __name__ + ".__init__ : " + str(e))


    ###########################################################################
    ## get config value
    ###########################################################################
    def get(self, section, name):
        try:
            value = self.config.get(section, name)
            self.log_info("system config get [" + section + "]." + name + " : XXXXXXX");
            return value
        except Exception, e:
            self.log_error("Invalid system config value [" + section + "]." + name)
            return None
        
    ###########################################################################
    ## get property value with dynamic params
    ## IMPORTANT : Support only one parameter...
    ###########################################################################
    def get_params(self, section, name, params):
        try:
            value = self.config.get(section, name).format(params)
            self.log_info("system config get [" + section + "]." + name + " : XXXXXXX");
            return value
        except NoSectionError, e:
            self.log_error("Invalid system config value [" + section + "]." + name)
            return None


    ###########################################################################
    ## encrypt config file
    ###########################################################################
    @staticmethod
    def encrypt(base_class, source_file, target_file, key):
        try:
            #encrypt_cmd = "openssl aes-256-cbc -in {0} -out {1}".format(source, target)
            #subprocess.Popen(encrypt_cmd, shell=True, stdout=PIPE, stderr=PIPE)
            source_data = file_read(source_file)
            if source_data is None:
                base_class.log_error("encrypt failed, source file is not exist : " + source_file)
                return False
            
            cipher = MongAESCipher(key)
            crypted_data = cipher.encrypt(source_data)
            
            if file_write(target_file, crypted_data):
                base_class.log_info("success encrypt " + source_file + " to " + target_file)
                return True
            else:
                base_class.log_error("failed encrypt " + source_file + " to " + target_file)
                
        except Exception, e:
            base_class.log_error("Exception occurred in the initializer " + __name__ + ".encrypt : " + str(e))
            return False


    ###########################################################################
    ## decrypt config file
    ###########################################################################
    @staticmethod
    def decrypt(base_class, source_file, key):
        try:
            #decrypt_cmd = "openssl aes-256-cbc -in {0} -d -k {1}".format(source, key)
            #p = Popen(decrypt_cmd, shell=True, stdin=PIPE, stdout=PIPE, stderr=PIPE)
            #return p.stdout
            
            source_data = file_read(source_file)
            if source_data is None:
                base_class.log_error("encrypt failed, source file is not exist : " + source_file)
                return False
            
            cipher = MongAESCipher(key)
            decrypted_data = cipher.decrypt(source_data)
            
            return decrypted_data
    
        except Exception, e:
            base_class.log_error("Exception occurred in the initializer " + __name__ + ".decrypt : " + str(e))
            return False


###############################################################################
## For Testing
###############################################################################
class MongSystemConfigTestCase(unittest.TestCase):
    
    key = "1234567"
    test_file_name = "MongSystemConfigTestCase.tmp"
    test_enc_file_name = "MongSystemConfigTestCase.tmp.enc"
    test_data = (
        "[Head]\n"
        ";ver=2.0\n"
        "#ver=3.0\n"
        "ver=1.0\n"
        "name:value\n"
        "param:value_{0}\n"
        "param2:%(param)s_{0}")
    
    # Start Point for Test
    def setUp(self):
        file_write(self.test_file_name, self.test_data)
    
    def test_1_encrypt_file(self):
        base_class = MongClass()
        self.assertTrue(MongSystemConfig.encrypt(base_class, self.test_file_name, self.test_enc_file_name, self.key))


    def test_2_load_failed(self):
        self.test_1_encrypt_file()
        config = MongSystemConfig(self.test_enc_file_name, self.key, "DEV")
        self.assertEqual(config.is_load, False)
    
    def test_3_load(self):
        self.test_1_encrypt_file()
        config = MongSystemConfig(self.test_enc_file_name, self.key)
        self.assertEqual(config.is_load, True)
        self.assertEqual(config.get("Head", "ver"), "1.0")
        self.assertEqual(config.get("Head", "name"), "value")
        self.assertEqual(config.get_params("Head", "param", "0"), "value_0")
        self.assertEqual(config.get_params("Head", "param2", "0"), config.get_params("Head", "param", "0") + "_0")
        
    # End Point for each case
    def tearDown(self):
        os.remove(self.test_file_name)
        os.remove(self.test_enc_file_name)
        

if __name__ == '__main__':
    unittest.main()
