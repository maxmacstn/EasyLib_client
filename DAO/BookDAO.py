from Book import Book
from datetime import datetime
from DAO.AbstractDAO import AbstractDAO
from constant import rfc_822_format
import requests


class BookDAO(AbstractDAO):
    def __init__(self, parent=None):
        AbstractDAO.__init__(self)
        self.parent = parent

    def getBookFromID(self, id):
        try:
            path = '/book/' + str(id)
            response = requests.get(self.server_ip + path, timeout=self.timeout,
                                    headers=self.get_authentication_header(path))
            book = None
            if response.status_code == 200:
                book = self.constructBook(response.json())

        except Exception:  # Connection timeout, use offline mockup data
            if self.parent is not None:
                self.parent.showError("Connection Error", "Please check your server connection.", 2)
            return

        if self.parent is not None:
            self.parent.addBook(book)

        return book

    def getBookFromRFID_ID(self, rfid):
        try:
            path = '/book/rfid/' + str(rfid)
            response = requests.get(self.server_ip + path, timeout=self.timeout,headers=self.get_authentication_header(path))
            book = None
            if response.status_code == 200:
                book = self.constructBook(response.json())
        except Exception:  # Connection timeout, use offline mockup data
            if self.parent is not None:
                self.parent.showError("Connection Error", "Please check your server connection.", 2)
            return


        if self.parent is not None:
            self.parent.addBook(book)

        return book

    @staticmethod
    def constructBook(arguments):
        time_arg = "added_on"

        arguments[time_arg] = datetime.strptime(arguments[time_arg], rfc_822_format)

        return Book(**arguments)


if __name__ == "__main__":
    bookDAO = BookDAO()
    book = bookDAO.getBookFromID(1)
    print(book)
    print(book.isbn)