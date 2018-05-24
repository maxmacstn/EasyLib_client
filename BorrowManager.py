import json
from datetime import datetime, timedelta

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

    def borrow(self, user, books):
        borrow_list = []
        for book in books:
            borrow_list.append({"user": {"user_id": user.user_id}, "book": {"book_id": book.book_id}})


        try:
            response = requests.post(self.server_ip + '/borrow', json=borrow_list, timeout = self.timeout)
            print(response.json())

            if response.status_code == 200:   #Success
                book_circulations = []
                for raw_book_circulation in response.json():
                    book_circulations.append(self.construct_book_ciruclation(raw_book_circulation))

                if self.parent is not None:
                    due_time = book_circulations[0].due_time
                    print(str(due_time))
                    self.parent.borrowBookCallback(due_time)


            else:  #Soft failed
                self.parent.borrowBookCallback(None,response.json()["message"])

        except requests.exceptions.ConnectTimeout:  # Connection timeout, use offline mockup data
            self.parent.borrowBookCallback(datetime.now() + timedelta(days=7))
            print("Borrow failed")


        # return book_circulations

    @staticmethod
    def construct_book_ciruclation(arguments):
        time_args = ["borrow_time", "due_time", "return_time"]

        for time_arg in time_args:
            if time_arg in arguments.keys() and arguments[time_arg] is not None:
                arguments[time_arg] = datetime.strptime(arguments[time_arg], rfc_822_format)

        arguments["book"] = BookDAO.constructBook(arguments["book"])
        arguments["user"] = UserDAO.constructUser(arguments["user"])

        return BookCirculation(**arguments)