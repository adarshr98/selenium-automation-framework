import json
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait

from pythontest.DemoTest1_utils import select_size, select_color, set_quantity
from pythontest.adsUtils import safe_click, wait_and_close_ads

# Setup
driver = webdriver.Chrome()
driver.maximize_window()
driver.implicitly_wait(5)
wait = WebDriverWait(driver, 10)

# Navigate to product listing page
driver.get("https://magento.softwaretestingboard.com/men/tops-men/hoodies-and-sweatshirts-men.html")
wait_and_close_ads(driver)
driver.execute_script("window.scrollBy(0,300);")
home_url = driver.current_url

# Load product data
with open("../data/product_details.json") as file:
    data = json.load(file)
    product_list = data["product_data"]

# Process each product
for product in product_list:
    name = product["name"]
    print(f"\n[DEBUG] Processing product: {name}")
    wait_and_close_ads(driver)

    # --- Locate and open correct product page ---
    try:
        products = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "li.product-item")))
        match_found = False

        for product_name in products:
            try:
                product_link = product_name.find_element(By.CSS_SELECTOR, "a.product-item-link")
                product_link_text = product_link.text.strip()
                if product_link_text.lower() == name.lower():
                    href = product_link.get_attribute("href")
                    print(f"[INFO] Navigating directly to: {href}")
                    driver.get(href)
                    match_found = True
                    break
            except Exception:
                continue

        if not match_found:
            print(f"[ERROR] Could not find product_name matching '{name}'")
            driver.save_screenshot(f"{name.replace(' ', '_')}_not_found.png")
            continue

    except Exception as e:
        print(f"[ERROR] Error while locating product tile for '{name}': {e}")
        driver.save_screenshot(f"{name.replace(' ', '_')}_tile_error.png")
        continue

    # --- Verify product page loaded correctly ---
    try:
        product_header = wait.until(EC.visibility_of_element_located((By.TAG_NAME, "h1")))
        actual_name = product_header.text.strip()
        if actual_name.lower() != name.lower():
            print(f"[ERROR] Product page mismatch: Expected '{name}' but landed on '{actual_name}'")
            driver.save_screenshot(f"{name.replace(' ', '_')}_page_mismatch.png")
            driver.get(home_url)
            continue
    except Exception as e:
        print(f"[ERROR] Product page not loaded: {e}")
        driver.save_screenshot(f"{name.replace(' ', '_')}_load_fail.png")
        driver.get(home_url)
        continue

    driver.execute_script("window.scrollBy(0, 600);")

    # --- Product option selection ---
    if "size" in product:
        select_size(driver, product["size"])
    if "color" in product:
        select_color(driver, product["color"])
    if "qty" in product:
        set_quantity(driver, product["qty"])

    # --- Wait for any overlay to disappear ---
    try:
        WebDriverWait(driver, 5).until(
            EC.invisibility_of_element_located((By.CSS_SELECTOR, ".loading-mask"))
        )
    except:
        print("[WARN] Overlay still visible. Continuing...")

    # --- Add to Cart ---
    try:
        add_to_cart_button = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[@title='Add to Cart']"))
        )
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", add_to_cart_button)
        time.sleep(0.5)
        try:
            safe_click(driver, add_to_cart_button)
        except:
            print("[WARN] Click intercepted. Retrying via JS...")
            driver.execute_script("arguments[0].click();", add_to_cart_button)
    except Exception as e:
        print(f"[ERROR] Add to cart failed for '{name}': {e}")
        driver.save_screenshot(f"{name.replace(' ', '_')}_add_to_cart_fail.png")
        driver.get(home_url)
        continue

    # --- Confirm product added to cart ---
    try:
        success_message = wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "div.message-success.success.message"))
        )
        print(f"[SUCCESS] {success_message.text.strip()}")
    except Exception as e:
        print(f"[ERROR] Product '{name}' not confirmed in cart: {e}")
        driver.save_screenshot(f"{name.replace(' ', '_')}_cart_message_fail.png")

    # --- Return to product list page ---
    driver.get(home_url)
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "li.product-item")))

# Done
print("\n✅ All products processed.")

#proceed to check_out
wait = WebDriverWait(driver,10)
product_checkout_initial_click = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,"a.action.showcart")))
product_checkout_initial_click.click()

#product_checkout_click
driver.find_element(By.XPATH,"//button[text() = 'Proceed to Checkout']").click()

#shipping address.
wait = WebDriverWait(driver,10)
shipping_address_page = wait.until(EC.visibility_of_element_located((By.TAG_NAME,"h1")))

email = "xyz@gmail.com"
driver.find_element(By.CSS_SELECTOR,"div.control._with-tooltip > input[id='customer-email']:nth-child(1)").send_keys(email)
first_name = "Adarsh"
driver.find_element(By.XPATH,"//div[@class='control']/input[@name='firstname']").send_keys(first_name)
last_name = "Ravichandran"
driver.find_element(By.CSS_SELECTOR,"div.control > input[name='lastname']").send_keys(last_name)
company = "xyz"
driver.find_element(By.XPATH,"//div[contains(@class, 'field')]//input[@name='company']").send_keys(company)
stree_address_line_one = "6/10 new delhi"
driver.find_element(By.CSS_SELECTOR,"div.control > input[name='street[0]']").send_keys(stree_address_line_one)
stree_address_line_two = "delhi"
driver.find_element(By.XPATH,"//div[@class='control']/input[@name='street[1]']").send_keys(stree_address_line_two)
city ="Noida"
locate_city = driver.find_element(By.XPATH,"//input[@name='city']")
driver.execute_script("arguments[0].scrollIntoView(true);", locate_city)
locate_city.send_keys(city)
State = "Guam"
scroll_to_state = driver.find_element(By.NAME, "region_id")
driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", scroll_to_state)
state_dropdown = Select(scroll_to_state)
state_dropdown.select_by_visible_text(State)
# Method 2: Select by index (0-based)
# country_dropdown.select_by_index(5)

# Method 3: Select by value attribute
# country_dropdown.select_by_value("IN")  # if <option value="IN">India</option>




time.sleep(2)
