from Book import Book
import googlebooks
import time
from DAO import LineNotification
import datetime

class BookDAO:
    def __init__(self,parent = None, serverIP = "10.0.0.1"):
        self.ip = serverIP
        self.parent = parent
        self.gBookAPI = googlebooks.Api()


    def getBookFromID(self, id, getOnlineInfo = True):
        # Fake loading
        time.sleep(0.5)

        book = None
        # Hard-coded demo return value
        if (id == "1"):
            book = Book(bookID=1,title="Introduction to Programming Using Python", isbn="9780132747189")
        if (id == "2"):
            book = Book(bookID=2, title="Practical Object-Oriented Design Using UML", isbn="9780077103934")

        if getOnlineInfo:
            book = self.getOnlineBookInfo(book)


        # Find the way to send information to parent class (May subject to change)
        self.parent.addBook(book)



    def getBookFromRFID_ID(self, rfid_id, getOnlineInfo = True):
            # Fake loading
            time.sleep(0.5)

            book = None
            # Hard-coded demo return value
            if (rfid_id == "9b56d82b"):
                book = Book(bookID=1, title="Introduction to Programming Using Python", isbn="9780132747189")
            if (rfid_id == "0492929a704880"):
                book = Book(bookID=2, title="Practical Object-Oriented Design Using UML", isbn="9780077103934")

            if getOnlineInfo:
                book =  self.getOnlineBookInfo(book)

            # Find the way to send information to parent class (May subject to change)
            self.parent.addBook(book)



    def getOnlineBookInfo(self, book:Book):
        if (book is None):
            return None

        # get new book information from google Database by using book ISBN
        isbn = book.isbn
        try:
            bookData = self.gBookAPI.list('isbn:' + isbn)["items"][0]["volumeInfo"]
            title =  bookData['title']
            authors = str(bookData['authors'])
            publisher =  bookData['publisher']
            publishedDate = bookData['publishedDate']
        except KeyError:
            # If book not found in Google DB, return original data
            return book

        #Override all of book data with new data from Google Database
        bookWithNewInfo = Book(book.bookID,isbn,title,authors,publisher,publishedDate)

        return bookWithNewInfo

    def borrowBooks(self, books,student):
        #TODO: send data(id) to server

        borrowDuration = 10              # Day duration that allowed to borrow

        returnDate = datetime.datetime.now() + datetime.timedelta(days=borrowDuration)
        LineNotification.sendBorrowedMessage(student,books,returnDate)
        print("BorrowBooks "+ str(books))
        self.parent.borrowBookCallback(returnDate)


