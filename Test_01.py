import random
import data_name
import json

# Генерация имени для того, кто делает code-review
def selection(name, list_name, reviewed_list, lust_gen_pair):
    result_name = random.choice(list_name)
    # Пока итоговое имя == своему or итоговое имя уже занято or итоговое имя у нас уже было в прошлой генерации
    while result_name == name or result_name in reviewed_list or result_name in lust_gen_pair[name]:
        result_name = random.choice(list_name)
    reviewed_list.append(result_name)
    return result_name, reviewed_list

# Выбор человека с кем можно обменяться
def sel(name, can_review_list, d, lust_gen_pair):
    result_name = random.choice(can_review_list)
    # Пока итоговое имя == своему or итоговому имени мы делаем code-review or у итогового есть имя, которое было у нас в прошлой генерации
    while result_name == name or result_name in d[name] or check(lust_gen_pair[name], d[result_name], True):
        result_name = random.choice(can_review_list)
    return result_name

# Обновление базы имён
def update_name(dict_name):
    list_name = []
    can_review_list = []
    my_file = open('name.json', "w")
    json.dump(dict_name, my_file,indent=2)
    my_file.close()
    for i in list(dict_name.keys()):
        if dict_name[i]["status"] == 1:
            list_name.append(i)
            if dict_name[i]["review"] == 1:
                can_review_list.append(i)
    return list_name, can_review_list

# Обновление предыдущей генерации
def update_lust_gen_pair(d):
    my_file = open('lust_gen_pair.json', "w")
    json.dump(d, my_file,indent=2)
    my_file.close()
    return d

# Проверка на наличие одинакового элемента
def check(list_1, list_2, k):
    for i in list_1:
        if i in list_2 and k == True:
            return True
        elif not(i in list_2) and k == False:
            return i

def help_for_user():
    print("Команды:")
    print("!help, !список, !рандом")
    print("!добавить(name)(status)(review), если не указать то 1 1", "      Пример: !добавить Данил 1 0")
    print("!удалить(name)", "                                               Пример: !удалить Данил")
    print("!изменить(name)(status,review)(знач)", "                         Пример: !изменить Данил status 0")

my_file = open('name.json', "r")
dict_name = json.load(my_file)
list_name, can_review_list = update_name(dict_name)
my_file = open('lust_gen_pair.json', "r")
lust_gen_pair = json.load(my_file)
reviewed_list = []

help_for_user()

while True:
    chat = input().split(' ')
    if chat[0] == "!рандом":
        d = {}                                                                  # Словарь кто делает code-review → кому
        for i in can_review_list:                                               # Ключ = имя, Значение = кортеж { "str":() }
            d[i] = tuple()
        reviewed_list = []
        r = 0                                                                   # Переменная для перебора списка can_review_list

        while len(list_name) != len(reviewed_list):
            i = can_review_list[r]
            # Если имя последнее и (имя == нашему или имя было у последнего в предыдущей генерации)
            if len(list_name) - len(reviewed_list) == 1 and ( not(i in reviewed_list) or check(list_name, reviewed_list, False) in lust_gen_pair[i]):
                p = sel(i, can_review_list, d, lust_gen_pair)
                d[i] += tuple(map(str, i.split()))
                d[i], d[p] = d[p], d[i]
                reviewed_list.append(i)
            else:
                b, reviewed_list = selection(i, list_name, reviewed_list, lust_gen_pair)
                d[i] += tuple(map(str, b.split()))

            r+=1
            if len(can_review_list) == r:                                       # Обнуление, когда дошли до конца списка
                r = 0

        lust_gen_pair = update_lust_gen_pair(d)
        for a, b in d.items():
            print(a, "→", b)

    elif chat[0] == "!добавить":
        if chat[1] in list_name:
            print("Уже добавлен")
        else:
            if len(chat) >= 3:
                status = int(chat[2])
                review = int(chat[3])
            else:
                status = 1
                review = 1
            dict_name[chat[1]] = {"status" : status, "review" : review}
            lust_gen_pair[chat[1]] = tuple()
            lust_gen_pair = update_lust_gen_pair(lust_gen_pair)
            list_name, can_review_list = update_name(dict_name)
            for a, b in dict_name.items():
                print(a, "→", b)
    elif chat[0] == "!удалить":
        if chat[1] in list_name:
            del dict_name[chat[1]]
            del lust_gen_pair[chat[1]]
            lust_gen_pair = update_lust_gen_pair(lust_gen_pair)
            list_name, can_review_list = update_name(dict_name)
            for a, b in dict_name.items():
                print(a, "→", b)
        else:
            print("Не правильно набрано имя")
    elif chat[0] == "!изменить":
        if chat[2] == "review":
            if int(chat[3]) == 1:
                lust_gen_pair[chat[1]] = tuple()
            elif int(chat[3]) == 0:
                del lust_gen_pair[chat[1]]
            lust_gen_pair = update_lust_gen_pair(lust_gen_pair)
        dict_name[chat[1]][chat[2]] = int(chat[3])
        list_name, can_review_list = update_name(dict_name)
        for a, b in dict_name.items():
            print(a, "→", b)
    elif chat[0] == "!список":
        print("list_name =", list_name)
        print("can_review_list =", can_review_list)
        for a, b in dict_name.items():
            print(a, "→", b)
    elif chat[0] == "!help":
        help_for_user()
    else:
        print("Неправильно")
