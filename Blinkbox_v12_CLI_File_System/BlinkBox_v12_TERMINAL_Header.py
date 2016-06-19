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

        self._input_mode = False
        self._current_line = None

        self._data_type = None
        self._data_collection_mode = None
        self._input_data = None
        
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
    def addText( self, text, color):
        textItem = super(CommandInterface, self).addText(text, self.font())
        textItem.setDefaultTextColor(color)
        self._current_text_edit = textItem
        return textItem
    def backspace(self):
        if ( self._current_line == None or not(isinstance(self._current_line, QtGui.QGraphicsTextItem)) ):
            return
        else:
            self.kursor = QtGui.QTextCursor(self._current_line.document())
            self.kursor.clearSelection()
            self.kursor.movePosition(QtGui.QTextCursor.End, QtGui.QTextCursor.MoveAnchor)
            self.kursor.deletePreviousChar()
            self._column -= 1
            point_size = self._current_line.font().pointSize()
            self._cursor.setPos(int(self._column*point_size*0.84),
                                int(self._line*point_size) + int(0.6 * point_size))
            self._cursor.setData(0, [self._line, self._column])
            
    def printf( self, string, color=None ):
        if(self._current_line == None and color != None):
            self._current_line = self.addText('', color)
            self.kursor = QtGui.QTextCursor(self._current_line.document())
            self.kursor.beginEditBlock()
            self.kursor.insertText(string)
            self.kursor.endEditBlock()

            point_size = self._current_line.font().pointSize()
            self._current_line.setPos(self._column*point_size*0.8, 1.5*self._line*point_size)
            self._current_line.setData(0, [self._line, self._column])
        elif ( self._current_line == None and color == None ):
            self._current_line = self.addText('', QtGui.QColor(0,255,0))
            self.kursor = QtGui.QTextCursor(self._current_line.document())
            self.kursor.beginEditBlock()
            self.kursor.insertText(string)
            self.kursor.endEditBlock()

            point_size = self._current_line.font().pointSize()
            self._current_line.setPos(self._column*point_size*0.8, 1.5*self._line*point_size)
            self._current_line.setData(0, [self._line, self._column])
        elif ( self._current_line != None and color != None ):
            self._current_line.setDefaultTextColor(color)
            self.kursor = QtGui.QTextCursor(self._current_line.document())
            self.kursor.clearSelection()
            self.kursor.movePosition(QtGui.QTextCursor.End, QtGui.QTextCursor.MoveAnchor)
            self.kursor.insertText(string)
        elif isinstance(self._current_line, QtGui.QGraphicsTextItem):
            self.kursor = QtGui.QTextCursor(self._current_line.document())
            self.kursor.clearSelection()
            self.kursor.movePosition(QtGui.QTextCursor.End, QtGui.QTextCursor.MoveAnchor)
            self.kursor.insertText(string)

        point_size = self._current_line.font().pointSize()
        
        self._column += len(string)
        self._cursor.setPos(int(self._column*point_size*0.84),
                            int(1.2*self._line*point_size) + int(0.7 * point_size))
        self._cursor.setData(0, [self._line, self._column])
        return self._current_line

    def println( self, string, color=None):
        if(self._current_line == None and color != None):
            self._current_line = self.addText('', color)
            self.kursor = QtGui.QTextCursor(self._current_line.document())
            self.kursor.beginEditBlock()
            self.kursor.insertText(string)
            self.kursor.endEditBlock()
            point_size = self._current_line.font().pointSize()
            self._current_line.setPos(self._column*point_size*0.8, 1.5*self._line*point_size)
            self._current_line.setData(0, [self._line, self._column])
        elif ( self._current_line == None and color == None ):
            self._current_line = self.addText('', QtGui.QColor(0,255,0))
            self.kursor = QtGui.QTextCursor(self._current_line.document())
            self.kursor.beginEditBlock()
            self.kursor.insertText(string)
            self.kursor.endEditBlock()

            point_size = self._current_line.font().pointSize()
            self._current_line.setPos(self._column*point_size*0.8, 1.5*self._line*point_size)
            self._current_line.setData(0, [self._line, self._column])
        elif ( self._current_line != None and color != None ):
            self._current_line.setDefaultTextColor(color)
            self.kursor = QtGui.QTextCursor(self._current_line.document())
            self.kursor.clearSelection()
            self.kursor.movePosition(QtGui.QTextCursor.End, QtGui.QTextCursor.MoveAnchor)
            self.kursor.insertText(string)
        elif isinstance(self._current_line, QtGui.QGraphicsTextItem):
            self.kursor = QtGui.QTextCursor(self._current_line.document())
            self.kursor.clearSelection()
            self.kursor.movePosition(QtGui.QTextCursor.End, QtGui.QTextCursor.MoveAnchor)
            self.kursor.insertText(string)

        point_size = self._current_line.font().pointSize()
        
        self._column = 0
        self._line += 1
        self._current_line = None
        self._cursor.setPos(int(self._column*point_size*0.84),
                            int(1.2*self._line*point_size) + int(0.7 * point_size))
        self._cursor.setData(0, [self._line, self._column])
        return self._current_line
    
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
    def inputf( self, prompt, data_type='' ):
        self._input_mode = True
        self.printf(prompt, QtGui.QColor(0,255,0))
        self._data_type = data_type
        self._input_data = ''
    def keyPressEvent(self, event):
        super(CommandInterface, self).keyPressEvent(event)
        if self._input_mode == True:
            key = event.text()
            if key == '\n' or key == '\r':
                data = str(self._input_data)
                self.println(" ;")
                self._input_mode = False
                self.processData(data)
            elif key == '\b':
                self.backspace()
                self._input_data = self._input_data[:-1]
            elif key == '\t':
                print "Tab"
            else:
                self._input_data = self._input_data + str(key)
                if self._data_type != "__password__":
                    #self.printf(str(key), QtGui.QColor(0,255,0))
                    self.printf(str(key))
                else:
                    #self.printf("*", QtGui.QColor(0,255,0))
                    self.printf("*")
        return
    def processData(self, data):
        if self._data_collection_mode == "__verify_user__":
            if self._data_type == "__username__":
                self._bucket = data
                self._data_collection_mode = "__verify_user__"
                self.inputf( "Password: ", "__password__" )
            elif self._data_type == "__password__":
                ssids = fileParseCsvData("SSIDS.txt")
                keys = fileParseCsvData("KEYS.txt")
                users = dict(zip(ssids, keys))
                try:
                    if users[self._bucket] == data:
                        self.printf("Success")
                    else:
                        self.verifyUser()
                except:
                    self.verifyUser()
            else:
                pass
        elif self._data_collection_mode == "__command__":
            pass
        else:
            pass
    def verifyUser(self):
        self._data_collection_mode = "__verify_user__"
        self.inputf( "Username: ", "__username__" )
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
