###############################################################################
## System LIB
###############################################################################
import os, sys
###############################################################################
## Mong LIB
###############################################################################
sys.path.append("./lib2.x")
import MongCommon
from MongClass import MongClass
from MongSystemConfig import MongSystemConfig
###############################################################################
## Usage Function
###############################################################################
def usage():
    print ""
    print "[Usage] python decrypt.py {crypted_file_name}"
    print ""


###############################################################################
## Main Function
###############################################################################
def main():
    try:
        if len(sys.argv) < 2:
            usage()
            return False
        
        # 1. input passkey
        pass1 = MongCommon.input_password("input encryption key : ")
        
        # 2. encrypt
        base_class = MongClass()
        source_data = MongSystemConfig.decrypt(base_class, sys.argv[1], pass1)
        
        print "*************************"
        print source_data
        print "*************************"
        
        if source_data is None:
            print "Failed Decryption.....!!!!"
            return False


        print "Success Decryption.....!!!!"
                
        return True
        
    except Exception, e:
        print("Failed Decryption : " + str(e))
        return False;
if __name__ == '__main__':
    main()
