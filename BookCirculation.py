class BookCirculation:
    def __init__(self, id, book, user, borrow_time, due_time, return_time = None):
        self.id = id
        self.book = book
        self.user = user
        self.borrow_time = borrow_time
        self.due_time = due_time
        self.return_time = return_time

    def __str__(self):
        return "Borrowed " + self.book.title + " by " + self.user.name + " on " + str(self.borrow_time) + " due " + str(self.return_time)