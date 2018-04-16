import requests
from User import Student
from Book import Book
import datetime

url = 'https://notify-api.line.me/api/notify'

def sendBorrowedMessage(student:Student, books, dueDate):
    token = student.getLineNotifyToken()
    returnDateString =  dueDate.strftime('%d/%m/%Y')
    msg = 'Thank you for using SmartLibrary\n\n[Borrowed Books]\n'
    headers = {'content-type': 'application/x-www-form-urlencoded', 'Authorization': 'Bearer ' + token}

    for book in books:
        msg += "- " + book.getSimpleStringInfo() +"\n"
    msg += "\nPlease return books before "+ returnDateString

    r = requests.post(url, headers=headers, data={'message': msg})
