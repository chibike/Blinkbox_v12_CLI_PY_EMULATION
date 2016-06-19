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

class CommandBuffer():
    def __init__(self, buffer_size):
        self._buffer = ['']
        self._max_size = buffer_size + 1
        self._index = 0
    def scrollUp(self):
        if len(self._buffer) <= 0:
            return ''
        self._index -= 1
        if self._index < 0:
            self._index = 0
        return self._buffer[self._index]
    def scrollDown(self):
        if len(self._buffer) <= 0:
            return ''
        self._index += 1
        if self._index+1 >= len(self._buffer):
            self._index = len(self._buffer)-2
        return self._buffer[self._index]
    def appendCommand(self, command):
        if command == '':
            return
        else:
            self._index = len(self._buffer)
            self._buffer[self._index-1] = command
            self._buffer.append('')

            if len(self._buffer) > self._max_size:
                self._buffer = self._buffer[1:]
                self._index -= 1
            return
    def showArray(self):
        print self._buffer


class CommandInterface(QtGui.QGraphicsScene):
    def __init__(self, parent=None):
        super(CommandInterface, self).__init__(parent)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        self.setBackgroundBrush(brush)

        self._width = 0
        self._height = 0
        self._original_width = 1050
        self._original_height = 710

        self._WIN_PWD = os.getcwd()
        self._USER = ''
        self._PWD = '\\HOME'
        self._commandBuffer = CommandBuffer(30)
        
        self._input_mode = False
        self._current_line = None
        
        self._data_type = None
        self._data_collection_mode = None
        self._input_data = None
        
        self._line = 0
        self._column = 0
        self._current_line_start_column = 0
        self._length_of_current_line_buffer = 0
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
    def setSceneRect(self, x, y, width, height):
        self._width = width
        self._height = height
        return super(CommandInterface, self).setSceneRect(x, y, width, height)
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
        elif ( len(str( self._current_line.toPlainText() )) <= 0 ):
            return
        else:
            self.kursor = QtGui.QTextCursor(self._current_line.document())
            self.kursor.clearSelection()
            #self.kursor.movePosition(QtGui.QTextCursor.End, QtGui.QTextCursor.MoveAnchor)
            self.kursor.setPosition(self._column - self._current_line_start_column, QtGui.QTextCursor.MoveAnchor)
            self.kursor.deletePreviousChar()
            self._column -= 1
            point_size = self._current_line.font().pointSize()
            self._cursor.setPos(int(self._column*point_size*0.84),
                                int(1.5*self._line*point_size) + int(0.6*point_size))
            self._cursor.setData(0, [self._line, self._column])
            self._length_of_current_line_buffer = len(self._current_line.toPlainText())
            
    def printf( self, string, color=None ):
        if(self._current_line == None and color != None):
            self._current_line_start_column = self._column
            self._current_line = self.addText('', color)
            self.kursor = QtGui.QTextCursor(self._current_line.document())
            self.kursor.beginEditBlock()
            self.kursor.insertText(string)
            self.kursor.endEditBlock()

            point_size = self._current_line.font().pointSize()
            self._current_line.setPos(self._column*point_size*0.8, 1.5*self._line*point_size)
            self._current_line.setData(0, [self._line, self._column])
        elif ( self._current_line == None and color == None ):
            self._current_line_start_column = self._column
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
            #self.kursor.movePosition(QtGui.QTextCursor.End, QtGui.QTextCursor.MoveAnchor)
            self.kursor.setPosition(self._column - self._current_line_start_column, QtGui.QTextCursor.MoveAnchor)
            self.kursor.insertText(string)
        elif isinstance(self._current_line, QtGui.QGraphicsTextItem):
            self.kursor = QtGui.QTextCursor(self._current_line.document())
            self.kursor.clearSelection()
            #self.kursor.movePosition(QtGui.QTextCursor.End, QtGui.QTextCursor.MoveAnchor)
            self.kursor.setPosition(self._column - self._current_line_start_column, QtGui.QTextCursor.MoveAnchor)
            self.kursor.insertText(string)

        point_size = self._current_line.font().pointSize()
        
        self._column += len(string)
        self._length_of_current_line_buffer = len(self._current_line.toPlainText())
        self._cursor.setPos(int(self._column*point_size*0.84),
                            int(1.5*self._line*point_size) + int(0.6*point_size))
        self._cursor.setData(0, [self._line, self._column])
        return self._current_line
    def endprintf(self):
        self._current_line = None
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
            #self.kursor.movePosition(QtGui.QTextCursor.End, QtGui.QTextCursor.MoveAnchor)
            self.kursor.setPosition(self._column - self._current_line_start_column, QtGui.QTextCursor.MoveAnchor)
            self.kursor.insertText(string)
        elif isinstance(self._current_line, QtGui.QGraphicsTextItem):
            self.kursor = QtGui.QTextCursor(self._current_line.document())
            self.kursor.clearSelection()
            #self.kursor.movePosition(QtGui.QTextCursor.End, QtGui.QTextCursor.MoveAnchor)
            self.kursor.setPosition(self._column - self._current_line_start_column, QtGui.QTextCursor.MoveAnchor)
            self.kursor.insertText(string)

        point_size = self._current_line.font().pointSize()
        
        self._column = 0
        self._current_line_start_column = 0
        self._length_of_current_line_buffer = 0
        self._line += 1
        self._current_line = None
        self._cursor.setPos(int(self._column*point_size*0.84),
                            int(1.5*self._line*point_size) + int(0.6*point_size))
        self._cursor.setData(0, [self._line, self._column])
        if( self._line > 36):
            self.setSceneRect(0, 0, self._width, self._height+18)
        self.setFocusItem(self._cursor)
        self._focus_on_cursor = True
        return self._current_line
    def replacef(self, string, color=None):
        if(self._current_line != None and color == None):
            self._column = self._column - len(self._current_line.toPlainText())
            self.kursor = QtGui.QTextCursor(self._current_line.document())
            self.kursor.clearSelection()
            self.kursor.movePosition(QtGui.QTextCursor.Start, QtGui.QTextCursor.MoveAnchor)
            self.kursor.movePosition(QtGui.QTextCursor.End, QtGui.QTextCursor.KeepAnchor)
            self.kursor.deleteChar()
            self.printf(string)
        elif(self._current_line != None and color != None):
            self._column = self._column - len(self._current_line.toPlainText())
            self._current_line.setDefaultTextColor(color)
            self.kursor = QtGui.QTextCursor(self._current_line.document())
            self.kursor.clearSelection()
            self.kursor.movePosition(QtGui.QTextCursor.Start, QtGui.QTextCursor.MoveAnchor)
            self.kursor.movePosition(QtGui.QTextCursor.End, QtGui.QTextCursor.KeepAnchor)
            self.kursor.deleteChar()
            self.printf(string)
        else:
            return
    
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
    def getCursor(self):
        if self._focus_on_cursor == True:
            self._focus_on_cursor = False
            return self._cursor
        else:
            return None
    def clearUi(self):
        self.clear()
        self.setSceneRect(0, 0, self._original_width, self._original_height)
        self._line = 0
        self._column = 0
        self._cursor = self.addRect(0,0, 10,10)
        self._cursor.setData(0, [self._line, self._column])
        self._cursor.setBrush(self._cursor_on_brush)
        self._cursor.setPen(self._cursor_pen)
        self._cursor_state = True
        self.updateCursor()
    def updateCursor(self):
        point_size = self.font().pointSize()
        pos = self._cursor.data(0).toList()
        line = pos[0].toInt()[0]
        column = pos[1].toInt()[0]
        x = int(column*point_size*0.9)+2
        y = int(1.5*self._line*point_size) + int(point_size)
        width = int(0.2 * point_size)
        height = int(1.4 * point_size)
        self._cursor.setRect(0, 0, width, height)
        self._cursor.setPos(x,y)
    def inputf( self, prompt, data_type='' ):
        self._input_mode = True
        self.printf(prompt, QtGui.QColor(0,255,0))
        self.endprintf()
        self.printf('', QtGui.QColor(0,255,0))
        self._data_type = data_type
        self._input_data = ''
    def keyPressEvent(self, event):
        super(CommandInterface, self).keyPressEvent(event)
        if self._input_mode == True:
            key = event.text()
            if key == '\n' or key == '\r':
                data = str(self._input_data)
                self.println("")
                self._input_mode = False
                self.processData(data)
            elif key == '\b':
                self._input_data = removeChar(self._input_data, self._column - self._current_line_start_column)
                self.backspace()
                #self._input_data = self._input_data[:-1]
            elif key == '\t':
                print "Tab btn"
            elif str(event.key()) == '16777235':#KEY DOWN
                if self._data_type != "__password__" and self._data_type != "__username__":
                    self._input_data = self._commandBuffer.scrollUp()
                    self.replacef( self._input_data )
            elif str(event.key()) == '16777237':#KEY DOWN
                if self._data_type != "__password__" and self._data_type != "__username__":
                    self._input_data = self._commandBuffer.scrollDown()
                    self.replacef( self._input_data )
            elif str(event.key()) == '16777234':#KEY LEFT
                if self._column <= self._current_line_start_column:
                    self._column = self._current_line_start_column
                else:
                    self._column -= 1
                point_size = self.font().pointSize()
                self._cursor.setPos(int(self._column*point_size*0.84),
                                    int(1.5*self._line*point_size) + int(0.6*point_size))
                self._cursor.setData(0, [self._line, self._column])
            elif str(event.key()) == '16777236':#KEY RIGHT
                if self._column >= (self._current_line_start_column + self._length_of_current_line_buffer):
                    self._column = self._current_line_start_column + self._length_of_current_line_buffer
                else:
                    self._column += 1
                point_size = self.font().pointSize()
                self._cursor.setPos(int(self._column*point_size*0.84),
                                    int(1.5*self._line*point_size) + int(0.6*point_size))
                self._cursor.setData(0, [self._line, self._column])
            elif str(event.key()) == '16777223':
                print "Delete btn"
            elif str(event.key()) == '16777232':
                print "Home btn"
            elif str(event.key()) == '16777233':
                print "End btn"
            elif str(event.key()) == '16777238':
                print "PgUp btn"
            elif str(event.key()) == '16777239':
                print "PgDn btn"
            elif str(event.key()) == '16777252':
                print "Caps btn"
            elif str(event.key()) == '16777248':
                print "Shift btn"
            elif str(event.key()) == '16777250':
                print "Ctrl btn"
            elif str(event.key()) == '16777251':
                print "Window btn"
            elif str(event.key()) == '16777216':
                print "Alt btn"
            elif str(event.key()) == '16777239':
                print "Esc btn"
            else:
                self._input_data = insertChar(self._input_data, str(key), self._column - self._current_line_start_column)
                if self._data_type != "__password__":
                    self.printf(str(key))
                else:
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
                        self._USER = self._bucket+"@"+data
                        self._data_collection_mode = "__command__"
                        self.inputf( self._USER+" "+self._PWD+" > ",
                                     "__command__" )
                    else:
                        self.verifyUser()
                except:
                    self.verifyUser()
            else:
                pass
        elif self._data_collection_mode == "__bool__":
            data = data.lower()
            if data == 'y':
                data = True
            else:
                data = False
            if self._data_type == "__delete_confirmation__":
                if data:
                    self.processRemoveCmd( self._bucket, self._PWD )
                else:
                    pass
            self._data_collection_mode = "__command__"
            self.inputf( self._USER+" "+self._PWD+" > ",
                         "__command__" )
        elif self._data_collection_mode == "__command__":
            self._commandBuffer.appendCommand(data)
            if data.startswith('ls'):
                self.processListDirCmd( data[2:], self._PWD )
            elif data.startswith("cd"):
                self._PWD = self.processChangeDirCmd( data[2:], self._PWD )
            elif data.startswith("mkdir"):
                self.processMakeDirCmd( data[5:], self._PWD )
            elif data.startswith("rm"):
                self._bucket = data[2:]
                self._data_collection_mode = "__bool__"
                self.inputf( "Are you sure<y/n> : ",
                             "__delete_confirmation__" )
                return
            elif data.startswith("cat "):
                self.processCatCmd( data[4:], self._PWD )
            elif data.startswith("tree ") or ( data.startswith("tree") and len(data) == 4 ):
                self.processTreeCmd( data[4:], self._PWD )
            elif data.startswith("touch "):
                self.processTouchCmd( data[6:], self._PWD )
            elif data == "clear":
                self.processClearCmd()
            elif data == '':
                pass
            elif data == 'exit':
                pass
            else:
                self.println(data+" is not a valid Blinkbox_v12 Shell command")
            self._data_collection_mode = "__command__"
            self.inputf( self._USER+" "+self._PWD+" > ",
                         "__command__" )
        else:
            pass
    def processClearCmd(self):
        self.clearUi()
    def processRemoveCmd( self, options, current_dir ):
        options = options.lstrip().rstrip().split(' ')
        File = options[0]
        if File == '':
            self.println("ERROR could not remove file")
        elif File.startswith('\\'):
            try:
                os.remove(self._WIN_PWD+'\\'+File)
            except OSError:
                self.println("ERROR directory is not empty")
            except:
                try:
                    os.removedirs(self._WIN_PWD+'\\'+File)
                except OSError:
                    self.println("ERROR directory is not empty")
                except:
                    self.println("ERROR could not remove")
        elif File.count('.') == 1:
            try:
                os.remove(self._WIN_PWD+current_dir+'\\'+File)
            except:
                self.println("ERROR could not remove file")
        else:
            try:
                os.removedirs(self._WIN_PWD+current_dir+'\\'+File)
            except OSError:
                self.println("ERROR directory is not empty")
            except:
                self.println("ERROR could not remove directory")
      
    def processTouchCmd( self, options, current_dir ):
        options = options.lstrip().rstrip().split(' ')
        if options[0] == '':
            self.println("ERROR invalid filename")
            return
        filename = options[0]
        if filename.count('.') <= 0:
            filename = filename + '.txt'
        try:
            open(filename, 'w').close()
        except:
            self.println("ERROR could not create file")
    
    def processTreeCmd( self, options, current_dir, tab_index=0 ):
        options = options.lstrip().rstrip().split(' ')
        if options[0] == '':
            self.println( self.processTabs( self.getTabs(tab_index) ) + current_dir.split('\\')[-1] )
            tab_index += 1
            for filename in os.listdir( self._WIN_PWD+'\\'+current_dir ):
                if filename.count('.') <= 0:# is directory
                    self.processTreeCmd( '', current_dir+'\\'+filename, tab_index )
                else:
                    self.println( self.processTabs( self.getTabs(tab_index) ) + filename )
        else:
            filename = options[0]
            if filename.startswith('\\'):
                self.processTreeCmd( '', filename, 0 )
            else:
                self.processTreeCmd( '', current_dir+'\\'+filename, 0)

    def processTabs( self, tabs ):
        if len(tabs) <= 0:
            return ''
        suffix = '|___ '
        string = ''
        for i in range( len(tabs)-1 ):
            string = string + '|    '
        return string+suffix

    def getTabs(self, length):
        tabs = ''
        for i in range(length):
            tabs = tabs + '\t'
        return tabs

    def processCatCmd( self, options, current_dir ):
        options = options.lstrip().rstrip().split(' ')
        length = 50
        if options[0] == '':
            self.println("ERROR invalid filename")
            return
        elif len(options) > 1:
            try:
                length = int(options[1])
            except:
                length = 50
        filename = options[0]
        try:
            File = open(filename, 'r')
            self.println("")
            self.println("--- "+filename.upper()+" ---")
            self.println(str(File.read(length)))
            self.println("*** "+filename.upper()+" ***")
            self.println("")
            File.close()
        except:
            self.println("ERROR could not open file")
    def processMakeDirCmd( self, options, current_dir ):
        options = options.lstrip().rstrip().split(' ')
        directory = options[0]
        if directory == "":
            self.println("ERROR could not create directory")
        elif directory.startswith("\\"):
            try:
                os.mkdir(self._WIN_PWD+directory)
            except:
                self.println("ERROR could not create directory")
        else:
            try:
                os.mkdir(self._WIN_PWD+current_dir+"\\"+directory)
            except:
                self.println("ERROR could not create directory")
    def processChangeDirCmd( self, options, current_dir ):
        options = options.lstrip().rstrip().split(' ')[0]
        if options == '':
            PWD = "\\HOME"
        elif options == '.':
            PWD = "\\"
        elif options == '..':
            PWD = self.getPreviousDir( current_dir )
        else:
            PWD = self.gotoDir( options )
        return PWD
    def gotoDir( self, directory ):
        directory = directory.lstrip().rstrip()
        PWD = ''
        if directory.startswith("\\"):
            try:
                os.chdir(self._WIN_PWD+directory)
                PWD = directory
            except:
                self.println("ERROR invalid directory")
                return self._PWD
        else:
            try:
                os.chdir(self._WIN_PWD+self._PWD+'\\'+directory)
                PWD = self._PWD + '\\' + directory
            except:
                self.println("ERROR invalid directory")
                return self._PWD
        return PWD
    def getPreviousDir( self, current_dir ):
        demarkerAt = self.stringFind( current_dir, "\\" )
        if current_dir == '' or demarkerAt == [] or len(demarkerAt) == 1:
            return '\\'
        else:
            return current_dir[:demarkerAt[-1]]
    def stringFind( self, string, find ):
        indexes = []
        for i in range(0, len(string)-len(find), 1):
            if string[i:i+len(find)] == find:
                indexes.append(i)
        return indexes
    def processListDirCmd( self, options, current_dir ):
        if options == '':
            self.runListDir( current_dir )
    def runListDir( self, current_dir ):
        os.chdir(self._WIN_PWD+current_dir)
        filenames = os.listdir(self._WIN_PWD+current_dir)
        total = len(filenames)
        self.println("Total number of files = "+str(total))
        for filename in filenames:
            self.println(filename)
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

def insertChar(string, char, index):#is zero indexed
    return string[:index] + char + string[index:]

def removeChar(string, index):#is zero indexed
    stringArray = [char for char in string]
    stringArray.pop(index)
    string = ''
    for i in stringArray:
        string = string + i
    return string
