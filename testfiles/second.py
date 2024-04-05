from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
from selenium.common.exceptions import TimeoutException
import openpyxl

def parse_steam_accounts(nickname):
    url = f'https://steamcommunity.com/search/users/#text={nickname}'
    driver = webdriver.Chrome()  # Используйте путь к вашему драйверу браузера
    driver.get(url)
    time.sleep(5)  # Добавляем задержку на 5 секунд для полной загрузки страницы
    
    accounts = []
    while True:
        # Разбор основной информации профиля
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        for account in soup.find_all("div", class_="searchPersonaInfo"):
            account_info = {}
            account_info['NickName'] = account.find('a', class_='searchPersonaName').text.strip()
            account_info['profile_link'] = account.find('a', class_='searchPersonaName')['href']
            br_tags = account.find_all('br')
            additional_info = []
            for br_tag in br_tags:
                if br_tag.next_sibling:
                    additional_info.append(br_tag.next_sibling.strip())
            account_info['additional_info'] = additional_info
            
            # Дополнительная информация о совпадениях, связанных с текущим профилем
            match_info_div = account.find_next_sibling("div", class_="search_match_info")
            if match_info_div and "Также известен как:" in match_info_div.text:
                match_info = match_info_div.find_all('span')
                match_info_data = [span.text.strip() for span in match_info]
                account_info['match_info'] = match_info_data
                
            accounts.append(account_info)
        
        # Находим кнопку "NextPage" и нажимаем на нее
        try:
            next_page_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//a[@onclick='CommunitySearch.NextPage(); return false;']")))
            if next_page_button:
                next_page_button.click()
                time.sleep(5)  # Добавляем задержку на 5 секунд для полной загрузки следующей страницы
        except TimeoutException:
            break  # Выходим из цикла, если кнопка "NextPage" не найдена
        
    driver.quit()
    return accounts

# Сохранение данных в Excel
def save_to_excel(data, filename):
    wb = openpyxl.Workbook()
    ws = wb.active
    for account in data:
        if 'NickName' in account:
            row = [account.get('NickName', ''),
                   account.get('profile_link', ''),
                   ', '.join(account.get('additional_info', ''))]
            # Добавление match_info в отдельные столбцы
            if 'match_info' in account:
                for match_info in account['match_info']:
                    row.append(match_info)
            ws.append(row)
    # Изменение ширины столбцов
    for column in ws.columns:
        max_length = 0
        for cell in column:
            try:
                if len(str(cell.value)) > max_length:
                    max_length = len(cell.value)
            except:
                pass
        adjusted_width = max_length+2  # Подстройка множителя по мере необходимости
        ws.column_dimensions[column[0].column_letter].width = adjusted_width

    wb.save(filename)

# Пример использования
nickname = '임찌'
steam_accounts = parse_steam_accounts(nickname)
if steam_accounts:
    save_to_excel(steam_accounts, 'steam_accounts.xlsx')
    print("Данные сохранены в steam_accounts.xlsx")