'''Modules Used '''
from behave import *
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
import time
import re

'''Used Paths '''
x_paths = {
    "INPUT_AREA": "//input[@id='twotabsearchtextbox']",
    "INPUT_CLICK": "//input[@id='nav-search-submit-button']",
    "ADD_TO_CART": "//input[@id='add-to-cart-button']",
    'rating_box_xpath':"(//li[@id='p_72/1318476031']/ancestor::ul)/descendant::li",
    'filtered_product_list_xpath':"//h2[@class='a-size-mini a-spacing-none a-color-base s-line-clamp-2']/child::a",
    'added_product_price_list_xpath':"//div[@class='sc-badge-price-to-pay']",
    'total_price_showing_after_added_to_cart_xpath':"(//span[@class='a-size-medium a-color-base sc-price sc-white-space-nowrap'])[1]",
}


@given(u'User is on Amazon Page')
def open_amazon_page(context):
    """
    I opened Amazon Page
    """
    context.driver = webdriver.Chrome()
    context.driver.get("https://www.amazon.in/")
    context.driver.maximize_window()


@when(u'He Search For Product Name "{product}"')
def search_product(context, product):
    """
    Searched Product According To User Interest
    :param product: name of product we searched of str type
    """
    context.product = product.split()[0]
    wait = WebDriverWait(context.driver, 20)
    input_prod = wait.until(ec.presence_of_element_located((By.XPATH, x_paths["INPUT_AREA"])))
    input_prod.send_keys(product)
    wait.until(ec.presence_of_element_located((By.XPATH, x_paths['INPUT_CLICK']))).click()
    context.parent_url = context.driver.current_window_handle


@when(u'He filters product based on more than "{rating_value}" star rating')
def filter_product_based_on_rating(context, rating_value):
    """
    Based On Given Rating I Filtered The Product
    :param rating_value: Value of rating based on which we want to filter It is of str type
    """
    context.wait = WebDriverWait(context.driver, 10)
    rating_list = context.driver.find_elements(By.XPATH, x_paths['rating_box_xpath'])
    if float(rating_value) >= 4 and float(rating_value) <= 5:
        rating_list[0].click()
        time.sleep(5)

    elif float(rating_value) >= 3 and float(rating_value) <= 4:
        rating_list[1].click()
        time.sleep(5)

    elif float(rating_value) >= 2 and float(rating_value) <= 3:
        rating_list[2].click()
        time.sleep(5)

    elif float(rating_value) >= 1 and float(rating_value) <= 2:
        rating_list[3].click()
        time.sleep(5)

    else:
        raise Exception('Please Enter Valid Rating Value :')


@when(u'He add first "{product_count}" product to cart')
def add_to_cart(context, product_count):
    """
    Adding Filtered Product to Cart Based On Count Value
    :param product_count:It Hold Total Number Of Product We want to add to cart it is of str type

    """
    count = 0
    product_list = context.driver.find_elements(By.XPATH,
                                       x_paths['filtered_product_list_xpath'])
    for i in range(1, len(product_list)):
        if count == int(product_count):
            break
        time.sleep(5)
        if re.search(context.product, product_list[i].text):
            product_list[i].click()
            time.sleep(10)
            count += 1
            multiple_window = context.driver.window_handles
            for window in multiple_window:
                if window != context.parent_url:
                    print(context.parent_url)
                    print(window)
                    context.driver.switch_to.window(window)
                    context.wait.until(ec.element_to_be_clickable((By.XPATH, x_paths['ADD_TO_CART']))).click()
                    time.sleep(5)
                    context.driver.close()
                    multiple_window.remove(window)
                    context.driver.switch_to.window(context.parent_url)


@then(u'the cart value should be sum of products')
def checking_summarized_and_actual_price(context):
    """
    Checking Whether The Actual Price Is Same To Summarized Price Of Not
    """
    actual_price = 0
    context.driver.find_element(By.XPATH, "//div[@id='nav-cart-count-container']").click()
    price_list = context.driver.find_elements(By.XPATH, x_paths['added_product_price_list_xpath'])
    for i in range(len(price_list)):
        print(price_list[i].text)
        actual_price += float(price_list[i].text.replace(',', ''))
    summarized_price = context.driver.find_element(By.XPATH,
                                                   x_paths['total_price_showing_after_added_to_cart_xpath']).text
    print(summarized_price)
    try:
        assert float(summarized_price.replace(',', '')) == actual_price, 'Cart Is Not Performing'
    except AssertionError as msg:
        print(msg)

