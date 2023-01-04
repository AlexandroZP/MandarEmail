import re


def in_list_check(check, list):
    checked = False
    for element in list:
        if element == check:
            checked = True
            break
    return checked


def double_list_check(list1, list2):
    checked = False
    element = ''
    for f_check in list1:
        for s_check in list2:
            if f_check == s_check:
                list2.remove(s_check)
                break
    return (list2, checked, element)


def valid_email(email):
    padrao = re.search(r'[a-zA-Z0-9_-]+@[a-zA-Z0-9]+\.[a-zA-Z]{1,3}$', email)
    return padrao