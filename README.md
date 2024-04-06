# SteamGetAccount
# Описание
этот проект позволяет написать любой nickname и получать данные о всех аккаунтах steam в видя excel
# Нюанс
одно из требований было по этой ссылке: https://steamcommunity.com/search/users/#text=%D0%A2%D1%83%D1%82+%D0%BD%D0%B8%D0%BA парсить "Описание из аккаунта" но из этой ссылки по моему мнению не возможно парсить описание. Единственый способ парсить описание это заходить каждому аккаутну в профиль, парсить описание, выходить из профиля. Однако это бы очень сильно замедлило програму и я решил не парсить описание
# Автор
Ризабеков Алишер
# Cтек
- Python
- Django
- Selenium
- BS4
- JavaScript
- HTML
- CSS
# Как запустить локально
- Создайте вертуальное окружение
```
python -m venv venv
# Для Windows
source venv/Scripts/activate
# Для MacOS, Linux
source venv/bin/activate
```
- Обновите pip и установите зависимости
```
python -m pip install --upgrade pip
pip install -r requirements.txt
```
- укажите директерию для сохранения excel в файле \SteamGetAccount\steam\constans.py
- Запуск проекта
```
python manage.py runserver
```
- заходите на http://127.0.0.1:8000/ и вводите ник после чего в директерии которую вы указали появится excel с нужными данными
