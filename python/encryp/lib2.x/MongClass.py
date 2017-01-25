###############################################################################
## System LIB
###############################################################################
import MongCommon
####################################################################
## Mong Base Class 
####################################################################
class MongClass(object):
    logger = None
    
    def __init__(self, logger = None):
        self.logger = logger
    
    def log_info(self, str):
        if self.logger:
            self.logger.info(str)
        else:
            print MongCommon.get_log_prefix(mode="INFO") + str
            
    def log_warning(self, str):
        if self.logger:
            self.logger.warning(str)
        else:
            print MongCommon.get_log_prefix(mode="WARNING") + str
    
    def log_error(self, str):
        if self.logger:
            self.logger.error(str)
        else:
            print MongCommon.get_log_prefix(mode="ERROR") + str
