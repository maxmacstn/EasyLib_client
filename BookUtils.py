import threading
from Book import Book
import googlebooks
class BookUtils(threading.Thread):
    def __init__(self,parent,id):
        self.parent = parent
        self.id = id
        threading.Thread.__init__(self)

    def run(self):
        # TODO : validate and get ISBN from bookID (ask to server)
        isbn = self.id
        print("run "+ isbn)
        self.gBookAPI = googlebooks.Api()
        try:
            bookData = self.gBookAPI.list('isbn:' + isbn)["items"][0]["volumeInfo"]


            title =  bookData['title']
            authors = str(bookData['authors'])
            publisher =  bookData['publisher']
            publishedDate = bookData['publishedDate']
        except KeyError:
            # TODO: If book not found in Google DB, it should return book data from local server instead
            return self.parent.addBook(None)

        book = Book(self.id,isbn,title,authors,publisher,publishedDate)

        self.parent.addBook(book)
