from func import *

COMMAND_CHANGE = "!изменить"
COMMAND_APPEND = "!добавить"
COMMAND_DELETE = "!удалить"
COMMAND_RANDOM = "!рандом"
COMMAND_CONCLUSION = "!список"                                                   # CONCLUSION - Вывод

file_data_name = open('name.json', "r")
from_data_dict_name = json.load(file_data_name)
list_name, can_review_list = update_name(from_data_dict_name)
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
                p = select_for_change(i, can_review_list, present_gen, last_gen_pair)
                present_gen[i] += tuple(map(str, i.split()))
                present_gen[i], present_gen[p] = present_gen[p], present_gen[i]
                reviewed_list.append(i)
            else:
                b, reviewed_list = select(i, list_name, reviewed_list, last_gen_pair)
                present_gen[i] += tuple(map(str, b.split()))

            r+=1
            if len(can_review_list) == r:                                       # Обнуление, когда дошли до конца списка
                r = 0

        update_last_gen_pair(present_gen)
        for a, b in present_gen.items():
            if len(b) == 1:
                print(a, "→", b[0])
            else:
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
            from_data_dict_name[user_selected_name] = {"status" : status, "review" : review}
            list_name, can_review_list = update_name(from_data_dict_name)
            last_gen_pair[user_selected_name] = tuple()
            update_last_gen_pair(last_gen_pair)
            for a, b in from_data_dict_name.items():
                print(a, "→", b)
    elif command == COMMAND_DELETE:
        if user_selected_name in list_name:
            del from_data_dict_name[user_selected_name]
            del last_gen_pair[user_selected_name]
            update_last_gen_pair(last_gen_pair)
            list_name, can_review_list = update_name(from_data_dict_name)
            for a, b in from_data_dict_name.items():
                print(a, "→", b)
        else:
            print("Не правильно набрано имя")
    elif command == COMMAND_CHANGE:
        # Не знаю как назвать переменные chat[2] и chat[3]
        if chat[2] == "review":
            if int(chat[3]) == 1:
                last_gen_pair[user_selected_name] = tuple()
            elif int(chat[3]) == 0:
                try:
                    del last_gen_pair[user_selected_name]
                except:
                    print("Уже равно 0")
            update_last_gen_pair(last_gen_pair)
        from_data_dict_name[user_selected_name][chat[2]] = int(chat[3])
        list_name, can_review_list = update_name(from_data_dict_name)
        for a, b in from_data_dict_name.items():
            print(a, "→", b)
    elif command == COMMAND_CONCLUSION:
        print("list_name =", list_name)
        print("can_review_list =", can_review_list)
        for a, b in from_data_dict_name.items():
            print(a, "→", b)
    elif command == "!help":
        help_for_user()
    else:
        print("Неправильно, для помощи введите !help")
