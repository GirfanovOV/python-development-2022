import sys
from locale import setlocale, LC_ALL
from .figdate import date


if __name__ == '__main__' :
    setlocale(LC_ALL, ('ru_RU', 'UTF-8'))
    print(date(*sys.argv[1:3]))