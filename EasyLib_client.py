from PyQt5 import QtCore, QtGui, uic
from PyQt5.QtWidgets import *
import sys
import cv2
import ISBNChecker
# from queue import Queue
from pyzbar.pyzbar import decode
from CameraViewerWidget import CameraViewerWidget
from CameraCapture import CameraCapture
from IDChecker import IDChecker
from Book import Book
from BookUtils import BookUtils
from typing import List

# running = False
# capture_thread = None
# q = Queue()

form_class = uic.loadUiType("easy_lib_client.ui")[0]


# Catch Error and display through MessageBox
def catch_exceptions(t, val, tb):
    QMessageBox.critical(None, "An exception was raised", "Exception type: {}".format(t))
    old_hook(t, val, tb)


old_hook = sys.excepthook
sys.excepthook = catch_exceptions


class MyWindowClass(QMainWindow, form_class):
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)
        self.setupUi(self)

        self.window_width_idScan = self.groupBox_scanner.geometry().width()
        self.window_height_idScan = self.groupBox_scanner.geometry().height()
        self.CamView_1 = CameraViewerWidget(self.CamView_1)
        self.timer1 = QtCore.QTimer(self)
        self.timer1.timeout.connect(self.update_id_frame)
        self.timer1.start(1)

        self.window_width_bookScan = self.tab_camera.geometry().width()
        self.window_height_bookScan = self.tab_camera.geometry().height()
        self.CamView_2 = CameraViewerWidget(self.CamView_2)
        self.timer2 = QtCore.QTimer(self)
        self.timer2.timeout.connect(self.update_book_frame)
        self.timer2.start(1)

        self.lastScannedData = None
        self.button_login_with_id.clicked.connect(self.login_clicked)
        self.pushButton_addBook.clicked.connect(lambda : self.getBookData(self.lineEdit_bookID.text()))

        # init Camera
        self.camIDscan = CameraCapture(0, 1280, 720, 10)

        self.bookList = []

        self.init_page_1()

    def start_clicked(self):
        self.camIDscan.start()
        # self.startButton.setEnabled(False)
        # self.startButton.setText('Starting...')

    def login_clicked(self):
        self.validateStuID(self.lineEdit_userID.text())

    def login_callback(self, result):
        print(result)
        self.init_page_2()

    def init_page_1(self):
        self.lineEdit_userID.setText("")
        self.stackedWidget.setCurrentIndex(0)
        if not self.camIDscan.isAlive():
            self.camIDscan.start()
        else:
            self.camIDscan.resume()

    def init_page_2(self):
        self.lineEdit_bookID.setText("")
        self.stackedWidget.setCurrentIndex(2)
        self.progressBar_query.setVisible(False)

        if not self.camIDscan.isAlive():
            self.camIDscan.start()
        else:
            self.camIDscan.resume()

    def update_id_frame(self):
        if self.stackedWidget.currentIndex() != 0:
            return

        self.window_width_idScan = self.groupBox_scanner.geometry().width()
        self.window_height_idScan = self.groupBox_scanner.geometry().height()
        # self.window_height = self.groupBox_scanner.geometry().width() *16 /9
        if not self.camIDscan.getImageQueue().empty():
            # self.startButton.setText('Camera is live')
            frame = self.camIDscan.getImageQueue().get()
            img = frame["img"]

            img_height, img_width, img_colors = img.shape

            scale_w = float(self.window_width_idScan) / float(img_width)
            scale_h = float(self.window_height_idScan) / float(img_height)
            scale = min([scale_w, scale_h])

            if scale == 0:
                scale = 1

            img = cv2.resize(img, None, fx=scale, fy=scale, interpolation=cv2.INTER_CUBIC)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            height, width, bpc = img.shape
            bpl = bpc * width
            decoded_data = decode(img)
            if decoded_data and decoded_data != self.lastScannedData:
                # print("Scanned data : " + str(decoded_data[0]))
                scannedNum = str(decoded_data[0][0])[2:-1]
                print("Barcode data : " + scannedNum)

                # else:
                #     try:
                #         if ISBNChecker.isValid(scannedNum):
                #             print(self.getFormattedBookInfo(scannedNum))
                #
                #     except Exception:
                #         print("Not a valid ISBN")

                self.lastScannedData = decoded_data
            # print(str(self.window_width) + "," + str(self.window_height))
            image = QtGui.QImage(img.data, width, height, bpl, QtGui.QImage.Format_RGB888).mirrored(True, False)
            self.CamView_1.setImage(image)

    def update_book_frame(self):
        if self.stackedWidget.currentIndex() != 2:
            return
        self.window_width_bookScan = self.groupBox_scanner.geometry().width()
        self.window_height_bookScan = self.groupBox_scanner.geometry().height()
        # self.window_height = self.groupBox_scanner.geometry().width() *16 /9
        if not self.camIDscan.getImageQueue().empty():
            # self.startButton.setText('Camera is live')
            frame = self.camIDscan.getImageQueue().get()
            img = frame["img"]
            img_height, img_width, img_colors = img.shape

            scale_w = float(self.window_width_idScan) / float(img_width)
            scale_h = float(self.window_height_idScan) / float(img_height)
            scale = min([scale_w, scale_h])

            if scale == 0:
                scale = 1

            img = cv2.resize(img, None, fx=scale, fy=scale, interpolation=cv2.INTER_CUBIC)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            height, width, bpc = img.shape
            bpl = bpc * width
            decoded_data = decode(img)
            if decoded_data and decoded_data != self.lastScannedData:
                # print("Scanned data : " + str(decoded_data[0]))
                scannedNum = str(decoded_data[0][0])[2:-1]
                print("Barcode data : " + scannedNum)
                self.lineEdit_bookID.setText(scannedNum)
                self.getBookData(scannedNum)
                # else:
                #     try:
                #         if ISBNChecker.isValid(scannedNum):
                #             print(self.getFormattedBookInfo(scannedNum))
                #
                #     except Exception:
                #         print("Not a valid ISBN")

                self.lastScannedData = decoded_data
            # print(str(self.window_width) + "," + str(self.window_height))
            image = QtGui.QImage(img.data, width, height, bpl, QtGui.QImage.Format_RGB888).mirrored(True, False)
            self.CamView_2.setImage(image)

    def closeEvent(self, event):
        self.camIDscan.pause()
        self.destroy()

    '''
    def getFormattedBookInfo(self, bookData):
        bookData = self.gBookAPI.list('isbn:' + bookData)["items"][0]["volumeInfo"]
        output = "Title : " + bookData['title'] + "\n"
        output += "Authors : " + str(bookData['authors']) + "\n"
        output += "Publisher : " + bookData['publisher'] + "\n"
        output += "Published : " + bookData['publishedDate'] + "\n"
        return output
    '''

    def validateStuID(self, stuID):
        if len(stuID) != 8 or not str(stuID).isdigit():
            QMessageBox.warning(self, "Error while parsing input", "Invalid student ID")
            return False

        self.camIDscan.pause()
        self.stackedWidget.setCurrentIndex(1)
        IDChecker(self, 000000).start()

    def getBookData(self,bookID):
        #TODO : Validate bookID input format
        if not (bookID.isdigit()):
            return
        BookUtils(self,bookID).start()
        self.progressBar_query.setVisible(True)


    def addBook(self,book:Book):
        self.progressBar_query.setVisible(False)
        if (book is None):
            print("No books found")
        else:
            self.bookList.append(book)
            #  testISBN : 9780077103934
            i = len(self.bookList) -1
            self.tableWidget_addBooks.insertRow(i)
            self.tableWidget_addBooks.setItem(i, 0, QTableWidgetItem(str(self.bookList[i].bookID)))
            self.tableWidget_addBooks.setItem(i, 1, QTableWidgetItem(str(self.bookList[i].title)))
            self.tableWidget_addBooks.setItem(i, 2, QTableWidgetItem(str(self.bookList[i].author)))
            header = self.tableWidget_addBooks.horizontalHeader()
            # header.setSectionResizeMode(0, QHeaderView.Stretch)
            header.setSectionResizeMode(1, QHeaderView.Stretch)
            # header.setSectionResizeMode(2, QHeaderView.Stretch)




# capture_thread = threading.Thread(target=grab, args=(0, q, 1280, 720, 15))
app = QApplication(sys.argv)
w = MyWindowClass(None)
w.setWindowTitle('EasyLib - Book Scanner')
w.show()
app.exec_()
