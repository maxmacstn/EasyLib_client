from PyQt5 import QtCore, QtGui, uic,QtWebEngineWidgets
from PyQt5.QtWidgets import *
import sys,os,requests,json
import urllib.parse as urlparse
from LineAuth import API_key



form_class = uic.loadUiType("lineAuth.ui")[0]


# Catch Error and display through MessageBox
def catch_exceptions(t, val, tb):
    QMessageBox.critical(None, "An exception was raised", "Exception type: {}".format(t))
    old_hook(t, val, tb)


old_hook = sys.excepthook
sys.excepthook = catch_exceptions


class LineAuthGUI(QMainWindow, form_class):
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)
        self.setupUi(self)
        self.webView = QtWebEngineWidgets.QWebEngineView(self.webView)
        self.pushButton.clicked.connect(self.loginAuth)

    def loginAuth(self):
        URL = 'https://notify-bot.line.me/oauth/authorize?'
        URL += 'response_type=code'
        URL += '&client_id=DnQgoVvnU1kl4rbY6eNp0Z'
        URL += '&redirect_uri=http://localhost/test/index.php'
        URL += '&scope=notify';
        URL += '&state=' + self.lineEdit.text()
        self.webView.load(QtCore.QUrl().fromUserInput(URL))
        self.webView.urlChanged.connect(self.checkURL)

    def checkURL(self):
        url = self.webView.url().toDisplayString()
        data = urlparse.urlparse(url)
        print(data.netloc)
        if (data.netloc == 'localhost'):
            response_data = urlparse.parse_qs(data.query)
            self.getToken(response_data)

    def getToken(self,response_data):
        code  = response_data.get("code")[0]
        print("Code = "+code)
        url = "https://notify-bot.line.me/oauth/token"
        payload = "grant_type=authorization_code&code="+code\
                  +"&redirect_uri=http%3A%2F%2Flocalhost%2Ftest%2Findex.php&client_id="+\
                  API_key.CLIENT_ID + "&client_secret="+ API_key.CLIENT_SECRET
        headers = {
            'content-type': "application/x-www-form-urlencoded",
            'cache-control': "no-cache"
        }

        response = requests.request("POST", url, data=payload, headers=headers)
        print(response.text)
        response_json = json.loads(response.text)
        if (response_json['status']!= 200):
            print("Request token error")
            return

        print("Token " + response_json['access_token'])


app = QApplication(sys.argv)
w = LineAuthGUI(None)
w.setWindowTitle('SmartLib - LineAuth')
w.show()
app.exec_()
