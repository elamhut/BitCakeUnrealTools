from tkinter import Tk
from tkinter.filedialog import askdirectory


def get_dir():
    Tk().withdraw()
    filename = askdirectory()
    return filename


if __name__ == '__main__':
    print(get_dir())
