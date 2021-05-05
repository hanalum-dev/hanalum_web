""" Hanalum Custom Exeptions """


class NoPermissionException(Exception):
    """ 권한 없음 """
    def __init__(self, message="", errors="No Permission Error"):
        super().__init__(message, errors)
