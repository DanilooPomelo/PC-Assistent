def get_txt(txt):
    return input(txt)


def get_int(numb):
    while True:
        try:
            return int(input(numb))
        except ValueError:
            return "Введите число!"


def waitfornext():
    get_txt("Enter for next")
    return