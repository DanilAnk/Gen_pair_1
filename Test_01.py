import random
import json

# Генерация имени для того, кто делает code-review
def selection(name: str, list_name: list, reviewed_list: list, last_gen_pair: dict) -> tuple:
    result_name = random.choice(list_name)
    # Пока итоговое имя == своему or итоговое имя уже занято or итоговое имя у нас уже было в прошлой генерации
    while result_name == name or result_name in reviewed_list or result_name in last_gen_pair[name]:
        result_name = random.choice(list_name)
    reviewed_list.append(result_name)
    return result_name, reviewed_list

# Выбор человека с кем можно обменяться
def sel(name: str, can_review_list: list, present_gen: dict, last_gen_pair: dict) -> str:
    result_name = random.choice(can_review_list)
    # Пока итоговое имя == своему or итоговому имени мы делаем code-review or у итогового есть имя, которое было у нас в прошлой генерации
    while result_name == name or result_name in present_gen[name] or check(last_gen_pair[name], present_gen[result_name], True):
        result_name = random.choice(can_review_list)
    return result_name

# Обновление базы имён
def update_name(dict_name: dict) -> tuple:
    list_name = []
    can_review_list = []
    file_data_name = open('name.json', "w")
    json.dump(dict_name, file_data_name,indent=2)
    file_data_name.close()
    for i in list(dict_name.keys()):
        if dict_name[i]["status"] == 1:
            list_name.append(i)
            if dict_name[i]["review"] == 1:
                can_review_list.append(i)
    return list_name, can_review_list

# Обновление предыдущей генерации
def update_last_gen_pair(last_gen_pair: dict):
    file_last_gen = open('last_gen_pair.json', "w")
    json.dump(last_gen_pair, file_last_gen,indent=2)
    file_last_gen.close()

# Проверка на наличие одинакового элемента в двух разных списках, с выводом значения, зависимого от переменной k
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

COMMAND_CHANGE = "!изменить"
COMMAND_APPEND = "!добавить"
COMMAND_DELETE = "!удалить"
COMMAND_RANDOM = "!рандом"
COMMAND_CONCLUSION = "список"                                                   # CONCLUSION - Вывод

file_data_name = open('name.json', "r")
dict_name = json.load(file_data_name)
list_name, can_review_list = update_name(dict_name)
file_data_name.close()

file_last_gen = open('last_gen_pair.json', "r")
last_gen_pair = json.load(file_last_gen)
file_last_gen.close()

help_for_user()

while True:
    chat = input().split(' ')
    command = chat[0]
    try:
        user_selected_name = chat[1]
    except:
        user_selected_name = None

    if command == COMMAND_RANDOM:
        present_gen = {}                                                        # Словарь кто делает code-review → кому
        for i in can_review_list:                                               # Ключ = имя, Значение = кортеж { "str":() }
            present_gen[i] = tuple()
        reviewed_list = []
        r = 0                                                                   # Переменная для перебора списка can_review_list

        while len(list_name) != len(reviewed_list):
            i = can_review_list[r]
            # Если имя последнее и (имя == нашему или имя было у последнего в предыдущей генерации)
            if len(list_name) - len(reviewed_list) == 1 and ( not(i in reviewed_list) or check(list_name, reviewed_list, False) in last_gen_pair[i]):
                p = sel(i, can_review_list, present_gen, last_gen_pair)
                present_gen[i] += tuple(map(str, i.split()))
                present_gen[i], present_gen[p] = present_gen[p], present_gen[i]
                reviewed_list.append(i)
            else:
                b, reviewed_list = selection(i, list_name, reviewed_list, last_gen_pair)
                present_gen[i] += tuple(map(str, b.split()))

            r+=1
            if len(can_review_list) == r:                                       # Обнуление, когда дошли до конца списка
                r = 0

        update_last_gen_pair(present_gen)
        for a, b in present_gen.items():
            print(a, "→", b)

    elif command == COMMAND_APPEND:
        if user_selected_name in list_name:
            print("Уже добавлен")
        else:
            if len(chat) >= 3:
                status = int(chat[2])
                review = int(chat[3])
            else:
                status = 1
                review = 1
            dict_name[user_selected_name] = {"status" : status, "review" : review}
            last_gen_pair[user_selected_name] = tuple()
            update_last_gen_pair(last_gen_pair)
            list_name, can_review_list = update_name(dict_name)
            for a, b in dict_name.items():
                print(a, "→", b)
    elif command == COMMAND_DELETE:
        if user_selected_name in list_name:
            del dict_name[user_selected_name]
            del last_gen_pair[user_selected_name]
            update_last_gen_pair(last_gen_pair)
            list_name, can_review_list = update_name(dict_name)
            for a, b in dict_name.items():
                print(a, "→", b)
        else:
            print("Не правильно набрано имя")
    elif command == COMMAND_CHANGE:
        if chat[2] == "review":
            if int(chat[3]) == 1:
                last_gen_pair[user_selected_name] = tuple()
            elif int(chat[3]) == 0:
                try:
                    del last_gen_pair[user_selected_name]
                except:
                    print("Уже равно 0")
            update_last_gen_pair(last_gen_pair)
        dict_name[user_selected_name][chat[2]] = int(chat[3])
        list_name, can_review_list = update_name(dict_name)
        for a, b in dict_name.items():
            print(a, "→", b)
    elif command == COMMAND_CONCLUSION:
        print("list_name =", list_name)
        print("can_review_list =", can_review_list)
        for a, b in dict_name.items():
            print(a, "→", b)
    elif command == "!help":
        help_for_user()
    else:
        print("Неправильно, для помощи введите !help")
