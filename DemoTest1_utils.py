# --- Reusable Functions --- for size, color and quantity of products
#for some product the details may differ and hence using a resuable file
import time
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

from pythontest.adsUtils import wait_and_close_ads


def select_size(driver, size_label):
    try:
        size_elem = WebDriverWait(driver, 10).until(
            expected_conditions.element_to_be_clickable((By.XPATH, f"//div[@option-label='{size_label}']"))
        )
        size_elem.click()
        print(f"[INFO] Selected size: {size_label}")
    except Exception as e:
        print(f"[WARN] Size '{size_label}' not found or not clickable. {e}")

def select_color(driver, color_label):
    try:
        color_elem = WebDriverWait(driver, 10).until(
            expected_conditions.element_to_be_clickable((By.XPATH, f"//div[@option-label='{color_label}']"))
        )
        color_elem.click()
        print(f"[INFO] Selected color: {color_label}")
    except Exception as e:
        print(f"[WARN] Color '{color_label}' not found or not clickable. {e}")


def set_quantity(driver, qty):
    try:
        # Wait until qty input is present and clickable
        qty_box = WebDriverWait(driver, 10).until(
            expected_conditions.presence_of_element_located((By.ID, "qty"))
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", qty_box)
        time.sleep(0.5)
        qty_box.clear()
        qty_box.send_keys(Keys.CONTROL, 'a')
        qty_box.send_keys(str(qty))
        qty_box.send_keys(Keys.TAB)
        print(f"[INFO] Set quantity to: {qty}")
    except Exception as e:
        print(f"[WARN] First attempt to set quantity failed. Retrying... Message: {e}")
        try:
            WebDriverWait(driver, 5).until(
                expected_conditions.presence_of_element_located((By.ID, "qty"))
            )
            time.sleep(1)
            driver.execute_script("document.querySelector('#qty').scrollIntoView(true);")
            driver.execute_script("document.querySelector('#qty').value = ''")
            driver.execute_script(f"document.querySelector('#qty').value = '{qty}'")
            print(f"[INFO] Set quantity to: {qty} via JS fallback")
        except Exception as ex:
            print(f"[ERROR] Still couldn't set quantity. Message: {ex}")