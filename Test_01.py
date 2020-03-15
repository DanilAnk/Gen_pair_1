import random
import data_name

# Генерация имени для того, кто делает code-review
def selection(name, list_name, reviewed_list):
    result_name = random.choice(list_name)
    while result_name == name or result_name in reviewed_list:
        result_name = random.choice(list_name)
    reviewed_list.append(result_name)
    return result_name, reviewed_list

# Выбор человека с кем можно обменяться
def sel(name, can_review_list, d):
    result_name = random.choice(can_review_list)
    while result_name == name or result_name in d[name]:
        result_name = random.choice(can_review_list)
    return result_name

list_name = []
reviewed_list = []
can_review_list = []

print("Команды:")
print("!добавить(name), !удалить(name), !список, !рандом")

for i in list(data_name.dict_name.keys()):
    if data_name.dict_name[i]["status"] == 1:
        list_name.append(i)
        if data_name.dict_name[i]["review"] == 1:
            can_review_list.append(i)

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
            if not(i in reviewed_list) and len(list_name) - len(reviewed_list) == 1:
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
            list_name.append(chat[1])
            print(list_name)
    elif chat[0] == "!удалить":
        list_name.remove(chat[1])
        print(list_name)
    elif chat[0] == "!список":
        print(list_name)
    else:
        print("Неправильно")
