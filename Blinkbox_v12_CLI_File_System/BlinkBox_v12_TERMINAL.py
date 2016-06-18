from BlinkBox_v12_TERMINAL_Header import*
from BlinkBox_v12_TERMINAL_Header import _translate, _fromUtf8
from BlinkBox_v12_TERMINAL_Header import fileParseCsvData

class Ui_MainWindow(QtGui.QMainWindow):
    def __init__(self):
        super(Ui_MainWindow, self).__init__()
        self.setupUi()
        self.timer = QtCore.QTimer()
        self.timer.setInterval(500)
        self.timer.timeout.connect(self.timerEvent)
        self.timer.start()
        
    def setupUi(self):
        self.setObjectName(_fromUtf8("Ui_MainWindow"))
        self.resize(1080, 800)
        self.setMaximumSize(QtCore.QSize(1080, 800))
        self.setWindowIcon(QtGui.QIcon("logo01.png"))
        
        self.centralwidget = QtGui.QWidget(self)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))

        self.verticallayout = QtGui.QVBoxLayout(self.centralwidget)
        self.verticallayout.setObjectName(_fromUtf8("verticallayout"))
        
        self.commandInterface = CommandInterface()
        self.commandInterface.setSceneRect(0, 0, 1060, 720)
        
        self.graphicsView = QtGui.QGraphicsView( self.commandInterface )
        self.graphicsView.setGeometry(QtCore.QRect(0, 0, 1080, 740))
        self.graphicsView.setMaximumSize(QtCore.QSize(1080, 740))
        #self.graphicsView.centerOn(self.commandInterface.items()[0])
        self.verticallayout.addWidget(self.graphicsView)

        self.graphicsView.setObjectName(_fromUtf8("graphicsView"))
        self.commandInterface.setObjectName(_fromUtf8("commandInterface"))
        self.setCentralWidget(self.centralwidget)

        self.statusbar = QtGui.QStatusBar(self)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        self.setStatusBar(self.statusbar)

        self.menubar = QtGui.QMenuBar(self)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1080, 31))
        self.menubar.setObjectName(_fromUtf8("menubar"))

        self.menuConnections = QtGui.QMenu(self.menubar)
        self.menuConnections.setObjectName(_fromUtf8("menuConnections"))

        self.menuShutdown = QtGui.QMenu(self.menubar)
        self.menuShutdown.setObjectName(_fromUtf8("menuShutdown"))

        self.setMenuBar(self.menubar)
        self.actionConnections = QtGui.QAction(self)
        self.actionConnections.setObjectName(_fromUtf8("actionConnections"))
        self.actionFont = QtGui.QAction(self)
        self.actionFont.setObjectName(_fromUtf8("actionFont"))
        self.actionSleep = QtGui.QAction(self)
        self.actionSleep.setObjectName(_fromUtf8("actionSleep"))
        self.actionShutdown = QtGui.QAction(self)
        self.actionShutdown.setObjectName(_fromUtf8("actionShutdown"))
        self.actionRestart = QtGui.QAction(self)
        self.actionRestart.setObjectName(_fromUtf8("actionRestart"))
        self.menuConnections.addAction(self.actionConnections)
        self.menuConnections.addAction(self.actionFont)
        self.menuShutdown.addAction(self.actionSleep)
        self.menuShutdown.addAction(self.actionShutdown)
        self.menuShutdown.addAction(self.actionRestart)
        self.menubar.addAction(self.menuShutdown.menuAction())
        self.menubar.addAction(self.menuConnections.menuAction())

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)
        self.start()
    def retranslateUi(self):
        self.setWindowTitle(_translate("Ui_MainWindow", "Blinkbox_v12 Shell", None))
        self.menuConnections.setTitle(_translate("Ui_MainWindow", "Settings", None))
        self.menuShutdown.setTitle(_translate("Ui_MainWindow", "Power", None))
        self.setCentralWidget(self.centralwidget)
        self.actionConnections.setText(_translate("Ui_MainWindow", "Connections", None))
        self.actionFont.setText(_translate("Ui_MainWindow", "Fonts", None))
        #self.actionFont.setShortcut("")
        self.actionFont.setStatusTip("Edit Font")
        self.actionFont.triggered.connect(self.editFont)
        self.actionSleep.setText(_translate("Ui_MainWindow", "Sleep", None))
        self.actionShutdown.setText(_translate("Ui_MainWindow", "Shutdown", None))
        self.actionRestart.setText(_translate("Ui_MainWindow", "Restart", None))
        self.show()
    def start(self):
        self.commandInterface.printf("Blink_v12 Shell 1.1 [on Blink Os v12]", self.commandInterface.font(), QtGui.QColor(0,255,0))
        ssids = fileParseCsvData("SSIDS.txt")
        keys = fileParseCsvData("KEYS.txt")
        users = dict(zip(ssids, keys))
        #self.commandInterface.println("Username: ", self.commandInterface.font(), QtGui.QColor(0,0,255))

    def timerEvent(self):
        self.commandInterface.blinkCursor()
    def editFont(self):
        font, valid = QtGui.QFontDialog.getFont()
        if valid:
            self.commandInterface.setFont(font)
            for item in self.commandInterface.items():
                try:
                    item_font = item.font()
                    item.setFont(font)
                    pos = item.data(0).toList()
                    line = pos[0].toInt()[0]
                    column = pos[1].toInt()[0]
                    point_size = item.font().pointSize()
                    item.setPos(0.9*point_size*column, 1.5*point_size*line)

                    if item_font.bold() == True:
                        type_style_font = item.font()
                        type_style_font.setBold(True)
                        item.setFont( type_style_font )
                    else:
                        type_style_font = item.font()
                        type_style_font.setBold(False)
                        item.setFont( type_style_font )

                    if item_font.italic() == True:
                        type_style_font = item.font()
                        type_style_font.setItalic(True)
                        item.setFont( type_style_font )
                    else:
                        type_style_font = item.font()
                        type_style_font.setItalic(False)
                        item.setFont( type_style_font )

                    if item_font.underline() == True:
                        type_style_font = item.font()
                        type_style_font.setUnderline(True)
                        item.setFont( type_style_font )
                    else:
                        type_style_font = item.font()
                        type_style_font.setUnderline(False)
                        item.setFont( type_style_font )

                    if item_font.strikeout() == True:
                        type_style_font = item.font()
                        type_style_font.setStrikeOut(True)
                        item.setFont( type_style_font )
                    else:
                        type_style_font = item.font()
                        type_style_font.setStrikeOut(False)
                        item.setFont( type_style_font )
                    
                except AttributeError:
                    continue
                except:
                    print("ERROR")
        else:
            pass


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    ui = Ui_MainWindow()
    sys.exit(app.exec_())

