import random
import data_name
import json

# Генерация имени для того, кто делает code-review
def selection(name, list_name, reviewed_list):
    result_name = random.choice(list_name)
    while result_name == name or result_name in reviewed_list:
        result_name = random.choice(list_name)
    reviewed_list.append(result_name)
    return result_name, reviewed_list

# Выбор человека с кем можно обменяться
def sel(name, can_review_list, d, lust_gen_pair):
    result_name = random.choice(can_review_list)
    while result_name == name or result_name in d[name]:
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

def update_lust_gen_pair(d):
    my_file = open('lust_gen_pair.json', "w")
    json.dump(d, my_file,indent=2)
    my_file.close()
    return d

my_file = open('name.json', "r")
dict_name = json.load(my_file)
list_name, can_review_list = update_name(dict_name)
reviewed_list = []

print("Команды:")
print("!добавить(name)(status)(review), !удалить(name), !список, !рандом")
print("Пример: ", "!добавить Данил 1 0")

while True:
    chat = input().split(' ')
    if chat[0] == "!рандом":
        d = {}                                                                  # Словарь кто делает code-review → кому
        for i in can_review_list:                                               # Ключ = имя, Значение = кортеж
            d[i] = tuple()
        reviewed_list = []
        r = 0                                                                   # Переменная для перебора списка can_review_list

        while len(list_name) != len(reviewed_list):
            i = can_review_list[r]
            if len(list_name) - len(reviewed_list) == 1 and  not(i in reviewed_list):
                p = sel(i, can_review_list, d)
                d[i] += tuple(map(str, i.split()))
                d[i], d[p] = d[p], d[i]
                reviewed_list.append(i)
            else:
                b, reviewed_list = selection(i, list_name, reviewed_list)
                d[i] += tuple(map(str, b.split()))

            r+=1
            if len(can_review_list) == r:                                       # Обнуление, когда дошли до конца списка
                r = 0

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
            list_name, can_review_list = update_name(dict_name)
            for a, b in dict_name.items():
                print(a, "→", b)
    elif chat[0] == "!удалить":
        if chat[1] in list_name:
            del dict_name[chat[1]]
            list_name, can_review_list = update_name(dict_name)
            for a, b in dict_name.items():
                print(a, "→", b)
        else:
            print("Не правильно набрано имя")
    elif chat[0] == "!изменить":
        dict_name[chat[1]][chat[2]] = int(chat[3])
        list_name, can_review_list = update_name(dict_name)
        for a, b in dict_name.items():
            print(a, "→", b)
    elif chat[0] == "!список":
        print("list_name =", list_name)
        print("can_review_list =", can_review_list)
        for a, b in dict_name.items():
            print(a, "→", b)
    else:
        print("Неправильно")
