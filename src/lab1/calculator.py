def calc(chislo1, chislo2, sign):
    """
    Ввожу калькулятор: создаю переменные chislo1 и chislo2,
    котороые будет вводить пользователь и сам знак операции
    """
    if sign == "+":
        return chislo1 + chislo2
    if sign == "-":
        return chislo1 - chislo2
    if sign == "*":
        return chislo1 * chislo2
    if sign == "/":
        if chislo2 != 0:
            return chislo1 / chislo2
        return "Ошибка! Делить на ноль нельзя!"
    return "Операцию, которую Вы ввели, нет в данном списке. Попробуйте еще!"


def vvod():
    """
    В vvod происходит считывание вводимых данных
    """
    chislo1 = float(input("a = "))
    chislo2 = float(input("b ="))
    sign = input("Введите любую из данных операций (+, -, *, /) :")
    print(calc(chislo1, chislo2, sign))
