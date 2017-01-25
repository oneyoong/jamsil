###############################################################################
# System LIB
###############################################################################
import os
from ConfigParser import ConfigParser, NoSectionError

###############################################################################
# Mong LIB
###############################################################################
from MongCommon import file_write
from MongClass import MongClass
import unittest

####################################################################
## rubin.config sample
####################################################################
#[{SectionName}]
#{Name}:{Value}
####################################################################


####################################################################
## Mong Config Class
## 1. Managing property 
####################################################################
class MongConfig(MongClass):

    is_load = False

    ###########################################################################
    ## init
    ###########################################################################
    def __init__(self, config_file_name, server_type="DEV", logger=None):
        load_file_name = config_file_name + "." + server_type
        try:
            MongClass.__init__(self, logger=logger)
            self.config = ConfigParser()
            self.log_info("load config file : " + load_file_name)
            
            if os.path.isfile(load_file_name):
                self.config.read(load_file_name)
                self.log_info("load success config file : " + load_file_name)
                self.is_load = True
            else:
                self.log_warning("file not found : " + load_file_name)
            
        except Exception, e:
            self.log_error("Exception occurred in the initializer " + __name__ + ".__init__" + str(e))
            self.log_error("Config File Load Failed : " + load_file_name)


    ###########################################################################
    ## get property value
    ###########################################################################
    def get(self, section, name):
        try:
            value = self.config.get(section, name)
            self.log_info("config value [" + section + "]." + name + " : " + value)
            return value
        except NoSectionError, e:
            self.log_error("Invalid config value [" + section + "]." + name)
            return None
    
    ###########################################################################
    ## get property value with dynamic params
    ## IMPORTANT : Support only one parameter...
    ###########################################################################
    def get_params(self, section, name, params):
        try:
            value = self.config.get(section, name).format(params)
            self.log_info("config value [" + section + "]." + name + " : " + value)
            return value
        except NoSectionError, e:
            self.log_error("Invalid config value [" + section + "]." + name)
            return None


###############################################################################
## For Testing
###############################################################################   
class MongConfigTestCase(unittest.TestCase):
    
    test_file_name = "MongConfigTestCase.tmp"
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
        file_write(self.test_file_name + ".DEV", self.test_data)
        
    def test_2_load_failed(self):
        config = MongConfig(self.test_file_name, "PRD")
        self.assertEqual(config.is_load, False)


    def test_3_load(self):
        config = MongConfig(self.test_file_name, "DEV")
        self.assertEqual(config.is_load, True)
        self.assertEqual(config.get("Head", "ver"), "1.0")
        self.assertEqual(config.get("Head", "name"), "value")
        self.assertEqual(config.get_params("Head", "param", "0"), "value_0")
        self.assertEqual(config.get_params("Head", "param2", "0"), config.get_params("Head", "param", "0") + "_0")
        
    # End Point for Test
    def tearDown(self):
        if os.path.isfile(self.test_file_name):
            os.remove(self.test_file_name + ".DEV")

if __name__ == '__main__':
    unittest.main()
