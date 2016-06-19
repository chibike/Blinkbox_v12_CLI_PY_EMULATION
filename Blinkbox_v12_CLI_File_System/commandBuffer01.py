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

c = CommandBuffer(5)
