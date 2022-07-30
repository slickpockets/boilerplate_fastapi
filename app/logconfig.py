import logging
simpleformatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
debugFormatter = logging.Formatter('[%(asctime)s] p%(process)s {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s')

def setup_logger(name, log_file,formatter, level=logging.INFO):
    """To setup as many loggers as you want"""

    handler = logging.FileHandler(log_file)
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)

    return logger

# first file logger
infoLogger = setup_logger('infoLogger', '/var/log/python/info.log', simpleformatter, logging.INFO)

# second file logger
debugLogger = setup_logger('debugLogger', '/var/log/python/debug.log', debugFormatter,logging.DEBUG)

errorLogger = setup_logger('errorLogger', '/var/log/python/error.log', simpleformatter, logging.ERROR)
