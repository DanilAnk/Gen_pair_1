import random
import data_name

def selection(name, list_name, busy_list):
    result_name = random.choice(list_name)
    while result_name == name or result_name in busy_list:
        result_name = random.choice(list_name)
    busy_list.append(result_name)
    return result_name, busy_list

list_name = []
busy_list = []                                                   # Список тех, у кого уже смотрят код
can_review_list = []
d = {}                                                           # Словарь кто смотрит - у кого смотрит


print("Команды:")
print("!добавить(name), !удалить(name), !список, !рандом")

for i in list(data_name.dict_name.keys()):
    if data_name.dict_name[i]["status"] == 1:
        list_name.append(i)
    if data_name.dict_name[i]["review"] == 1:
        can_review_list.append(i)

while True:
    chat = input().split(' ')                                     # Что пишет пользователь в строку

    if chat[0] == "!рандом":
        for i in can_review_list:
            if not(i in busy_list) and len(list_name) - len(busy_list) == 1:
                p = random.randint(0, len(can_review_list) - 2)
                d[i], d[str(list(d)[p])] = d[list(d)[p]], i
                busy_list.append(i)
            else:
                d[i], busy_list = selection(i, list_name, busy_list)

        while len(busy_list) != len(list_name):
            i = random.choice(can_review_list)
            if not(i in busy_list) and len(list_name) - len(busy_list) == 1:
                p = random.randint(0, len(can_review_list) - 2)
                d[i], d[str(list(d)[p])] = d[list(d)[p]], i
                busy_list.append(i)
            else:
                b, busy_list = selection(i, list_name, busy_list)
                d[i] = (d[i], b)

        for a, b in d.items():
            print(a, "→", b)
        busy_list = []
        d = {}

    elif chat[0] == "!добавить":
        list_name.append(chat[1])
        print(list_name)

    elif chat[0] == "!удалить":
        list_name.remove(chat[1])
        print(list_name)

    elif chat[0] == "!список":
        print(list_name)

    else:
        print("Неправильно")
