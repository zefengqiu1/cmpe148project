      MainWindow.resize(500, 400)
        MainWindow.setMinimumSize(QtCore.QSize(500, 400))
        MainWindow.setMaximumSize(QtCore.QSize(500, 400))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(370, 320, 81, 31))
        self.pushButton.setObjectName("pushButton")
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(40, 320, 301, 31))
        self.lineEdit.setObjectName("lineEdit")
        self.textEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit.setGeometry(QtCore.QRect(40, 40, 401, 261))
        self.textEdit.setObjectName("textEdit")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(20, 10, 71, 16))
        self.label.setObjectName("label")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 500, 23))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.pushButton.clicked.connect(self.clickGoHandler)
        self.textEdit.append("robot: I am robot, what can I do for you?")

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def clickGoHandler(self):

        text=self.lineEdit.text().strip()
        self.textEdit.append(f"Me: {text}")
        res=self.translate__english_chat(text)
        self.textEdit.append(f"robot: {res}")

    def translate__english_chat(self,text):
        try:
            url = "http://api.qingyunke.com/api.php"
            header = {
                "user-agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36"
            }
            parmas = {
                "key": "free",
                "appid": 0,
                "msg": text
            }
            result = requests.get(url, params=parmas, headers=header)
            json_data = result.json()

            if json_data["result"] == 0:
                result = json_data["content"]
            else:
                raise ValueError

        except Exception as e:
            result = "I am sorry, I do not understand !"

        res=self.trans_api(result)
        return res

    def trans_api(self,q,from_Lang='auto',to='en'):

        appid = '20200329000407787'
        secretKey = 'qsUZtDyxbnMWovo0hUDE'  
        httpClient = None
        myurl = '/api/trans/vip/translate'

        fromLang = from_Lang  # Language used
        toLang = to  #  Language used

        salt = random.randint(32768, 65536)
        sign = appid + q + str(salt) + secretKey
        sign = hashlib.md5(sign.encode()).hexdigest()
        myurl = myurl + '?appid=' + appid + '&q=' + urllib.parse.quote(
            q) + '&from=' + fromLang + '&to=' + toLang + '&salt=' + str(
            salt) + '&sign=' + sign

        try:
            httpClient = http.client.HTTPConnection('api.fanyi.baidu.com')
            httpClient.request('GET', myurl)

            # response Http
            response = httpClient.getresponse()
            result_all = response.read().decode("utf-8")
            result = json.loads(result_all)
            reply = result["trans_result"][0]["dst"]

        except Exception as e:
            reply = "I am sorry, I do not understand !"
        finally:
            if httpClient:
                httpClient.close()
        return reply

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "AI Chatbot"))
        self.pushButton.setText(_translate("MainWindow", "sent"))
        self.label.setText(_translate("MainWindow", "Chatting information："))


if __name__ == "__main__":

    app = QtWidgets.QApplication(sys.argv)
    widget = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(widget)
    widget.show()
    sys.exit(app.exec_())
