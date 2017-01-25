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
    print "[Usage] python encrypt.py {source_file_name} {target_file_name}"
    print ""
###############################################################################
## Main Function
###############################################################################
def main():
    try:
        if len(sys.argv) < 3:
            usage()
            return False
        
        # 1. input passkey
        pass1 = MongCommon.input_password("input encryption key : ")
        pass2 = MongCommon.input_password("reinput encryption key : ")
        
        if pass1 != pass2:
            print "Input key is not missmatched!!!!!"
            return False
        
        # 2. encrypt
        base_class = MongClass()
        if MongSystemConfig.encrypt(base_class, sys.argv[1], sys.argv[2], pass1):
            print "Encryptioning..... : " + sys.argv[2]
        
        # 3. Validation
        source_data = MongCommon.file_read(sys.argv[1]);
        decrypt_data = MongSystemConfig.decrypt(base_class, sys.argv[2], pass1);
        
        if source_data != decrypt_data:
            print "Failed Encryption.....!!!!"
            os.remove(sys.argv[2])
            return False
        
        print "Success Encryption.....!!!!"
                
        return True
        
    except Exception, e:
        print("Failed Encryption : " + str(e))
        return False;
if __name__ == '__main__':
    main()
