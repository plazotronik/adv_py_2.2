#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re
from pprint import pprint
# читаем адресную книгу в формате CSV в список contacts_list
import csv
with open('phonebook_raw.csv') as file:
    rows = csv.reader(file, delimiter=',')
    contacts_list = list(rows)
# pprint(contacts_list)


# TODO 1: выполните пункты 1-3 ДЗ
# ваш код
header = contacts_list.pop(0)
list_dicts = []

# формирование словарей из каждой строки исходного файла (сохранение связи данных со столбцами)
for line in contacts_list:
    dict = {}
    line = ','.join(line)
    fio = re.search(r'^(\w+)(\s|\W)(\w+)(\s|\W)(\w*)(,{1,3})', line)
    org = re.search(r'^\w+\W\w+\W\w+\W+(\w+)', line)
    pos = re.search(r'^\w+\W\w+\W\w+\W+(\w+)\W+([а-яa-z]+)([^,]+)', line, re.I)
    tel = re.search(r'(\+7|8)+(\s*)(\(*)(\d{3})(\)*)(\W|\s)*(\d{3})(\W|\s)*(\d{2})(\W|\s)*(\d{2})(\s*)(\(*)'
                    r'(\w*\.*)(\s*)(\d{4})*(\)*)', line)
    mail = re.search(r'([^,]+)(@)([a-z]+)(\W?)([a-z]+)', line)
    organization = org.expand(r'\1') if org else ''
    position = pos.expand(r'\2\3') if pos else ''
    if tel:
        phone = '+7({}){}-{}-{}'.format(tel.expand(r'\4'), tel.expand(r'\7'), tel.expand(r'\9'),
                                        tel.expand(r'\11\12\14\16'))
    else:
        phone = ''
    email_addr = mail.expand(r'\1\2\3\4\5') if mail else ''
    dict[header[0]] = fio.expand(r'\1')
    dict[header[1]] = fio.expand(r'\3')
    dict[header[2]] = fio.expand(r'\5')
    dict[header[3]] = organization
    dict[header[4]] = position
    dict[header[5]] = phone
    dict[header[6]] = email_addr
    list_dicts.append(dict)

# объединение всей информации об одном и том же человеке, при условии,
# что фамилия это идентификатор одного и того же человека
for dict in list_dicts:
    for dict_mirror in list_dicts:
        if dict[header[0]] == dict_mirror[header[0]]:
            for key in dict:
                if dict[key] == dict_mirror[key]:
                    continue
                else:
                    dict[key] += dict_mirror[key]

# удаление всех возможных дублей
for dict in list_dicts:
    count = list_dicts.count(dict)
    if count > 1:
        for _ in range(count - 1):
            list_dicts.remove(dict)


# TODO 2: сохраните получившиеся данные в другой файл
# код для записи файла в формате CSV
with open('phonebook.csv', 'w') as file:
    file.write(','.join(header) + '\n')
    datawriter = csv.writer(file, delimiter=',')
    # Вместо contacts_list подставьте свой список
    datawriter.writerows([[dict[column] for column in header] for dict in list_dicts])
