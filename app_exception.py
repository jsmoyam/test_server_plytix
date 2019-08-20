import logging


class AppException(Exception):
    """
    Standard exception
    """

    def __init__(self, msg: str = '', logger=None, level: int = logging.WARNING,) -> None:
        """
        Constructor with optional message
        :param msg: optional message of the exception
        :type msg: str
        :return: This function return nothing
        :rtype: None
        """
        if logger:
            logger.log(level, msg)
        Exception.__init__(self, msg)


class GenericErrorMessages:
    """
    Class of generic standard messages
    """

    # Error messages
    KEYFILE_ERROR = 'Not found the key'
    UNKNOWN_LOG_ERROR = 'Unknown log name'
    MODULE_NOT_FOUND = 'Module not found'
    CONFIGURATION_ERROR = 'Configuration error in config.ini'
    VALIDATION_ERROR = 'Validation error'
    LOGIN_ERROR = 'API login error'
    WERKZEUG_NOT_RUNNING = 'Not running with the Werkzeug Server'
    DATABASE_ERROR = 'Error accessing database'
    EXECUTED_COMMAND_ERROR = 'Error executing command'
