from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

from pythontest.adsUtils import safe_click

driver = webdriver.Firefox()

driver.get("https://www.saucedemo.com/")

driver.maximize_window()
driver.implicitly_wait(5)

home_url = driver.current_url  #.current_url gives you the url mentioned above in driver.get() - basically we are asking to go to home page

#Login page:
user_name = "standard_user"
driver.find_element(By.XPATH,"//div[@class='login-box']//input[@name='user-name']").send_keys(user_name)
password = "secret_sauce"
driver.find_element(By.CSS_SELECTOR,"div.login-box > form > div:nth-child(2) > input[name='password']").send_keys(password)
driver.find_element(By.XPATH,"//input[@id='login-button']").click()

#product page:
wait = WebDriverWait(driver,10)
productPageTitle = wait.until(expected_conditions.visibility_of_element_located((By.XPATH, "//div[contains(text(), 'Swag')]"))).text
print(productPageTitle) #output: Swag Labs, contains(text(), 'Swag') doesn't mean "only Swag", It means "any element whose text includes Swag". So Swag Labs, Swag!, Best Swag Ever — all are matched.

actual_list = ['Sauce Labs Backpack', 'Test.allTheThings() T-Shirt (Red)']
added_list = []

products = driver.find_elements(By.XPATH,"//div[@class='inventory_item']")

for product in products:
    product_name = product.find_element(By.CSS_SELECTOR,"div.inventory_item_name").text

    try:
        if product_name in actual_list and product_name not in added_list:
            add_to_cart_button = product.find_element(By.XPATH,".//div[@class='pricebar']/button")
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", add_to_cart_button)
            try:
                safe_click(driver, add_to_cart_button)
                print("All the products added to the cart")
            except:
                driver.execute_script("arguments[0].click();", add_to_cart_button)
                print("Click intercepted")

            added_list.append(product_name)
    except:
        print("Failed to locate the add-to-cart element")

#cart box click
driver.find_element(By.CSS_SELECTOR,"a.shopping_cart_link").click()

#product description page:
wait = WebDriverWait(driver,10)
wait.until(expected_conditions.visibility_of_element_located((By.XPATH,"//div[text()='Swag Labs']")))

price_details = driver.find_elements(By.CSS_SELECTOR,"div.inventory_item_price")

sum = 0
for price in price_details:
    price_text = price.text.strip()
    price_total = float(price_text.replace("$", ""))
    sum = sum + price_total
print(sum)

driver.find_element(By.CSS_SELECTOR,"div.cart_footer > button:nth-of-type(2)").click()

#Checkout information page:
name = "Adarsh"
driver.find_element(By.ID,"first-name").send_keys(name)
last_name = "Ravichandran"
driver.find_element(By.ID,"last-name").send_keys(last_name)
pincode = "0101"
driver.find_element(By.ID,"postal-code").send_keys(pincode)

action = ActionChains(driver)

#normal click will work- used JS just for practise
continue_button = driver.find_element(By.XPATH,"//div[@class='checkout_info_wrapper']/form/div[2]/input[@id='continue']")
action.move_to_element(continue_button).perform()
driver.execute_script("arguments[0].click();", continue_button)

#Checkout: Overview Page
wait = WebDriverWait(driver,10)
checkoutOverviewPage = wait.until(expected_conditions.visibility_of_element_located((By.CSS_SELECTOR,"div.header_container > div:nth-of-type(2) > span"))).text
print(checkoutOverviewPage)

finish_button = driver.find_element(By.XPATH,"//div[@class='cart_footer']/button[2]")
driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", finish_button)
safe_click(driver,finish_button)

#FinalPage:
wait = WebDriverWait(driver,10)
ThankYouMsg = wait.until(expected_conditions.visibility_of_element_located((By.XPATH,"//h2[contains(text(), 'Thank you')]"))).text
print(ThankYouMsg)

driver.get(home_url) #it goes back to the login page

assert "Swag Labs" in productPageTitle, "Expected text not found"
assert sorted(added_list) == sorted(actual_list)
assert sum == 45.98, f"Expected total 45.98, but got {sum}"
assert "THANK YOU" in ThankYouMsg.upper(), "ThankYou message not found in the Final Page"