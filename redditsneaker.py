import bs4, time, sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from config import size, fname, lname, street, zipcode, city, state_code, phone, email, ccnumber, ccmonth, ccyear, cccsv

#current bugs
#sometimes fails to add shoe to cart, when this happens restart the script

#put url of shoes
url = 'http://www.footlocker.com/product/model:98963/sku:24300657/nike-air-force-1-low-mens/all-white/white/?cm='

cart_url = 'http://www.footlocker.com/shoppingcart/default.cfm?sku='
shipping_info_loaded = False
credit_info_loaded = False
successful_load = False

browser = webdriver.Firefox()
size_formatted = str(size).zfill(2)
print('Loading page...')
while successful_load == False:
    browser.get(url)

    #size
    print('Selecting size...')
    (browser.find_element_by_id('pdp_size_select_mask')).click()
    size_select_path = "//span[@id='size_selection_list']/a[@data-modelsize='" + size_formatted +"_0']"
    elem = browser.find_element_by_xpath(size_select_path)
    elem.click()
    print('Successful!')

    #add to cart
    print('Adding to cart...')
    add_to_cart = browser.find_element_by_id('pdp_addtocart_button')
    add_to_cart.click()
    print('Successful!')
    print('Going to cart...')
    browser.get(cart_url)
    if browser.current_url != 'http://www.footlocker.com/catalog/emptyCart.cfm?cartIsEmpty=1':
        print('Going to checkout...')
        checkout = browser.find_element_by_xpath('//*[@id="cart_checkout_button"]')
        checkout.click()
        print('Successful!')
        print('Going to billing...')
        successful_load = True
    
#waits for page to load

try:
    element = WebDriverWait(browser, 300).until(EC.presence_of_element_located((By.XPATH, '//*[@id="billFirstName"]')))
    print('Page loaded')
    shipping_info_loaded = True
except TimeoutException:
    print('Page took too long to load')

if shipping_info_loaded == True:
    time.sleep(1)
    print('Filling out shipping info')
    first_name = browser.find_element_by_xpath('//*[@id="billFirstName"]')
    first_name.send_keys(fname)
    last_name = browser.find_element_by_xpath('//*[@id="billLastName"]')
    last_name.send_keys(lname)
    street_elem = browser.find_element_by_xpath('//*[@id="billAddress1"]')
    street_elem.send_keys(street)
    zipcode_elem = browser.find_element_by_xpath('//*[@id="billPostalCode"]')
    zipcode_elem.send_keys(zipcode)
    city_elem = browser.find_element_by_xpath('//*[@id="billCity"]')
    city_elem.send_keys(city)
    state_elem = browser.find_element_by_xpath('//*[@id="billState"]/option[' + state_code +  ']')
    state_elem.click()
    phone_elem = browser.find_element_by_xpath('//*[@id="billHomePhone"]')
    phone_elem.send_keys(phone)
    email_elem = browser.find_element_by_xpath('//*[@id="billEmailAddress"]')
    email_elem.send_keys(email)
    email_elem.submit()
    print('Successful!')
    print('Skipping delivery options')
    next_step = browser.find_element_by_xpath('//*[@id="billPaneContinue"]')
    next_step.click()
    if browser.current_url == 'http://www.footlocker.com/shoppingcart/?sessionExpired=true':
        successful_load = False
    print('Button clicked')
    
    try:
        element = WebDriverWait(browser, 300).until(EC.presence_of_element_located((By.XPATH, '//*[@id="shipMethod3"]')))
        print('Page passed')
        next_step_loaded = True
        print('Successful!')
        print('Loading next step')
        if next_step_loaded == True:
            next_step_2 = browser.find_element_by_xpath('//*[@id="shipMethodPaneContinue"]')
            next_step_2.click()
    except TimeoutException:
        print('Page took too long to load')
        
try:
    element = WebDriverWait(browser, 300).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="payMethodPanestoredCCCardNumber"]')))
    print('Page loaded')
    credit_info_loaded = True
except TimeoutException:
    print('Page took too long to load')

if credit_info_loaded == True:
    time.sleep(1)
    print('Filling out credit card information')
    credit_card_number = browser.find_element_by_xpath('//*[@id="CardNumber"]')
    credit_card_number.send_keys(ccnumber)
    credit_card_number_month = browser.find_element_by_xpath('//*[@id="CardExpireDateMM"]')
    credit_card_number_month.send_keys(ccmonth)
    credit_card_number_year = browser.find_element_by_xpath('//*[@id="CardExpireDateYY"]')
    credit_card_number_year.send_keys(ccyear)
    time.sleep(1)
    print('Filling out csv')
    credit_card_number_csv = browser.find_element_by_xpath('//*[@id="CardCCV"]')
    credit_card_number_csv.send_keys(cccsv)
    credit_card_number_csv.submit()
    print('Successful')
    continueButton = browser.find_element_by_xpath('//*[@id="payMethodPaneContinue"]')
    continueButton.click()

    try:
        element = WebDriverWait(browser, 300).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="orderSubmit"]')))
        print('Submitting order')
        submit = browser.find_element_by_xpath('//*[@id="orderSubmit"]')
        submit.click()
        print('Order submitted. All done!')
    except TimeoutException:
        print('Page took too long to load')

