###############################################################################
## System LIB
###############################################################################
import os
import unittest
import getpass
from subprocess import Popen, PIPE
from datetime import datetime
import time

###############################################################################
## Load Password for decrypting system.ini.enc
###############################################################################
def input_password(msg="Input System Password: "):
    return getpass.getpass(msg)
###############################################################################
## Run Shell Command
###############################################################################
def run_command(command):
    try:
        #print "- command : %s" % command
        p = Popen(command, shell=True, stdout=PIPE)
        (output, err) = p.communicate()
        p_status=p.wait()
        return p_status
    except Exception, e:
        print "Exception occured in the initializer " + __name__ + ".run_command : " + str(e)
        return -1
    #for line in p.stdout:
    #    print line

###############################################################################
## file read and return it
###############################################################################
def file_read(filename):
    f = None
    try:
        f = open(filename, "r")
        data = f.read()
        return data
    except Exception, e:
        print "Exception occured in the initializer " + __name__ + ".file_read : " + str(e)
        return None
    finally:
        if f is not None:
            f.close()

###############################################################################
## file write and return isSuccess
###############################################################################
def file_write(filename, data):
    f = None
    try:
        f = open(filename, "w")
        f.write(data)
        return True
    except Exception, e:
        print "Exception occured in the initializer " + __name__ + ".file_write : " + str(e)
        return False
    finally:
        if f is not None:
            f.close()


###############################################################################
## get date with format 
###############################################################################
def get_time_string(dt=None, format="%Y-%m-%d %H:%M.%S"):
    try:
        if dt is None:
            dt = datetime.now()
            
        return dt.strftime(format)
    except Exception, e:
        print "Exception occured in the initializer " + __name__ + "get_time_string : " + str(e)
        return None;
    
def get_log_prefix(mode="INFO"):
    return get_time_string(format="%Y-%m-%d %H:%M.%S,000") + " - default - " + mode + " - "


###############################################################################
## file write and return isSuccess
###############################################################################
"""
>>> stringTemplate = 'pos1={1} pos2={2} pos3={3} foo={foo} bar={bar}'
>>> print(formatString(stringTemplate, 1, 2))
pos1=1 pos2=2 pos3={3} foo={foo} bar={bar}
>>> print(formatString(stringTemplate, 42, bar=123, foo='hello'))
pos1=42 pos2={2} pos3={3} foo=hello bar=123
"""
def formatString(stringTemplate, *args, **kwargs):
    # Replace any positional parameters
    for i in range(0, len(args)):
        tmp = '{%s}' % str(1+i)
        while True:
            pos = stringTemplate.find(tmp)
            if pos < 0:
                break
            stringTemplate = stringTemplate[:pos] + \
                             str(args[i]) + \
                             stringTemplate[pos+len(tmp):]



    # Replace any named parameters
    for key, val in kwargs.items():
        tmp = '{%s}' % key
        while True:
            pos = stringTemplate.find(tmp)
            if pos < 0:
                break
            stringTemplate = stringTemplate[:pos] + \
                             str(val) + \
                             stringTemplate[pos+len(tmp):]
 
    return stringTemplate

def get_timestamp():
    return int(time.mktime(datetime.now().timetuple()))


###############################################################################
## For Testing
###############################################################################   
class MongCommonTestCase(unittest.TestCase):
    
    test_file_name = "MongCommonTestCase.tmp"
    test_data = "test123"
    
    def test_1_file_write(self):
        self.assertEqual(file_write(self.test_file_name, self.test_data), True)
    
    def test_2_file_read(self):
        self.assertEqual(file_read(self.test_file_name), self.test_data)
        os.remove(self.test_file_name)
        
    def get_time_string(self):
        self.assertNotEqual(get_time_string(), None)
        
if __name__ == '__main__':
    #suite1 = unittest.TestSuite(map(MongCommonTestCase,['test_file_write', 'test_file_read']))
    #allsuites = unittest.TestSuite([suite1])
    
    #unittest.TextTestRunner(verbosity=2).run(allsuites)
    unittest.main()
