import argparse

# Использование:
# python task4.py *первая строка* *вторая строка*
# Например: task4.py abcd ***a***b*c**** -> OK
# В большинстве оболочек астериск (*) является
# специальным символом, поэтому его следует экранировать
# обратный слешем (\), например: ab\*c\*d\*

def compare(str_a, str_b):

    str_b = str_b.replace('*', '')

    # Используем однострочный вариант записи if-else, поскольку условие достаточно короткое
    return 'OK' if str_b in str_a else 'KO'

# Создаем парсер аргументов и считываем их из ввода командной строки
parser = argparse.ArgumentParser(description='Check strings')
parser.add_argument('str_a', type=str, help='First string')
parser.add_argument('str_b', type=str, help='Second string, may contain asterisk (*)')
args = parser.parse_args()
print(compare(args.str_a, args.str_b))