class FlatMatrix(object):

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.data = [0 for x in range(width * height)]

    def __idx(self, i, j):
        return j * self.width + i

    def get(self, i, j):
        return self.data[self.__idx(i, j)]

    def set(self, i, j, val):
        self.data[self.__idx(i, j)] = val

    def __str__(self):
        str = []
        for j in range(self.height):
            for i in range(self.width):
                str += "%d " % self.data[self.__idx(i, j)]
            str += "\n"
        return ''.join(str)