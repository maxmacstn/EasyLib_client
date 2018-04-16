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

    def getSimpleStringInfo(self):
        return self.title+", " +self.author

    #Compare method for book (Compare by ID)
    def __eq__(self, other):
        return self.bookID == other.bookID




