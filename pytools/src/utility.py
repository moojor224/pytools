from enum import Enum as _Enum
from typing import Any as _Any


def getValueOrDefault(value, default):
    return value if value is not None else default


def logAndReturn(val):
    """
    prints and returns the value passed to it
    used for one-liners
    """
    print(val)
    return val


class _formatter:
    _reset = True

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], _Enum):
            args = args[0]
            self._chain = [args.value]
            return
        _chain = []
        for i in args:
            if isinstance(i, _formatter):
                _chain.extend(i._chain)
        self._chain = _chain
        pass

    def _prefix(self):
        return f"\x1B[{';'.join(str(p) for p in self._chain)}m"

    def __call__(self, *args, end="\n", sep=" ", file=None):
        print(f"{self._prefix()}", end="", file=file)
        print(*args, end="", sep=sep, file=file)
        if self._reset:
            print(PrintStyles.RESET._prefix(), end="", file=file)
        print(end, end="", file=file)

    def __add__(self, other):
        newFormatter = _formatter()
        newFormatter._chain = self._chain + other._chain
        return newFormatter

    def __sub__(self, other):
        myChain = list(self._chain)
        for i in other._chain:
            if i in myChain:
                myChain.remove(i)
        newFormatter = _formatter()
        newFormatter._chain = myChain
        return newFormatter


class PrintStyles(_formatter, _Enum):
    """
    normal usage:
    >>> printer = PrintStyles.BOLD + PrintStyles.RED + PrintStyles.ON_WHITE
    >>> printer("Hello, World!")

    styles can be used inline for one-time use:
    >>> (PrintStyles.ITALIC + PrintStyles.GREEN)("Inline styling example")
    >>> PrintStyles.BOLD("Another inline styling example")

    you can also disable the styles resetting if you want to
    >>> printer = PrintStyles.ITALIC + PrintStyles.BOLD + PrintStyles.RED
    >>> printer._reset = False
    >>> printer("disabled reset")
    >>> print("styles are still applied")
    >>> print("no changes here")
    >>> Formatter.reset()
    >>> print("back to normal")

    >>> warning = PrintStyles.BOLD + PrintStyles.YELLOW + PrintStyles.ITALIC
    >>> warning("This is an example warning!")

    >>> error = PrintStyles.BOLD + PrintStyles.ON_RED
    >>> error("This is an example error!")

    it is also possible to subtract styles from an already-compiiled style
    >>> printer = PrintStyles.MAGENTA + PrintStyles.BOLD + PrintStyles.ON_RED
    >>> printer("This is before subtracting")
    >>> printer = printer - PrintStyles.BOLD
    >>> printer = printer - PrintStyles.ON_RED
    >>> printer("This is after subtracting")

    note: PrintStyles can be imported as an alias for shorter code
    >>> from pytools import PrintStyles as S
    """

    # text colors
    BLACK = 30
    RED = 31
    GREEN = 32
    YELLOW = 33
    BLUE = 34
    MAGENTA = 35
    CYAN = 36
    WHITE = 37
    GREY = 90
    BRIGHT_RED = 91
    BRIGHT_GREEN = 92
    BRIGHT_YELLOW = 93
    BRIGHT_BLUE = 94
    BRIGHT_MAGENTA = 95
    BRIGHT_CYAN = 96
    BRIGHT_WHITE = 97
    # background colors
    BLACK_BG = 40
    RED_BG = 41
    GREEN_BG = 42
    YELLOW_BG = 43
    BLUE_BG = 44
    MAGENTA_BG = 45
    CYAN_BG = 46
    WHITE_BG = 47
    GREY_BG = 100
    BRIGHT_RED_BG = 101
    BRIGHT_GREEN_BG = 102
    BRIGHT_YELLOW_BG = 103
    BRIGHT_BLUE_BG = 104
    BRIGHT_MAGENTA_BG = 105
    BRIGHT_CYAN_BG = 106
    BRIGHT_WHITE_BG = 107
    # resets
    RESET = 0
    NO_BOLD = 21
    NO_BOLD_FEINT = 22
    NO_ITALIC_BLACKLETTER = 23
    NO_UNDERLINE = 24
    NO_BLINK = 25
    NO_INVERT = 27
    NO_CONCEAL = 28
    NO_CROSSED = 29
    NO_COLOUR = 39
    NO_BACKGROUND = 49
    NO_PROPORTIONAL_SPACING = 50
    NO_FRAMED_ENCIRCLED = 54
    NO_OVERLINE = 55
    DEFAULT_UNDERLINE_COLOUR = 59
    NO_SUPERSCRIPT_SUBSCRIPT = 75
    # styles
    BOLD = 1
    DIM = 2
    ITALIC = 3
    UNDERLINE = 4
    BLINK = 5
    RAPID_BLINK = 6
    INVERT = 7
    CONCEAL = 8
    CROSSED = 9
    PRIMARY_FONT = 10
    ALT_FONT_1 = 11
    ALT_FONT_2 = 12
    ALT_FONT_3 = 13
    ALT_FONT_4 = 14
    ALT_FONT_5 = 15
    ALT_FONT_6 = 16
    ALT_FONT_7 = 17
    ALT_FONT_8 = 18
    ALT_FONT_9 = 19
    GOTHIC = 20
    PROPORTIONAL_SPACING = 26
    FRAMED = 51
    ENCIRCLED = 52
    OVERLINE = 53
    RIGHT_LINE = 60
    RIGHT_DOUBLE_LINE = 61
    LEFT_LINE = 62
    LEFT_DOUBLE_LINE = 63
    SUPERSCRIPT = 73
    SUBSCRIPT = 74

    @staticmethod
    def reset():
        print(PrintStyles.RESET._prefix(), end="")

    def __init__(self, value):
        self._value = value
        super().__init__(value)
        self._chain = [value]


def Proxy(target, handlers):
    class _ProxyHandler:
        def __init__(self):
            pass

        def __getattr__(self, name: str) -> _Any:
            if "get" in handlers:
                return handlers["get"](target, name)
            elif name in target:
                return target[name]
            return None

        def __setattr__(self, name: str, value: _Any) -> None:
            if "set" in handlers:
                handlers["set"](target, name, value)
            elif name in target:
                target[name] = value
            return None

        def __call__(self, *args, **kwargs):
            if "apply" in handlers:
                return handlers["get"](target, *args, **kwargs)
            elif callable(target):
                return target()
            return None

    return _ProxyHandler()
