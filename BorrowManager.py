from datetime import datetime

import requests

from BookCirculation import BookCirculation
from DAO.AbstractDAO import AbstractDAO
from DAO.BookDAO import BookDAO
from DAO.UserDAO import UserDAO
from constant import *


class BorrowManager(AbstractDAO):
    def __init__(self, parent = None):
        AbstractDAO.__init__(self)
        self.parent = parent

    def borrow(self, user, book):
        borrow_request = {"user": user, "book": book}

        response = requests.post(self.server_ip + '/borrow/', json=borrow_request)

        book_circulation = self.construct_book_ciruclation(response.json())

        if self.parent is not None:
            self.parent.callback(book_circulation)

        return book_circulation

    @staticmethod
    def construct_book_ciruclation(arguments):
        time_args = ["borrow_time", "due_time", "return_time"]

        for time_arg in time_args:
            arguments[time_arg] = datetime.strptime(arguments[time_arg], rfc_822_format)

        arguments["book"] = BookDAO.constructBook(arguments["book"])
        arguments["user"] = UserDAO.constructUser(arguments["user"])

        return BookCirculation(**arguments)