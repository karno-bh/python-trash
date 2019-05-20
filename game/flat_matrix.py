class FlatMatrix(object):

    def __init__(self, width, height, new_state=None):
        # type: (int, int, list[int]) -> FlatMatrix

        self.width = width
        self.height = height
        if new_state:
            self.data = new_state
        else:
            self.data = [0 for x in range(width * height)]

    def __idx(self, i, j):
        # type: (int, int) -> int

        return j * self.width + i

    def get(self, i, j):
        # type: (int, int) -> int

        return self.data[self.__idx(i, j)]

    def set(self, i, j, val, clone=True):
        # type: (int, int, int, bool) -> FlatMatrix

        if clone:
            new_state = [x for x in self.data]
            new_state[self.__idx(i, j)] = val
            return FlatMatrix(self.width, self.height, new_state)
        else:
            self.data[self.__idx(i, j)] = val
            return self

    def out_of_range(self, i, j):
        max_horizontal = self.width - 1
        max_vertical = self.height - 1
        return i < 0 or i > max_horizontal or i < 0 or i > max_vertical

    def __str__(self):
        buf = []
        for j in range(self.height):
            for i in range(self.width):
                placeholder = "%d" if i == 0 else " %d"
                buf += placeholder % self.data[self.__idx(i, j)]
            buf += "\n"
        return ''.join(buf)


__all__ = ['FlatMatrix']