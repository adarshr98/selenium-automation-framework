from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException, TimeoutException
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait


def close_ads(driver):
    try:
        ad_button = driver.find_element(By.XPATH, "//div[contains(@class, 'sa-button-container')]//button[text()='OK']")
        ad_button.click()
        print("[INFO] Ad popup closed.")
    except:
        print("[INFO] No ad popup found or already closed.")

def safe_click(driver, element):
    from selenium.webdriver.common.action_chains import ActionChains
    try:
        ActionChains(driver).move_to_element(element).perform()
        element.click()
    except Exception as e:
        print(f"[WARN] First click attempt failed: {e}. Retrying via JS...")
        try:
            driver.execute_script("arguments[0].click();", element)
        except Exception as ex:
            print(f"[ERROR] Still not clickable: {ex}")


def wait_and_close_ads(driver, max_attempts=5):
    """
    Tries to close or hide ad iframes and overlaying ad elements like <ins>.
    """
    for attempt in range(1, max_attempts + 1):
        try:
            ad_iframes = driver.find_elements(By.CSS_SELECTOR, "iframe[id^='aswift_'], iframe[src*='doubleclick']")
            ad_ins_tags = driver.find_elements(By.CSS_SELECTOR, "ins.adsbygoogle")

            for iframe in ad_iframes:
                try:
                    driver.execute_script("""
                        arguments[0].style.display = 'none';
                        arguments[0].style.visibility = 'hidden';
                        arguments[0].style.opacity = '0';
                        arguments[0].style.pointerEvents = 'none';
                    """, iframe)
                except Exception as inner_e:
                    print(f"[WARN] Could not hide iframe: {inner_e}")

            for ins_tag in ad_ins_tags:
                try:
                    driver.execute_script("""
                        arguments[0].style.display = 'none';
                        arguments[0].style.visibility = 'hidden';
                        arguments[0].style.opacity = '0';
                        arguments[0].style.pointerEvents = 'none';
                        arguments[0].remove();
                    """, ins_tag)
                except Exception as inner_e:
                    print(f"[WARN] Could not hide <ins>: {inner_e}")

            if ad_iframes or ad_ins_tags:
                print(f"[INFO] Ad iframe and container divs hidden successfully on attempt {attempt}")
                return
            else:
                print(f"[INFO] No ad found on attempt {attempt}")

        except Exception as e:
            print(f"[WARN] Ad removal exception: {e}")

        time.sleep(1)

    print("[INFO] No ad popup found or already closed.")



#why to use javascript executor when we have explicit waits?

# BUT — When .click() Still Fails Even After Wait
# Yes, this happens. Even if element_to_be_clickable passes, .click() might still fail if:
# Problem	Why click() still fails
# Overlays still cover the element	Wait doesn't detect that it’s blocked by another layer
# Element animates in/out	Appears clickable, but DOM state is unstable
# Custom JavaScript prevents interaction	Site’s scripts hijack clicks or use event delegation
# Element rendered inside a shadow DOM or iframe	Wait works, but .click() hits a boundary Selenium can't cross

#Basically we should try performin with explicit waits before jumping into javascript executor