import random
import json

# Выбор имени для того, кто делает code-review
def select(name: str, list_name: list, reviewed_list: list, last_gen_pair: dict) -> tuple:
    result_name = random.choice(list_name)
    # Пока итоговое имя == своему or итоговое имя уже занято or итоговое имя у нас уже было в прошлой генерации
    while result_name == name or result_name in reviewed_list or result_name in last_gen_pair[name]:
        result_name = random.choice(list_name)
    reviewed_list.append(result_name)
    return result_name, reviewed_list

# Выбор человека с кем можно обменяться
def select_for_change(name: str, can_review_list: list, present_gen: dict, last_gen_pair: dict) -> str:
    result_name = random.choice(can_review_list)
    # Пока итоговое имя == своему or итоговому имени мы делаем code-review or у итогового есть имя, которое было у нас в прошлой генерации
    while result_name == name or result_name in present_gen[name] or check(last_gen_pair[name], present_gen[result_name], True):
        result_name = random.choice(can_review_list)
    return result_name

# Обновление базы имён
def update_name(from_data_dict_name: dict) -> tuple:
    list_name = []
    can_review_list = []
    file_data_name = open('name.json', "w")
    json.dump(from_data_dict_name, file_data_name,indent=2, ensure_ascii=False)
    file_data_name.close()
    for i in list(from_data_dict_name.keys()):
        if from_data_dict_name[i]["status"] == 1:
            list_name.append(i)
            if from_data_dict_name[i]["review"] == 1:
                can_review_list.append(i)
    return list_name, can_review_list

# Обновление предыдущей генерации
def update_last_gen_pair(last_gen_pair: dict):
    file_last_gen = open('last_gen_pair.json', "w")
    json.dump(last_gen_pair, file_last_gen,indent=2, ensure_ascii=False)
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
