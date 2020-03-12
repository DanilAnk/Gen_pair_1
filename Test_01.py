import random

def selection(name, list_name, busy_list):
    result_name = random.choice(list_name)
    while result_name == name or result_name in busy_list:
        result_name = random.choice(list_name)
    busy_list.append(result_name)
    return result_name, busy_list


list_name = ["Женя", "Никита", "Ваня", "Рома", "Настя", "Миша"]  # Список всех программистов
busy_list = []                                                   # Список тех, у кого уже смотрят код
d = {}                                                           # Словарь кто смотрит - у кого смотрит
print("Команды:")
print("!добавить(name), !удалить(name), !рандом")

while True:
    chat = input().split(' ')                                     # Что пишет пользователь в строку

    if chat[0] == "!рандом":
        for i in list_name:
            d[i], busy_list = selection(i, list_name, busy_list)
        for a, b in d.items():
            print(a, "→", b)

    if chat[0] == "!добавить":
        list_name.append(chat[1])

    if chat[0] == "!удалить":
        list_name.remove(chat[1])
