import json
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

import pytest

from pageObjects.FinalPage import FinalPage
from pageObjects.checkoutInformationPage import CheckoutInformation
from pageObjects.checkoutOverviewPage import CheckoutOverview
from pageObjects.loginPage import LoginPage
from pageObjects.shopDescriptionPage import ShopDescription
from pageObjects.shopPage import ShopPage
from pythontest.adsUtils import safe_click

test_data_path = "../data/DemoTest2_details.json"
with open(test_data_path) as f:
    test_data = json.load(f)
    test_list = test_data["LoginCredentials"]

@pytest.mark.parametrize("test_list_item",test_list)
def test_DemoTest2(browserInstance, test_list_item):
    driver = browserInstance
    loginPage = LoginPage(driver)
    loginPage.login(test_list_item["UserName"], test_list_item["Password"])
    shopPage = ShopPage(driver)
    productPageTitle, added_list, actual_list = shopPage.shop(test_list_item["ProductName"])
    #productPageTitle, added_list, actual_list- this is not a variable to the ProductName, this is that we are
    #returing productPageTitle, added_list, actual_list from the shop POM, because we are using assertion for them
    #basically if we are using assertion- assertion expects the values to be returned, if we are not using assertion then it's not needed to be returned.
    shopPage.add_to_cart_full_box_click()
    shop_description_page = ShopDescription(driver)
    total_price = shop_description_page.shopDescription()
    #here the same like mentioned above, since we are using assertion for total_price, we are returning from
    #shop description page and mentioning the returned value here where the total price exists in shop description page
    shop_description_page.checkoutButton()
    checkout_info_page = CheckoutInformation(driver)
    checkout_info_page.checkout_info(test_list_item["FirstName"], test_list_item["LastName"], test_list_item["PinCode"])
    checkout_info_page.continue_click_info_button()
    checkout_Overview_page = CheckoutOverview(driver)
    checkout_Overview_page.checkout_overview()
    checkout_Overview_page.checkout_overview_finish_button()
    final_page_text = FinalPage(driver)
    ThankYouMsg = final_page_text.final_page()

    assert "Swag Labs" in productPageTitle, "Expected text not found"
    assert sorted(added_list) == sorted(actual_list)
    expected_price = float(test_list_item["ExpectedPrice"])
    #used ExpectedPrice in json file because, the test runs the product once at a time, so it calculated first product's
    #price and then second come after that, so since we are doing assertion we initially tried validating the whole price
    #and hence used Expected price inidividually in the json file
    assert total_price == expected_price, f"Expected total {expected_price}, but got {sum}"
    assert "THANK YOU" in ThankYouMsg.upper(), "ThankYou message not found in the Final Page"