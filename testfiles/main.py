from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
from selenium.common.exceptions import TimeoutException

def parse_steam_accounts(nickname):
    url = f'https://steamcommunity.com/search/users/#text={nickname}'
    driver = webdriver.Chrome()  # Use the path to your browser driver
    driver.get(url)
    time.sleep(5)  # Add a delay of 5 seconds to ensure the page is fully loaded
    
    accounts = []
    while True:
        # Parse main profile information
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        for account in soup.find_all("div", class_="searchPersonaInfo"):
            account_info = {}
            account_info['NickName'] = account.find('a', class_='searchPersonaName').text.strip()
            account_info['profile_link'] = account.find('a', class_='searchPersonaName')['href']
            account_info['real_name'] = account.find('br',).next_sibling.strip()
            br_tags = account.find_all('br')
            additional_info = []
            for br_tag in br_tags:
                if br_tag.next_sibling:
                    additional_info.append(br_tag.next_sibling.strip())
            account_info['additional_info'] = additional_info
            accounts.append(account_info)
            
            # Additional match info associated with the current profile
            match_info_div = account.find_next_sibling("div", class_="search_match_info")
            if match_info_div:
                match_info = match_info_div.find_all('span')
                match_info_data = [span.text.strip() for span in match_info]
                match_info_data.append({'profile_link': account_info['profile_link']})
                accounts.append({'match_info': match_info_data})
        
        # Find the "NextPage" button and click it
        try:
            next_page_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//a[@onclick='CommunitySearch.NextPage(); return false;']")))
            if next_page_button:
                next_page_button.click()
                time.sleep(5)  # Add a delay of 5 seconds to ensure the next page is fully loaded
        except TimeoutException:
            break  # Exit the loop if the "NextPage" button is not found
        
    driver.quit()
    return accounts

# Example usage
nickname = '임찌'
steam_accounts = parse_steam_accounts(nickname)
if steam_accounts:
    for account in steam_accounts:
        if 'NickName' in account:
            print(account)
        else:
            print("Совпадения:", account['match_info'])