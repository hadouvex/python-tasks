import logging
import argparse
import os
import sys
import csv
import pandas as pd


from time import sleep
from random import randint, choice


# Данный скрипт использует библиотеку 'pandas' и ее зависимости,
# не входящие в состав стандартной библиотеки python.
# Необходимо создать виртуальное окружение (python3 -m venv *имя*),
# активировать его (source venv/bin/activate), установить зависимости
# из файла "requirements.txt" (pip install -r requirements.txt)
# или же установить зависимости глобально.

# Использование:
# python3 task3.py *имя файла* *начальная дата* *конечная дата*

# Пример использования:
# python3 task3.py log.log 2020-08-20T02:19:01 2020-08-20T02:19:10
# Вывод программы:
"""
За указанный период было совершено попыток налить воду: 3007
Из них процент успешных: 99.97%
Процент неудачных: 0.03%

За указанный период было совершено попыток вычерпать воду: 2907
Из них процент успешных: 99.93%
Процент неудачных: 0.07%

На начало указанного периода в бочке было 15 литров воды
На конец указанного периода в бочке было 2713 литров воды

За указанный период объем воды изменился на 2698 литров
На конец указанного периода не хватало 287 литров воды, чтобы заполнить бочку
"""
# Также программа генерирует файл "output.csv"

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s — [%(user)s] — %(message)s — (%(is_successful)s) ',
    datefmt='%Y-%m-%dT%H:%M:%S.%SZ',
    filename='log.log'
)


def generate_username():
    return 'username' + str(randint(0, 100))


def fill_barrel(barrel_vol, barrel_vol_current):
    generate_log_initial(barrel_vol, barrel_vol_current)
    while barrel_vol > barrel_vol_current and barrel_vol_current >= 0:
        sleep(0.001)
        if choice(('top_up', 'scoop')) == 'top_up':
            to_top_up = randint(0, 50)
            if barrel_vol_current + to_top_up <= barrel_vol:    
                barrel_vol_current += to_top_up
                generate_log_main(to_top_up, 'top up', 'успех', barrel_vol_current)
            else:
                generate_log_main(to_top_up, 'top up', 'фейл', barrel_vol_current)
        else:
            to_scoop = randint(0, 50)
            if barrel_vol_current - to_scoop >= 0:
                barrel_vol_current -= to_scoop
                generate_log_main(to_scoop, 'scoop', 'успех', barrel_vol_current)
            else:
                generate_log_main(to_scoop, 'scoop', 'фейл', barrel_vol_current)


def generate_log_initial(barrel_vol, barrel_vol_current):
    with open("log.log", "a") as f:
        f.write('META DATA:\n')
        f.write(f'{barrel_vol} (объем бочки)\n')
        f.write(f'{barrel_vol_current} (текущий объем воды в бочке)\n')


def generate_log_main(value, action_type, status, vol):
    extras = {'user': generate_username(), 'is_successful': status}
    logging.info(f'wanna {action_type} {value}l — {vol}', extra=extras)


def analyse_data(log_file, datetime_begin=None, datetime_end=None):
    df = pd.read_csv(
        log_file,
        skiprows=3,
        names=('date/time', 'username', 'action/amount', 'result', 'status'),
        sep='—',
        engine='python'
    )
    df = df.set_index(['date/time'])
    df_located = df.loc[datetime_begin : datetime_end]
    df_located = df_located.reset_index()
    df_located.columns = df_located.columns.str.replace(' ', '')

    volume_begin = df_located.iloc[0]['result']
    volume_end = df_located.iloc[-1]['result']

    volume_change = volume_end - volume_begin
    left_to_fill = df.iloc[-1]['result'] - volume_end

    # attempts_failed_total = df_located.loc[df_located['status'].str.strip() == '(фейл)']
    attempts_succeed_total = df_located.loc[df_located['status'].str.strip() == '(успех)']

    scoop_attempts_total = df_located.loc[df_located['action/amount'].str.contains('scoop')]
    top_up_attempts_total = df_located.loc[df_located['action/amount'].str.contains('top')]

    # scoop_attempts_failed_total = attempts_failed_total.loc[attempts_failed_total['action/amount'].str.contains('scoop')]
    # top_up_attempts_failed_total = attempts_failed_total.loc[attempts_failed_total['action/amount'].str.contains('top')]

    scoop_attempts_succeed_total = attempts_succeed_total.loc[attempts_succeed_total['action/amount'].str.contains('scoop')]
    top_up_attempts_succeed_total = attempts_succeed_total.loc[attempts_succeed_total['action/amount'].str.contains('top')]

    scoop_succeed_count = len(scoop_attempts_succeed_total.index)
    # scoop_failed_count = len(scoop_attempts_failed_total.index)
    top_up_succeed_count = len(top_up_attempts_succeed_total.index)
    # top_up_failed_count = len(top_up_attempts_failed_total.index)
    
    scoop_attempts_total_count = len(scoop_attempts_total.index)
    top_up_attempts_total_count = len(top_up_attempts_total.index)

    top_up_succeed_percentage = round(top_up_succeed_count / top_up_attempts_total_count * 100, 2)
    top_up_failed_percentage = round(100 - top_up_succeed_percentage, 2)

    scoop_succeed_percentage = round(scoop_succeed_count / scoop_attempts_total_count * 100, 2)
    scoop_failed_percentage = round(100 - scoop_succeed_percentage, 2)

    return {
        'volume_begin': volume_begin,
        'volume_end': volume_end,
        'volume_change': volume_change,
        'left_to_fill': left_to_fill,
        'scoop_attempts_total_count': scoop_attempts_total_count,
        'top_up_attempts_total_count': top_up_attempts_total_count,
        'scoop_succeed_percentage': scoop_succeed_percentage,
        'top_up_succeed_percentage': top_up_succeed_percentage,
        'scoop_failed_percentage': scoop_failed_percentage,
        'top_up_failed_percantage': top_up_failed_percentage
    }


def parse_arguments():
    parser = argparse.ArgumentParser(description="Analyse log file content")
    parser.add_argument('filename', type=str, help='Log file name')
    parser.add_argument('datetime_begin', type=str, help='Period start date')
    parser.add_argument('datetime_end', type=str, help='Period end date')
    args = parser.parse_args()

    if os.path.isfile('./' + args.filename):
        return args
    else:
        parser.print_help()
        sys.exit(1)
        

def main():
    args = parse_arguments()
    da = analyse_data(args.filename, args.datetime_begin, args.datetime_end)
    
    print('\nЗа указанный период было совершено попыток налить воду: ' + str(da['top_up_attempts_total_count']))
    print('Из них процент успешных: ' + str(da['top_up_succeed_percentage']) + '%')
    print('Процент неудачных: ' + str(da['top_up_failed_percantage']) + '%')
    print('\nЗа указанный период было совершено попыток вычерпать воду: ' + str(da['scoop_attempts_total_count']))
    print('Из них процент успешных: ' + str(da['scoop_succeed_percentage']) + '%')
    print('Процент неудачных: ' + str(da['scoop_failed_percentage']) + '%')
    print('\nНа начало указанного периода в бочке было ' + str(da['volume_begin']) + ' литров воды.')
    print('На конец указанного периода в бочке было ' + str(da['volume_end']) + ' литров воды.')
    print('\nЗа указанный период объем воды изменился на ' + str(da['volume_change']) + ' литров.')
    print('На конец указанного периода не хватало ' + str(da['left_to_fill']) + ' литров воды, чтобы заполнить бочку.')

    with open('output.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([
            'top up',              #1
            'top up succeed (%)',  #2
            'top up failed (%)',   #3
            'scoop',               #4
            'scoop succeed (%)',   #5
            'scoop failed (%)',    #6
            'volume at start',     #7
            'volume at end',       #8
            'volume change',       #9
            'volume to fill'       #10
        ])
        writer.writerow([
            da['top_up_attempts_total_count'], #1
            da['top_up_succeed_percentage'],   #2
            da['top_up_failed_percantage'],    #3
            da['scoop_attempts_total_count'],  #4
            da['scoop_succeed_percentage'],    #5
            da['scoop_failed_percentage'],     #6
            da['volume_begin'],                #7
            da['volume_end'],                  #8
            da['volume_change'],               #9
            da['left_to_fill']                 #10
        ])
main()