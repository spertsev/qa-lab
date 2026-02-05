import time
import allure


@allure.title("Открытие главной страницы Google")
def test_open_google(browser):
    with allure.step("Открыть страницу Google"):
        browser.get("https://www.google.com")

    with allure.step("Проверить, что заголовок страницы содержит 'Google'"):
        assert "Google" in browser.title

    time.sleep(300)
