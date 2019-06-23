class FlatMatrix(object):

    def __init__(self, width, height, new_state=None, initial_val=0):
        # type: (int, int, list[any], any) -> FlatMatrix

        self.width = width
        self.height = height
        if new_state:
            self.data = new_state
        else:
            self.data = [initial_val for x in range(width * height)]

    def __idx(self, i, j):
        # type: (int, int) -> int

        return j * self.width + i

    def get(self, i, j):
        # type: (int, int) -> any

        return self.data[self.__idx(i, j)]

    def set(self, i, j, val, clone=True):
        # type: (int, int, any, bool) -> FlatMatrix

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
        return i < 0 or i > max_horizontal or j < 0 or j > max_vertical

    def __str__(self):
        buf = []
        for j in range(self.height):
            for i in range(self.width):
                placeholder = "{0}" if i == 0 else " {0}"
                buf += placeholder.format(self.data[self.__idx(i, j)])
            buf += "\n"
        return ''.join(buf)

    def pretty_log(self, replace):
        buf = []
        for j in range(self.height - 1, -1, -1):
            for i in range(self.width):
                placeholder = "{0}" if i == 0 else " {0}"
                buf += placeholder.format(replace[self.data[self.__idx(i, j)]])
            buf += "\n"
        return ''.join(buf)

    def __mul__(self, other):
        if isinstance(other, FlatMatrix):
            if self.width != other.height:
                raise Exception("Other instance is FlatMatrix but current matrix width != other matrix height")
            result = FlatMatrix(self.height, other.width)
            possible_zero = 0
            if isinstance(self.data[0], float):
                possible_zero = 0.0
            for i in range(self.height):
                for j in range(other.width):
                    res_el = possible_zero
                    for k in range(self.width):
                        res_el += self.get(k, i) * other.get(j, k)
                    result.set(i, j, res_el, clone=False)
            return result
        elif isinstance(other, list):
            if self.width != len(other):
                raise Exception("Other instance is list but current matrix width != other list length")
            possible_zero = 0
            if isinstance(self.data[0], float):
                possible_zero = 0.0
            # result = [possible_zero for t in range(self.height)]
            result = []
            for i in range(self.height):
                res_el = possible_zero
                for j in range(self.width):
                    res_el += self.get(j, i) * other[j]
                result.append(res_el)
            return result


__all__ = ['FlatMatrix']


def __test_mul_matrix():
    left_data = [
        1., 2., 3., 4.,
        5., 6., 7., 8.,
    ]
    left = FlatMatrix(4, 2, new_state=left_data)

    right_data = [
        1., 2.,
        1., 2.,
        1., 2.,
        1., 2.,
    ]
    right = FlatMatrix(2, 4, new_state=right_data)

    res = left * right

    print res


def __test_mul_vector():
    left_data = [
        1., 2., 3.,
        4., 5., 6.,
    ]
    left = FlatMatrix(3, 2, new_state=left_data)
    right = [2., 2., 2.]
    result = left * right

    print result


if __name__ == '__main__':
    __test_mul_matrix()
    __test_mul_vector()