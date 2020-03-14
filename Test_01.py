import random
import data_name

def selection(name, list_name, busy_list):
    result_name = random.choice(list_name)
    while result_name == name or result_name in busy_list:
        result_name = random.choice(list_name)
    busy_list.append(result_name)
    return result_name, busy_list

def sel(name, can_review_list, d):
    result_name = random.choice(can_review_list)
    while result_name == name or result_name in d[name]:
        result_name = random.choice(can_review_list)
    return result_name

list_name = []
busy_list = []
can_review_list = []
d = {}
r = 0

print("Команды:")
print("!добавить(name), !удалить(name), !список, !рандом")

for i in list(data_name.dict_name.keys()):
    if data_name.dict_name[i]["status"] == 1:
        list_name.append(i)
        if data_name.dict_name[i]["review"] == 1:
            can_review_list.append(i)
for i in can_review_list:
    d[i] = tuple()

while True:
    chat = input().split(' ')
    if chat[0] == "!рандом":
        while len(list_name) != len(busy_list):
            i = can_review_list[r]
            if not(i in busy_list) and len(list_name) - len(busy_list) == 1:
                p = sel(i, can_review_list, d)
                d[i] += tuple(map(str, i.split()))
                d[i], d[p] = d[p], d[i]
            else:
                b, busy_list = selection(i, list_name, busy_list)
                d[i] += tuple(map(str, b.split()))

            r+=1
            if len(can_review_list) == r:
                r = 0

        for a, b in d.items():
            print(a, "→", b)
        busy_list = []
        d = {}
        for i in can_review_list:
            d[i] = tuple()

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
