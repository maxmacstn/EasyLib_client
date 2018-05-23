from Book import Book
import googlebooks
import time
from DAO import LineNotification
from datetime import datetime
from DAO.AbstractDAO import AbstractDAO
from constant import rfc_822_format
import requests
import random

#
# class BookDAO:
#     def __init__(self,parent = None, serverIP = "10.0.0.1"):
#         self.ip = serverIP
#         self.parent = parent
#         self.gBookAPI = googlebooks.Api()
#
#
#     def getBookFromID(self, id, getOnlineInfo = True):
#         # Fake loading
#         time.sleep(0.5)
#
#         book = None
#         # Hard-coded demo return value
#         if (id == "1"):
#             book = Book(bookID=1,title="Introduction to Programming Using Python", isbn="9780132747189")
#         if (id == "2"):
#             book = Book(bookID=2, title="Practical Object-Oriented Design Using UML", isbn="9780077103934")
#
#         if getOnlineInfo:
#             book = self.getOnlineBookInfo(book)
#
#
#         # Find the way to send information to parent class (May subject to change)
#         self.parent.addBook(book)
#
#
#
#     def getBookFromRFID_ID(self, rfid_id, getOnlineInfo = True):
#             # Fake loading
#             time.sleep(0.5)
#
#             book = None
#             # Hard-coded demo return value
#             if (rfid_id == "9b56d82b"):
#                 book = Book(bookID=1, title="Introduction to Programming Using Python", isbn="9780132747189")
#             if (rfid_id == "0492929a704880"):
#                 book = Book(bookID=2, title="Practical Object-Oriented Design Using UML", isbn="9780077103934")
#
#             if getOnlineInfo:
#                 book =  self.getOnlineBookInfo(book)
#
#             # Find the way to send information to parent class (May subject to change)
#             self.parent.addBook(book)
#
#
#
#     def getOnlineBookInfo(self, book:Book):
#         if (book is None):
#             return None
#
#         # get new book information from google Database by using book ISBN
#         isbn = book.isbn
#         try:
#             bookData = self.gBookAPI.list('isbn:' + isbn)["items"][0]["volumeInfo"]
#             title =  bookData['title']
#             authors = str(bookData['authors'])
#             publisher =  bookData['publisher']
#             publishedDate = bookData['publishedDate']
#         except KeyError:
#             # If book not found in Google DB, return original data
#             return book
#
#         #Override all of book data with new data from Google Database
#         bookWithNewInfo = Book(book.bookID,isbn,title,authors,publisher,publishedDate)
#
#         return bookWithNewInfo
#
#     def borrowBooks(self, books,student):
#         #TODO: send data(id) to server
#
#         borrowDuration = 10              # Day duration that allowed to borrow
#
#         returnDate = datetime.datetime.now() + datetime.timedelta(days=borrowDuration)
#         LineNotification.sendBorrowedMessage(student,books,returnDate)
#         print("BorrowBooks "+ str(books))
#         self.parent.borrowBookCallback(returnDate)

class BookDAO(AbstractDAO):
    def __init__(self, parent=None):
        AbstractDAO.__init__(self)
        self.parent = parent

    def getBookFromID(self, id):
        try:
            response = requests.get(self.server_ip + '/book/' + str(id), timeout = self.timeout)
            book = None
            if response.status_code == 200:
                book = self.constructBook(response.json())
        except requests.exceptions.ConnectTimeout:  # Connection timeout, use offline mockup data
            book = Book(random.randint(100,1000),"Offline book", "-",datetime.now(),True,"Offline guy",
                        "Offline press .ltd")
            print("Waring! use offline data for debugging only")
        if self.parent is not None:
            self.parent.addBook(book)

        return book

    def getBookFromRFID_ID(self, rfid):
        try:
            response = requests.get(self.server_ip + '/book/rfid/' + str(rfid), timeout = self.timeout)
            book = None
            if response.status_code == 200:
                book = self.constructBook(response.json())
        except requests.exceptions.ConnectTimeout:  # Connection timeout, use offline mockup data
            book = Book(random.randint(100, 1000), "Offline book", "-", datetime.now(), True, "Offline guy",
                        "Offline press .ltd")
            print("Waring! use offline data for debugging only")


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