from PyQt4 import QtCore, QtGui

import os,sys
try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)


class CommandInterface(QtGui.QGraphicsScene):
    def __init__(self, parent=None):
        super(CommandInterface, self).__init__(parent)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        self.setBackgroundBrush(brush)

        self._line = 0
        self._column = 0
        self._cursor = self.addRect(0,0, 10,10)
        self._cursor.setData(0, [self._line, self._column])
        
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Courier"))
        font.setPointSize(12)
        font.setBold(False)#font.setWeight(QtCore.QFont.Bold)
        self.setFont(font)

        self._cursor_on_brush = QtGui.QBrush()
        self._cursor_on_brush.setStyle(QtCore.Qt.SolidPattern)
        self._cursor_on_brush.setColor(QtGui.QColor(0, 255, 0))

        self._cursor_off_brush = QtGui.QBrush()
        self._cursor_off_brush.setStyle(QtCore.Qt.SolidPattern)
        self._cursor_off_brush.setColor(QtGui.QColor(0, 0, 0))

        self._cursor_pen = QtGui.QPen()
        self._cursor_pen.setColor(QtGui.QColor(0, 255, 0))
        self._cursor_pen.setStyle(QtCore.Qt.SolidLine)
        
        self._cursor.setBrush(self._cursor_on_brush)
        self._cursor.setPen(self._cursor_pen)
        self._cursor_state = True
    def setFont(self, font):
        return_obj = super(CommandInterface, self).setFont(font)
        self.updateCursor()
        return return_obj
    def addText( self, text, font, color):
        textItem = super(CommandInterface, self).addText(text, font)
        textItem.setDefaultTextColor(color)
        return textItem
    def printf( self, string, font, color ):
        textItem = self.addText(string, font, color)
        point_size = textItem.font().pointSize()
        
        textItem.setPos(self._column*point_size*0.8, self._line*point_size)
        textItem.setData(0, [self._line, self._column])
        
        self._column += len(string)
        x = int(self._column*point_size*0.84)
        y = int(self._line*point_size) + int(0.6 * point_size)
        #print "(line,column) =",(self._line,self._column)
        #print "(x,y) =",(x,y)
        self._cursor.setPos(x, y)
        self._cursor.setData(0, [self._line, self._column])
        return textItem
    def println( self, string, font, color ):
        textItem = self.addText(string, font, color)
        point_size = textItem.font().pointSize()
        
        textItem.setPos(self._column*point_size*0.8, self._line*point_size)
        textItem.setData(0, [self._line, self._column])
        
        self._line += 1
        self._column = 0
        self._cursor.setPos(int(self._column*point_size*0.84),
                            int(self._line*point_size) + int(0.0 * point_size))
        self._cursor.setData(0, [self._line, self._column])
        return textItem
    def blinkCursor(self):
        if self._cursor_state == False:
            self._cursor_pen.setStyle(QtCore.Qt.SolidLine)
            self._cursor.setBrush(self._cursor_on_brush)
            self._cursor_state = True
        else:
            self._cursor_pen.setStyle(QtCore.Qt.NoPen)
            self._cursor.setBrush(self._cursor_off_brush)
            self._cursor_state = False
        self._cursor.setPen(self._cursor_pen)
    def updateCursor(self):
        point_size = self.font().pointSize()
        pos = self._cursor.data(0).toList()
        line = pos[0].toInt()[0]
        column = pos[1].toInt()[0]
        x = int(column*point_size*0.9)+2
        y = int(line*point_size) + int(1.2 * point_size)
        width = int(0.2 * point_size)
        height = int(1.4 * point_size)
        self._cursor.setRect(0, 0, width, height)
        self._cursor.setPos(x,y)
    def inputf( self ):
        pass

def fileParseCsvData(filename):
    try:
        with open(filename, 'r') as file:
            f = file.read()
            file.close()
            p = f.split(',')
            return p
    except TypeError:
        return ["ERROR"]


'''
while(1):
            try:
                self.commandInterface.println("Username: ", self.commandInterface.font(), QtGui.QColor(0,0,255))
                ssid = raw_input("Username: ")
                self.commandInterface.println("Password: ", self.commandInterface.font(), QtGui.QColor(0,0,255))
                key = raw_input("Password: ")
                if users[ssid] == key:
                    self.USER = ssid + "@" + key
                    break
                else:
                    raise NameError()
            except TypeError:
                continue
'''
