class FlatMatrix(object):

    def __init__(self, width, height, new_state=None):
        self.width = width
        self.height = height
        if new_state:
            self.data = new_state
        else:
            self.data = [0 for x in range(width * height)]

    def __idx(self, i, j):
        return j * self.width + i

    def get(self, i, j):
        return self.data[self.__idx(i, j)]

    def set(self, i, j, val, clone=True):
        if clone:
            new_state = [x for x in self.data]
            new_state[self.__idx(i, j)] = val
            return FlatMatrix(self.width, self.height, new_state)
        else:
            self.data[self.__idx(i, j)] = val
            return self

    def __str__(self):
        buf = []
        for j in range(self.height):
            for i in range(self.width):
                buf += "%d " % self.data[self.__idx(i, j)]
            buf += "\n"
        return ''.join(buf)