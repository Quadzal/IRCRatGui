from PyQt5 import QtCore, QtGui, QtWidgets
import time, socket, threading

class Ui_MainWindow(object):

    def __init__(self):
        self.SERVER = "irc.freenode.net"
        self.KANAL = input("Kanal'ı Giriniz: ")
        if not self.KANAL.startswith("#"):
            print("Kanal İsminin Başına Lütfen # Koyunuz.")
            exit()
        self.ISIM = input("Nickinizi Giriniz: ")

        self.baglan = socket.socket()
        self.baglan.connect((self.SERVER, 6667))
        self.baglan.send(bytes("USER " + self.ISIM + " " + self.ISIM + " " +
                               self.ISIM + " " + self.ISIM + "\n", "UTF-8"))
        self.baglan.send(bytes("NICK " + self.ISIM + "\n", "UTF-8"))
        self.baglan.send(bytes("JOIN " + self.KANAL + "\n", "UTF-8"))
        while 1:
            ircmsg = self.baglan.recv(2048).decode("UTF-8")
            ircmsg = ircmsg.strip('\n\r')
            if "End of /NAMES list" in ircmsg:
                break
        time.sleep(3)


    def sendmsg(self):
        self.baglan.send(bytes("PRIVMSG " + self.KANAL +
                                " :" + str(self.get_command.toPlainText()) + "\n", "UTF-8"))
        time.sleep(1)
        ircmsg = self.baglan.recv(1024).decode("UTF-8")
        self.item = QtGui.QStandardItem("Bot Message: " + ircmsg.split(":")[2])
        self.model.appendRow(self.item)

    def thread_calistir(self):
        t1=threading.Thread(target = self.sendmsg)
        t1.start()

    def createListbox(self):
        self.command_list = QtWidgets.QListView(self.centralwidget)
        self.command_list.setGeometry(QtCore.QRect(0, 60, 791, 381))
        self.command_list.setObjectName("command_list")
        self.model = QtGui.QStandardItemModel()
        self.command_list.setModel(self.model)

    def createPushButton(self):
        self.send_command = QtWidgets.QPushButton(self.centralwidget)
        self.send_command.setGeometry(QtCore.QRect(350, 0, 111, 61))
        font = QtGui.QFont()
        font.setFamily("Arial Black")
        font.setPointSize(8)
        font.setBold(True)
        font.setItalic(False)
        font.setUnderline(False)
        font.setWeight(75)
        font.setStrikeOut(False)
        font.setKerning(True)
        self.send_command.setFont(font)
        self.send_command.setObjectName("send_command")
        self.send_command.clicked.connect(self.thread_calistir)

    def createScrollbar(self):
        self.scrollbar = QtWidgets.QScrollBar(self.centralwidget)
        self.scrollbar.setGeometry(QtCore.QRect(790, 0, 20, 441))
        self.scrollbar.setOrientation(QtCore.Qt.Vertical)
        self.scrollbar.setObjectName("scrollbar")

    def createTextedit(self):
        self.get_command = QtWidgets.QTextEdit(self.centralwidget)
        self.get_command.setGeometry(QtCore.QRect(0, 20, 341, 31))
        self.get_command.setObjectName("get_command")

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(815, 467)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.createPushButton()
        self.createScrollbar()
        self.createTextedit()
        self.createListbox()
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.send_command.setText(_translate("MainWindow", "Send Command"))


if __name__=="__main__":
     import sys
     app = QtWidgets.QApplication(sys.argv)
     MainWindow = QtWidgets.QMainWindow()
     ui = Ui_MainWindow()
     ui.setupUi(MainWindow)
     MainWindow.show()
     sys.exit(app.exec_())