class Book:
    def __init__(self,bookID,isbn=None,title = None, author = None,publisher = None, publishedDate = None):
        self.bookID = bookID
        self.title = title
        self.isbn = isbn
        self.author = author
        self.publisher = publisher
        self.publishedDate = publishedDate

    def setInfo(self,isbn,title, author,publisher, publishedDate ):
        self.title = title
        self.isbn = isbn
        self.author = author
        self.publisher = publisher
        self.publishedDate = publishedDate