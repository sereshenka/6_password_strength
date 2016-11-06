import argparse
import os
import tempfile
import urllib.request
import re


def read_arguments():
    parser = argparse.ArgumentParser('Скрипт оценивает сложность пароля')
    parser.add_argument('--password', help = 'Укажите пароль ', \
                        required = True, nargs = '+')
    url_default = 'https://raw.githubusercontent.com/danielmiessler/SecLists/' \
    'master/Passwords/10_million_password_list_top_500.txt'
    parser.add_argument('--url', help = 'Укажите адрес с blacklist паролей' \
                       , default = url_default)
    parser.add_argument('--blacklist', help = 'Укажите фаил с blacklist')
    if len(parser.parse_args().password) > 1:
        return None, None, None, 1
    password = parser.parse_args().password
    url_blacklist = parser.parse_args().url
    local_blacklist = parser.parse_args().blacklist
    if local_blacklist is not None:
        if os.path.exists(local_blacklist):
            return password, parser, local_blacklist, None
        else:
            return password, parser, get_blacklist(url_blacklist), 2
    else:
        return password, parser, get_blacklist(url_blacklist), None


def get_blacklist(url_blacklist):
    destination = os.path.join(tmpdirectory,'blacklist.txt')
    try:
        urllib.request.urlretrieve(url_blacklist, destination)
    except urllib.error.URLError:
        return None
    if not os.path.exists(destination):
        return None
    return destination
        

def get_password_strength(password,password_list):
    if len(password) <= 6:
        return 1
    if len(set(password.lower())) == 1:
        return 2
    if password in password_list:
        return 3
    point = 3
    points = 0
    if re.search(r'[a-zа-я]', password) is not None:
        points = point + 1
    if re.search(r'[A-ZА-Я]', password) is not None:
        points = point + 2
    if re.search(r'[0-9]', password) is not None:
        points = point + 2
    if re.search(r'\W', password) is not None:
        points = point + 2
    return points


def read_blacklist(blacklist):
    with open (blacklist, 'r') as bl:
        password_list = re.findall(r'\w+', bl.read().lower())
    print (set( password_list))
    return set( password_list)


def print_results(points):
    if points == 1:
        print('Пароль слишком короткий:', points, 'из 10')
    elif points == 2:
        print('Пароль состоит из одних и тех же символов:', points, 'из 10')
    elif points == 3:
        print('Пароль распостранен(находится в blacklist):', points, 'из 10')
    else:
        print('Сложность пароля:', points,'of 10')

    
if __name__ == '__main__':
    while True:
        with tempfile.TemporaryDirectory() as tmpdirectory:
            passwords, parser, blacklist, state = read_arguments()
            if state == 1:
                print('Пароль не может содержать пробелов')
                break
            if state == 2 :
                print('Неправильно указан путь до blacklist\его не существует.'\
                      'Будет загружен стандартный blacklist')
            if blacklist is None:
                password_list = []
                print('Blacklist не скачался.Оценка будет призводиться' \
                      'без его учета')
            else:
                password_list = read_blacklist(blacklist)
        password = passwords[0]
        points = get_password_strength(password, password_list)
        print_results(points)
        break
