""" error.py """


class Error:
    """ Base class for exceptions """

    def __init__(self):
        """생성자"""

        self.status = False
        self.msg = ""
