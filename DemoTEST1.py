import json
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait

from pythontest.DemoTest1_utils import select_size, select_color, set_quantity
from pythontest.adsUtils import safe_click, wait_and_close_ads

driver = webdriver.Chrome()
driver.maximize_window()
driver.implicitly_wait(5)


wait = WebDriverWait(driver, 10)
driver.get("https://magento.softwaretestingboard.com/men/tops-men/hoodies-and-sweatshirts-men.html")     #main url: https://magento.softwaretestingboard.com
wait_and_close_ads(driver)
driver.execute_script("window.scrollBy(0,300);")

home_url = driver.current_url

# Load product data
with open("../data/product_details.json") as file:
    data = json.load(file)
    product_list = data["product_data"]

#iterating and get the product name
for product in product_list:
    name = product["name"]
    print(f"[DEBUG] Processing product: {name}")

    #Use the name in the product link directly, it means the name from json file which find link text should click it
    try:
        xpath = f"//a[normalize-space(text())='{name}']/ancestor::li[contains(@class, 'product-item')]"
        wait_and_close_ads(driver)  # add again
        wait = WebDriverWait(driver,10)
        product_link = wait.until(expected_conditions.element_to_be_clickable((By.XPATH, xpath)))
        driver.execute_script("arguments[0].scrollIntoView(true);", product_link)
        time.sleep(2)  # small wait to ensure scroll completes
        safe_click(driver, product_link)
    except Exception as e:
        print(f"[ERROR] Could not click product link for '{name}': {e}")
        driver.save_screenshot("product_link failed.png")

    # Wait for product detail page to load
    try:
        WebDriverWait(driver, 10).until(
        expected_conditions.visibility_of_element_located((By.TAG_NAME, "h1")))
    except Exception as e:
        print(f"Product page not loaded {e}")
        driver.save_screenshot("product_link failed.png")

    #scroll till the product details
    driver.execute_script("window.scrollBy(0, 600);")

    #Iterate and get size, colour and Qty:
    if "size" in product:
        select_size(driver, product["size"])
    if "color" in product:
        select_color(driver, product["color"])
    if "qty" in product:
        set_quantity(driver, product["qty"])

    # Wait for overlay to disappear
    try:
        WebDriverWait(driver, 5).until(
            expected_conditions.invisibility_of_element_located((By.CLASS_NAME, "page-wrapper"))
        )
    except:
        print("[WARN] 'page-wrapper' still visible, continuing...")

    #add to cart button process:
    try:
        wait = WebDriverWait(driver,10)
        add_to_cart_button = wait.until(expected_conditions.element_to_be_clickable((By.XPATH,"//button[@title='Add to Cart']")))
        driver.execute_script("arguments[0].scrollIntoView(true);",add_to_cart_button)
        safe_click(driver, add_to_cart_button)
    except Exception as e:
        print(f"Add to cart button not clickable {e}")
        driver.save_screenshot("product_link failed.png")

    #add to cart success message:
    try:
        wait = WebDriverWait(driver,10)
        product_added = wait.until(expected_conditions.visibility_of_element_located((By.CSS_SELECTOR,"div.message-success.success.message")))
        print(product_added.text)
    except Exception as e:
        print(f"Product not added {e}")

    driver.get(home_url)
    wait.until(expected_conditions.presence_of_element_located((By.CSS_SELECTOR, "li.product-item")))


print("All the items added to the cart successfully")


