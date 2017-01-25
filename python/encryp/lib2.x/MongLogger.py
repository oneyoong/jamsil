###############################################################################
# System LIB
###############################################################################
import sys, traceback
import logging, logging.config, yaml
from logging.handlers import TimedRotatingFileHandler

import MongCommon
####################################################################
# logging.config sample
####################################################################
"""
[loggers]
keys=root,file
 
[handlers]
keys=fileHandler,consoleHandler
 
[formatters]
keys=myFormatter
 
[logger_root]
level=DEBUG
handlers=consoleHandler

[logger_file]
level=DEBUG
handlers=fileHandler
qualname=file
 
[handler_consoleHandler]
class=StreamHandler
level=DEBUG
formatter=myFormatter
args=(sys.stdout,)
 
[handler_fileHandler]
class=handlers.TimedRotatingFileHandler
formatter=myFormatter
args=("batch.log",)
 
[formatter_myFormatter]
format=%(asctime)s - %(name)s - %(levelname)s - %(message)s
datefmt=%Y%d%m
"""


####################################################################
## Mong Logger Class
####################################################################
class MongLogger(object):
    logger = None
    
    ###########################################################################
    ## init
    ###########################################################################
    def __init__(self, config_file_name, log_name, server_type="DEV"):
        try:
            #logging.config.dictConfig(yaml.load(open(config_file_name + "." + server_type)))
            #handler = TimedRotatingFileHandler(path, when="d", interval=1)
            log_config_file_name = config_file_name + "." + server_type
            self.info("Loading log config file : " + log_config_file_name)
            logging.config.fileConfig(log_config_file_name)
            
            self.info("Loading log config file Success")
            self.logger = logging.getLogger(log_name)
            self.info("get logger : " + log_name)
            
            if self.logger is None:
                self.warning("Failed load log config file : " + log_config_file_name)
            else:
                self.info("Succesed load log config file : " + log_config_file_name)
            
        except Exception, e:
            self.error("Exception occurred in the initializer " + __name__ + ".__init__ : " + str(e))


    ###########################################################################
    ## debug log
    ###########################################################################
    def debug(self, s):
        if self.logger is not None:
            self.logger.debug(s)
        else:
            print MongCommon.get_log_prefix(mode="DEBUG") + s

    ###########################################################################
    ## info log
    ###########################################################################
    def info(self, s):
        if self.logger is not None:
            self.logger.info(s)
        else:
            print MongCommon.get_log_prefix(mode="INFO") + s

    ###########################################################################
    ## warning log
    ###########################################################################
    def warning(self, s):
        if self.logger is not None:
            self.logger.warning(s)
        else:
            print MongCommon.get_log_prefix(mode="WARNING") + s


    ###########################################################################
    ## error log
    ###########################################################################
    def error(self, s):
        if self.logger is not None:
            self.logger.error(s)
        else:
            print MongCommon.get_log_prefix(mode="ERROR") + s 

    @staticmethod
    def trace_back():

        print "*" * 80
        print "*** [START] TRACE BACK"
        print "*" * 80
        
        exc_type, exc_value, exc_traceback = sys.exc_info()
        print "-" * 80
        print "- print_tb:"
        print "-" * 80
        traceback.print_tb(exc_traceback, limit=1, file=sys.stdout)
        print "-" * 80
        print "- print_exception:"
        print "-" * 80
        traceback.print_exception(exc_type, exc_value, exc_traceback,
                                  limit=2, file=sys.stdout)


        print "-" * 80
        print "- print_exc:"
        print "-" * 80
        traceback.print_exc()
        print "-" * 80
        print "- format_exc, first and last line:"
        print "-" * 80
        formatted_lines = traceback.format_exc().splitlines()
        print formatted_lines[0]
        print formatted_lines[-1]
        print "-" * 80
        print "- format_exception:"
        print "-" * 80
        print repr(traceback.format_exception(exc_type, exc_value,
                                              exc_traceback))
        print "-" * 80
        print "- extract_tb:"
        print "-" * 80
        print repr(traceback.extract_tb(exc_traceback))
        print "-" * 80
        print "- format_tb:"
        print "-" * 80
        print repr(traceback.format_tb(exc_traceback))
        print "-" * 80
        print "- tb_lineno:", exc_traceback.tb_lineno
        print "-" * 80
        
        print "*" * 80
        print "*** [END] TRACE BACK"
        print "*" * 80


###############################################################################
# For Testing
###############################################################################
if __name__ == '__main__':
    logger = MongLogger("logging.ini", "console")
    logger.debug("debug");
    logger.info("debug");
    logger.warning("debug");
    logger.error("debug");

    #logger = MongLogger("logging.ini", "file")
    #logger.debug("debug");
    #logger.info("debug");
    #logger.warning("debug");
    #logger.error("debug");
