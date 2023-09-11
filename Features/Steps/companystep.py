from behave import *
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
import time
import csv
import re

Details = []
'''Paths used '''
paths={
    'input_box_xpath':"//*[@type='search']",
    'company_name_xpath':"(//div[@class='SPZz6b']/child::h2)/child::span",
    'company_address_xpath':"(//span[@class='LrzXr'])",
    'company_rating_xpath':"(//*[@class='CJQ04']/descendant::span)[1]",
    'company_review_xpath':"(//*[@class='CJQ04']/descendant::a)",
    'direction_xpath':"(//div[@class='QqG1Sd'])[2]",
}


@given(u'He Opened Google Page')
def opening_google(context):
    '''Opening Google Page '''
    context.driver = webdriver.Chrome()
    context.driver.get('https://www.google.com/')
    context.driver.maximize_window()


@when(u'He Search Company Name "{company_name}"')
def searching_company(context, company_name):
    '''
    :param company_name: it stores the name of company given by user to store the data in string datatype
    '''
    context.company_name = company_name
    context.driver.find_element(By.XPATH, paths['input_box_xpath']).send_keys(company_name, Keys.ENTER)


@when(u'He Save Details Of Company')
def extracting_information(context):
    '''
    According to requirement extracting information from the page
    '''
    D = {}
    try:
        D['name'] = context.driver.find_element(By.XPATH,paths['company_name_xpath'] ).text
    except:
        D['name'] = context.company_name
    try:
        D['address'] = context.driver.find_element(By.XPATH, paths['company_address_xpath']).text
    except:
        D['address'] = 'Null'
    try:
        D['rating'] = context.driver.find_element(By.XPATH, paths['company_rating_xpath']).text
    except:
        D['rating'] = 'Null'
    try:
        D['reviews'] = context.driver.find_element(By.XPATH, paths['company_review_xpath']).text
    except:
        D['reviews'] = 'Null'
    try:
        directions = context.driver.find_element(By.XPATH, paths['direction_xpath']).click()
        time.sleep(5)
        url = str(context.driver.current_url)
        lan = re.search('@\d+\S{1}\d+,\d+\S{1}\d+', url)
        Log_and_Lat = lan.group()
        D['Log_and_Lat'] = Log_and_Lat.replace('@', '')
    except:
        D['Log_and_Lat'] = 'Null'
    Details.append(D)


@then(u'He Make Csv File Of That')
def makeing_csv_file(context):
    '''Making Csv File of all extracted information'''
    field_names = ['name', 'address', 'rating', 'reviews', 'Log_and_Lat']
    with open('company_report.csv', 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=field_names)
        writer.writeheader()
        writer.writerows(Details)
