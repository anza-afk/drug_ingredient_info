from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

import os
import sys

sys.path.append(os.getcwd())
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "drugs_info.settings")

import django
django.setup()
from drugs_api.models import DrugLink


def get_drug_links(browser, url):
    browser.get(url)
    abc_window = browser.find_element(
        By.CLASS_NAME, 'b-alphabet-body').find_element(By.CLASS_NAME, 'head')
    letters = [a.get_attribute('href') for a in abc_window.find_elements(By.TAG_NAME, 'a')]
    for a in letters:
        browser.get(a)
        with open('kirill-petooh.txt', 'a', encoding='UTF-8') as f:
            abc_list = browser.find_element(By.CLASS_NAME, 'b-alphabet-index')
            links = abc_list.find_elements(By.CLASS_NAME, 'link')
            for link in links:
                drug_link = DrugLink(url=link.get_attribute("href"))
                drug_link.save()


def rls_authorization(browser, auth_url, auth_data):
    browser.get(auth_url)
    browser.find_element(By.ID, 'email').send_keys(auth_data['login'])
    browser.find_element(By.ID, 'password').send_keys(auth_data['password'])
    browser.find_element(By.CLASS_NAME, 'btn').click()

    try:
        browser.find_element(By.CLASS_NAME, 'card-header')
        buttons = browser.find_elements(By.CLASS_NAME, 'btn')
        for button in buttons:
            if button.text == 'Продолжить':
                button.click()
    except NoSuchElementException:
        pass

    try:
        title = browser.find_element(By.CLASS_NAME, 'card-header')
        if title.text == 'Выбор аккаунта':
            buttons = browser.find_elements(By.CLASS_NAME, 'btn')
            for button in buttons:
                if button.text == 'Разрешить':
                    button.click()
    except NoSuchElementException:
        pass


def get_drug_info(browser, drug_url):
    drug_dict = {
        'name': None,
        'active_ingredient': [],
        'pharmacological_class': None,
        'form_of_release': None,
        'recipe_only': None,
    }
    browser.get(drug_url)
    slist = browser.find_element(By.CLASS_NAME, 'structure-list')
    drug_dict['name'] = browser.find_element(By.CLASS_NAME, 'heading').text
    if 'Действующее вещество' in slist.text:
        drug_dict['active_ingredient'].append(browser.find_element(
            By.XPATH, "//h2[@id='deistvuyushhee-veshhestvo']/following-sibling::div").text)
    if 'Фармакологическая группа' in slist.text:
        drug_dict['pharmacological_class'] = browser.find_element(
            By.XPATH, "//h2[@id='farmakologiceskaya-gruppa']/following-sibling::div").text
    if 'Форма выпуска' in slist.text:
        drug_dict['form_of_release'] = browser.find_element(
            By.XPATH, "//h2[@id='forma-vypuska']/following-sibling::div").text
    if 'Условия отпуска из аптек' in slist.text:
        drug_dict['recipe_only'] = browser.find_element(
            By.XPATH, "//h2[@id='usloviya-otpuska-iz-aptek']/following-sibling::div").text
    return drug_dict