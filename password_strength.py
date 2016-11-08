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
        return None, None, None
    passwords = parser.parse_args().password
    url_blacklist = parser.parse_args().url
    local_blacklist = parser.parse_args().blacklist
    return passwords, local_blacklist, url_blacklist


def check_blacklist(local_blacklist, url_blacklist):
    """
    2 в return переменная - это состояние. 
    1 - local blacklist не прошел проверку на os.path.exists,
    идет загрузка url_blacklist
    2 - local_blacklist существует, но прочитать нельзя, не тот формат,
    идет загрузка url_blacklist
    3 - передается local_blacklist
    """
    if local_blacklist is None:
        return get_blacklist(url_blacklist), None
    else:
        if os.path.exists(local_blacklist):
            if read_blacklist(local_blacklist) is not None:
                return read_blacklist(local_blacklist), 4
            else:
                return get_blacklist(url_blacklist), 2
        else:
            return get_blacklist(url_blacklist), 1
    

def get_blacklist(url_blacklist):
    destination = os.path.join(tmpdirectory,'blacklist.txt')
    try:
        urllib.request.urlretrieve(url_blacklist, destination)
    except urllib.error.URLError:
        return None
    if not os.path.exists(destination):
        return None
    return read_blacklist(destination)


def read_blacklist(blacklist):
    try:
        with open (blacklist, 'r') as bl:
            password_list = re.findall(r'\w+', bl.read().lower())
        return set( password_list)
    except ValueError:
        return None        


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
        passwords, local_blacklist ,url_blacklist = read_arguments()
        if passwords is None:
            print('Пароль не может содержать пробелов')
            break
        with tempfile.TemporaryDirectory() as tmpdirectory:
            blacklist, state = check_blacklist(local_blacklist, url_blacklist)
        if state == 1 :
            print('Неправильно указан путь до blacklist\его не существует.'\
                    'Будет загружен стандартный blacklist')
        if state == 2:
            print('Неправильный формат.'\
                    'Будет загружен стандартный blacklist')
        if blacklist is None:
            print('Blacklist не скачался')
            blacklist = []
        password = passwords[0]
        points = get_password_strength(password, blacklist)
        print_results(points)
        break
