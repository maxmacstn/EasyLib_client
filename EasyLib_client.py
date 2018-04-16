from PyQt5 import QtCore, QtGui, uic, QtWebEngineWidgets
from PyQt5.QtWidgets import *
import sys,cv2,requests,json
from DAO import UserDAO,BookDAO
from CameraViewerWidget import CameraViewerWidget
from Scanner.CameraScanner import CameraScanner
from Scanner.RFIDScanner import RFIDScanner
from Book import Book
from threading import Timer,Thread
import urllib.parse as urlparse
from LineAuth import API_key

form_class = uic.loadUiType("easy_lib_client.ui")[0]


# Catch Error and display through MessageBox
def catch_exceptions(t, val, tb):
    QMessageBox.critical(None, "An exception was raised", "Exception type: {}".format(t))
    old_hook(t, val, tb)


old_hook = sys.excepthook
sys.excepthook = catch_exceptions


class SmartLibGUI(QMainWindow, form_class):
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)
        self.setupUi(self)

        self.currentUser = None
        self.userDAO = UserDAO.UserDAO(self,"10.0.0.1")
        self.bookDAO = BookDAO.BookDAO(self,"10.0.0.1")

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
        self.pushButton_addBook.clicked.connect(lambda : self.queryBookInfo(self.lineEdit_bookID.text()))
        self.pushButton_clear.clicked.connect(self.clearBook)
        self.label_IDerror.hide()
        self.label_borrow_error.hide()
        self.pushButton_back_to_p1.clicked.connect(self.onButtonToPage1)
        self.pushButton_confirm_borrow.clicked.connect(self.onBorrowBookButtonClicked)
        self.pushButton_line_connect.clicked.connect(self.onLineConnectButtonClicked)
        self.pushButton_line_connect_back.clicked.connect(self.init_page_2)

        self.scanMode = 1 #scanner scan mode (id or books)

        # init Camera
        self.camIDscan = CameraScanner(self,0, 1280, 720, 10)
        self.RFIDScanner = RFIDScanner(self)

        self.webView = QtWebEngineWidgets.QWebEngineView(self.webView)


        self.bookBasket = []

        self.init_page_1()

    def start_clicked(self):
        self.camIDscan.start()
        # self.startButton.setEnabled(False)
        # self.startButton.setText('Starting...')

    def login_clicked(self):
        self.camIDscan.pause()
        self.validateStuID(self.lineEdit_userID.text())

    def login_callback(self, user):

        # Get user failed
        if (user == None):
            self.label_IDerror.show()
            self.init_page_1()
            t = Timer(5, self.hideErrorMessage)
            t.start()  # after 5 seconds, red error text will disappear
            return
        else:
            self.currentUser = user

        self.init_page_2()

    def onButtonToPage1(self):
        self.camIDscan.pause()
        self.init_page_1()


    def init_page_1(self):
        self.currentUser = None
        self.scanMode = 1
        self.lineEdit_userID.setText("")
        self.stackedWidget.setCurrentIndex(0)

        if not self.camIDscan.isAlive():
            self.camIDscan.start()
        else:
            self.camIDscan.resume()

        if not self.RFIDScanner.isAlive():
            self.RFIDScanner.start()
        else:
            self.RFIDScanner.resume()

    def hideErrorMessage(self):
        self.label_IDerror.hide()
        self.label_borrow_error.hide()

    def init_page_2(self):
        self.scanMode = 2
        self.clearBook()
        self.label_borrow_name.setText(self.currentUser.getName())
        self.label_borrow_id.setText(str(self.currentUser.getID()))
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

            try:
                img_height, img_width, img_colors = img.shape
            except AttributeError:
                return

            scale_w = float(self.window_width_idScan) / float(img_width)
            scale_h = float(self.window_height_idScan) / float(img_height)
            scale = min([scale_w, scale_h])

            if scale == 0:
                scale = 1

            img = cv2.resize(img, None, fx=scale, fy=scale, interpolation=cv2.INTER_CUBIC)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            height, width, bpc = img.shape
            bpl = bpc * width
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
            try:
                img_height, img_width, img_colors = img.shape
            except AttributeError:
                return
            scale_w = float(self.window_width_idScan) / float(img_width)
            scale_h = float(self.window_height_idScan) / float(img_height)
            scale = min([scale_w, scale_h])

            if scale == 0:
                scale = 1

            img = cv2.resize(img, None, fx=scale, fy=scale, interpolation=cv2.INTER_CUBIC)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            height, width, bpc = img.shape
            bpl = bpc * width

            image = QtGui.QImage(img.data, width, height, bpl, QtGui.QImage.Format_RGB888).mirrored(True, False)
            self.CamView_2.setImage(image)

    def scannerCallback(self,data,scannerType = 0):
        if (self.scanMode == 1):
            if (scannerType == 0):
               self.lineEdit_userID.setText(data)
            if (scannerType == 1):
                self.validateStuID(data,True)

        if (self.scanMode == 2):
            if (scannerType == 0):
               self.lineEdit_bookID.setText(data)
            if (scannerType == 1):
                self.queryBookInfo(data,True)




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

    def validateStuID(self, ID, isRFID_id = False):
        self.camIDscan.pause()
        self.stackedWidget.setCurrentIndex(1)

        if (isRFID_id):
              Thread(target= self.userDAO.getUserFromRFID_ID, args=[ID]).start()

        else:
            if len(ID) != 8 or not str(ID).isdigit():
                QMessageBox.warning(self, "Error while parsing input", "Invalid student ID")
                self.init_page_1()
                return
            Thread(target = self.userDAO.getUserFromID, args=[ID]).start()


    # Add book from ID (Same function as validateStuID, but for Book.)
    def queryBookInfo(self,ID,isRFID_id=False):
        self.progressBar_query.setVisible(True)


        if (not isRFID_id):
            if not (ID.isdigit()):
                return
            Thread(target=self.bookDAO.getBookFromID, args=[ID]).start()
        else:
            Thread(target=self.bookDAO.getBookFromRFID_ID, args=[ID]).start()


    def clearBook(self):
        while (self.tableWidget_addBooks.rowCount() > 0):
                self.tableWidget_addBooks.removeRow(0)
        self.bookBasket = []

    def addBook(self,book:Book):
        self.progressBar_query.setVisible(False)

        if (book is None):
            print("No books found")
            self.label_borrow_error.setText("No book found!!")
            self.label_borrow_error.show()
            Timer(5, self.hideErrorMessage).start()
        else:
            if (book in self.bookBasket):
                self.label_borrow_error.setText("This book is already added!!")
                self.label_borrow_error.show()
                Timer(5, self.hideErrorMessage).start()
                return

            self.bookBasket.append(book)
            #  testISBN : 9780077103934
            i = len(self.bookBasket) -1

            self.tableWidget_addBooks.insertRow(i)
            self.tableWidget_addBooks.setItem(i, 0, QTableWidgetItem(str(self.bookBasket[i].bookID)))
            self.tableWidget_addBooks.setItem(i, 1, QTableWidgetItem(str(self.bookBasket[i].title)))
            self.tableWidget_addBooks.setItem(i, 2, QTableWidgetItem(str(self.bookBasket[i].author)))
            header = self.tableWidget_addBooks.horizontalHeader()
            # header.setSectionResizeMode(0, QHeaderView.Stretch)
            header.setSectionResizeMode(1, QHeaderView.Stretch)
            # header.setSectionResizeMode(2, QHeaderView.Stretch)

    def onBorrowBookButtonClicked(self):
        Thread(target= self.bookDAO.borrowBooks,args=[self.bookBasket,self.currentUser]).start()
        self.stackedWidget.setCurrentIndex(1)

    def init_page_3(self):
        self.stackedWidget.setCurrentIndex(3)

    def borrowBookCallback(self,returnDate):
        if returnDate == None:
            self.stackedWidget.setCurrentIndex(2)
        else:
            print(returnDate.strftime('%d %m %Y'))
            self.stackedWidget.setCurrentIndex(3)
            self.label_due_date.setText(returnDate.strftime('%d %m %Y'))
            Timer(0.2,self.init_page_3).start()
            Timer(5,self.init_page_1).start()

    def onLineConnectButtonClicked(self):
        self.camIDscan.pause()
        self.stackedWidget.setCurrentIndex(4)
        self.webView.show()
        self.label_line_connect_success.hide()

        URL = 'https://notify-bot.line.me/oauth/authorize?'
        URL += 'response_type=code'
        URL += '&client_id=DnQgoVvnU1kl4rbY6eNp0Z'
        URL += '&redirect_uri=http://localhost/test/index.php'
        URL += '&scope=notify';
        URL += '&state=' + str(self.currentUser.getID())
        self.webView.load(QtCore.QUrl().fromUserInput(URL))
        self.webView.urlChanged.connect(self.checkURL)


    def checkURL(self):
        url = self.webView.url().toDisplayString()
        data = urlparse.urlparse(url)
        print(data.netloc)
        if (data.netloc == 'localhost'):
            response_data = urlparse.parse_qs(data.query)
            self.getToken(response_data)

    def getToken(self, response_data):


        code = response_data.get("code")[0]
        print("Code = " + code)
        url = "https://notify-bot.line.me/oauth/token"
        payload = "grant_type=authorization_code&code=" + code \
                  + "&redirect_uri=http%3A%2F%2Flocalhost%2Ftest%2Findex.php&client_id=" + \
                  API_key.CLIENT_ID + "&client_secret=" + API_key.CLIENT_SECRET
        headers = {
            'content-type': "application/x-www-form-urlencoded",
            'cache-control': "no-cache"
        }

        response = requests.request("POST", url, data=payload, headers=headers)
        print(response.text)
        response_json = json.loads(response.text)
        if (response_json['status'] != 200):
            print("Request token error")
            return

        token = response_json['access_token']

        print("Token " + token)
        self.currentUser.setLineNotifyToken(token)
        self.webView.hide()
        self.label_line_connect_success.show()
        Timer(2,self.init_page_2)


# capture_thread = threading.Thread(target=grab, args=(0, q, 1280, 720, 15))
app = QApplication(sys.argv)
w = SmartLibGUI(None)
w.setWindowTitle('EasyLib - Book Scanner')
w.show()
app.exec_()
