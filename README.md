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
# Как запустить локально(Windows)
- Создайте и активируйте вертуальное окружение
```
python -m venv venv
source venv/Scripts/activate
```
- Обновите pip и установите зависимости
```
python -m pip install --upgrade pip
pip install -r requirements.txt
```
- укажите директерию для сохранения excel в файле \SteamGetAccount\steam\constans.py
- 
```

```
