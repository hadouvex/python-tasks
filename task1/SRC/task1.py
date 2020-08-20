import string
import argparse

# Максимально возможное основание системы счисления - 36.

# При использовании бОльших значений при формировании числа
# будут использоваться небуквенные символы.

# Поскольку Python не позволяет перегрузку функций/методов,
# воспользуемся небольшим воркэраундом.
# для этого используем аргументы со значениями по умолчанию.
# В зависимости от переданных из командной строки аргументов
# и их значений, будет меняться поведение функции i_to_base,
# которая теперь способна как выполнять перевод из десятичной
# системы счисления в любую другую, так и выполнять перевод
# из системы x в систему y, посредством использования служебных
# функций decimal_to_any() [из десятичной в любую] и
# any_to_decimal() [из любой в десятичную].

# Использование:

# Запуск перевода из десятичной системы в другую (основное задание):
# python3 task1.py *число* --base *основание системы*
# Ввод осуществляется без звездочек, основание системы,
# Согласно заданию, записывается в виде последовательности
# Элементов, составляющих систему, в порядке их возрастания.
# Например: python3 task1.py 1000 --base 01 -> 1111101000
# Данный пример переводит 1000@10 в 1111101000@2

# Запуск перевода из любой системы в любую (дополнительное задание):
# python3 task1.py *число* --base_src *система счисления "из"* --base_dst *система счисления "в"*
# Например: python3 task1.py 10111101 --base_src 01 --base_dst 01234567 -> 275
# Данный пример переводит 10111101@2 в 275@8

# Разделим функционал на две разные функции, чтобы избежать
# Повторения кода.

def i_to_base(nb, base=None, base_src=None, base_dst=None):
    if base != None:
        return decimal_to_any(nb, base)
    elif base_src != None and base_dst != None:
        interm_res = any_to_decimal(nb, base_src)
        return decimal_to_any(interm_res, base_dst)


def decimal_to_any(nb, base):
    result = ""
    # Из строки, включающей элементы системы счисления, находим ее основание
    base_digit = len(base)
    nb = int(nb)
    while nb > 0:
        digit = int(nb % base_digit)
        # Проверяем, возможно ли записать значение арабскими цифрами
        if digit < 10:
            result += str(digit)
        # Если нет, то находим для него буквенное обозначение, начиная с латинской 'A'
        else:
            result += chr(ord('A') + digit - 10)
        nb //= base_digit
    # Переворачиваем результат
    result = result[::-1]
    return result


def any_to_decimal(nb, base):
    nb = nb[::-1]
    result = 0
    base_digit = len(base)
    for k in range(len(nb)):
        digit = nb[k]
        if digit.isdigit():
            digit = int(digit)
        else:
            digit = ord(digit.upper()) - ord('A') + 10
        result += digit * (base_digit ** k)
    return result


def main():
    # Создаем парсер аргументов, вызывающий usage при неверном вводе
    # аргументов или при непрохождении проверки

    # 'nb' - обязательный аргумент, остальные - опциональные, в
    # зависимости от их значений меняется поведение управляющей функции
    # i_to_base()

    parser = argparse.ArgumentParser(description="Convert decimal -> any")
    parser.add_argument('nb', type=str, help="number to convert")
    parser.add_argument('--base', type=str, help="base to convert to")
    parser.add_argument('--base_src', type=str, help="base src")
    parser.add_argument('--base_dst', type=str, help="base dst")
    args = parser.parse_args()
    allowed_symbols = set(string.ascii_lowercase + string.digits)

    # Проверяем на наличие несовместимых аргументов и, если все в порядке,
    # проверяем аргументы на валидность. Если аргумениы валидны, вызываем
    # i_to_base() с соответствующими аргументами и печатаем результат.
    # В противном случае выводим usage сообщение.

    if args.base != None and (args.base_src != None or args.base_dst != None):
        parser.print_help()
    else:
        if args.nb and args.base:
            if set(args.nb) <= allowed_symbols and set(args.base) <= allowed_symbols:
                print(i_to_base(args.nb, args.base))
            else:
                parser.print_help()
        elif args.nb and args.base_src and args.base_dst:
            if (set(args.nb) <= allowed_symbols and set(args.base_src) <= allowed_symbols and
                set(args.base_dst) <= allowed_symbols):
                print(i_to_base(args.nb, base_src=args.base_src, base_dst=args.base_dst))
            else:
                parser.print_help()


main()