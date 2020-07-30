"""
# @Time    : 2020/7/30 11:29
# @Author  : tmackan
 业务异常
"""

ERROR_CODES = {
    "ServerError": (11, '系统错误', 'ServerError'),
    "ValidationError": (10, '参数错误', 'Invalid field')

}


class BaseError(Exception):
    alarm_level = 'error'

    def __init__(self, message=None, payload=None):
        status, msg, msg_en = ERROR_CODES.get(self.__class__.__name__)
        self.status = status
        if message is not None:
            self.message = message
        else:
            self.message = msg
        super(BaseError, self).__init__(message, status, payload)

    def __str__(self):
        return '%s: %s' % (self.status, self.message)

    def __repr__(self):
        return '%s: %s' % (self.__class__.__name__, self.args)


class ServerError(BaseError):
    alarm_level = 'error'

    def __init__(self, message=None, payload=None):
            super(ServerError, self).__init__(message, payload)


class ThirdAPIException(BaseError):
    alarm_level = 'error'

    def __init__(self, message=None, payload=None):
        super(ThirdAPIException, self).__init__(message, payload)


class ValidationError(BaseError):
    alarm_level = 'info'

    def __init__(self, message=None, payload=None):
        super(ValidationError, self).__init__(message, payload)
