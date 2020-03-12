import random
list_name = ["Женя", "Никита", "Ваня", "Рома", "Настя", "Миша"]
kogo_list = []
d = {}
print("Команды:")
print("!добавить(name), !удалить(name), !рандом")
while True:
    chat = input()
    chat_1 = chat.split(' ')
    if chat_1[0] == "!рандом":
        for i in list_name:
            kogo_list.append(i)
            c = list(set(list_name)-set(kogo_list))
            t = random.choice(c)
            d[i] = t
            kogo_list.append(t)
            kogo_list.remove(i)
        print(d)
    if chat_1[0] = "!добавить":
        list_name.append(chat_1[1])
    if chat_1[0] = "!удалить":
        list_name.remove(chat_1[1])
