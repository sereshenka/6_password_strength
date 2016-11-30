# 6_password_strength
#Что делает этот скрипт?#
Задача скриппта оценить сложность пароля(от 1 до 10).
#Инструкция:#
Указывать пароль нужно через --password. Есть возможность исользовать как стандартный blacklist,так и локальный или указать сайт с ним(blacklistом). Если локальный или url blacklist не указывается, то скрипт автоматически скачивает стандартный словарь для проверки,если же указывается локальный blacklist,то проверяется по локальному словарю,также и с url blacklist-ом. Если указан и локальный,и url blacklist будет использован локальный словарь,а в случае,если его не сущетсвует или путь к фаилу задан не правильно, то будет использован url blacklist.
#Как запустить?#
*python3 password_strength.py --password your_password*

*python3 password_strength.py --password your_password --url_blacklist your_url*

*python3 password_strength.py --password your_password --local_blacklist your_path*
