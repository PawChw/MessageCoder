class Coder:
    chars = {'0': 0,
             '1': 1,
             '2': 2,
             '3': 3,
             '4': 4,
             '5': 5,
             '6': 6,
             '7': 7,
             '8': 8,
             '9': 9,
             'a': 10,
             'A': 11,
             'b': 12,
             'B': 13,
             'c': 14,
             'C': 15,
             'd': 16,
             'D': 17,
             'e': 18,
             'E': 19,
             'f': 20,
             'F': 21,
             'g': 22,
             'G': 23,
             'h': 24,
             'H': 25,
             'i': 26,
             'I': 27,
             'j': 28,
             'J': 29,
             'k': 30,
             'K': 31,
             'l': 32,
             'L': 33,
             'm': 34,
             'M': 35,
             'n': 36,
             'N': 37,
             'o': 38,
             'O': 39,
             'p': 40,
             'P': 41,
             'r': 42,
             'R': 43,
             's': 44,
             'S': 45,
             't': 46,
             'T': 47,
             'u': 48,
             'U': 49,
             'w': 50,
             'W': 51,
             'q': 52,
             'Q': 53,
             'y': 54,
             'Y': 55,
             'z': 56,
             'Z': 57,
             '!': 58,
             '"': 59,
             '#': 60,
             '$': 61,
             '%': 62,
             '&': 63,
             "'": 64,
             '(': 65,
             ')': 66,
             '*': 67,
             '+': 68,
             ',': 69,
             '-': 70,
             '.': 71,
             '/': 72,
             ':': 73,
             ';': 74,
             '<': 75,
             '=': 76,
             '>': 77,
             '?': 78,
             '@': 79,
             '[': 80,
             '\\': 81,
             ']': 82,
             '^': 83,
             '_': 84,
             '`': 85,
             '{': 86,
             '|': 87,
             '}': 88,
             '~': 89}

    @staticmethod
    def get_value(chr):
        value = Coder.chars.get(chr)
        if value is None:
            raise ValueError
        else:
            return value

    @staticmethod
    def get_chr(val):
        for key, value in Coder.chars.items():
            if val == value:
                return key
        raise ValueError

    @staticmethod
    def get_number(string):
        lenght = int(len(string))
        values = 0
        for count, value in enumerate(string):
            values += int(Coder.get_value(value)) * int(90 ** (lenght - count - 1))
        return values

    @staticmethod
    def get_string(value):
        if value == 0:
            return "0"
        s = ""
        a = 1
        while value != 0:
            tmp = value % (90 ** a)
            s = Coder.get_chr(tmp / (90 ** (a - 1))) + s
            value = value - tmp
            a += 1
        return s
