import os
import time

import openpyxl
from bs4 import BeautifulSoup
from django.shortcuts import render
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait

from .constans import (EXCEL_SAVE_DIRECTORY, WAIT_FOR_FIRST_LOADING,
                       WAIT_FOR_NEXT_LOADING)


def parse_steam_accounts(nickname):
    url = f'https://steamcommunity.com/search/users/#text={nickname}'
    driver = webdriver.Chrome()
    driver.get(url)
    time.sleep(WAIT_FOR_FIRST_LOADING)

    accounts = []
    while True:
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

            match_info_div = account.find_next_sibling("div", class_="search_match_info")
            if match_info_div and "Также известен как:" in match_info_div.text:
                match_info = match_info_div.find_all('span')
                match_info_data = [span.text.strip() for span in match_info]
                account_info['match_info'] = match_info_data

            accounts.append(account_info)

        try:
            next_page_button = WebDriverWait(driver, 10).until(ec.presence_of_element_located((By.XPATH, "//a[@onclick='CommunitySearch.NextPage(); return false;']")))
            if next_page_button:
                next_page_button.click()
                time.sleep(WAIT_FOR_NEXT_LOADING)
        except TimeoutException:
            break

    driver.quit()
    return accounts


def save_to_excel(data, filename):
    save_path = os.path.join(EXCEL_SAVE_DIRECTORY, filename)
    wb = openpyxl.Workbook()
    ws = wb.active
    for account in data:
        if 'NickName' in account:
            name = ''
            country = ''
            if len(account.get('additional_info', [])) >= 2:
                name, country = account['additional_info']
            elif len(account.get('additional_info', [])) == 1:
                country = account['additional_info'][0]

            row = [account.get('profile_link', ''),
                   '',
                   country,
                   name]

            # Добавление match_info в следующие столбцы
            match_info = account.get('match_info', [])
            row.extend(match_info)

            ws.append(row)

    for column in ws.columns:
        max_length = 0
        for cell in column:
            try:
                if len(str(cell.value)) > max_length:
                    max_length = len(cell.value)
            except:
                pass
        adjusted_width = max_length+5
        ws.column_dimensions[column[0].column_letter].width = adjusted_width

    wb.save(save_path)


def index(request):
    if request.method == 'POST':
        nickname = request.POST.get('nickname')
        steam_accounts = parse_steam_accounts(nickname)
        if steam_accounts:
            save_to_excel(steam_accounts, 'steam_accounts.xlsx')
            return render(request, 'index.html', {'completed': True})
    return render(request, 'index.html', {'completed': False})
