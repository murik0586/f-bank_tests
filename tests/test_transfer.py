import pytest
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class TestFakeBank:

    def test_card_17_digits_bug(self, open_transfer_menu):
        driver = open_transfer_menu

        card_input = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, "//input[@placeholder='0000 0000 0000 0000']"))
        )
        card_input.clear()
        card_input.send_keys("11112222333344445")

        entered_value = card_input.get_attribute("value").replace(" ", "")
        assert len(entered_value) <= 16, f"БАГ: В поле можно ввести больше 16 цифр: {len(entered_value)}"

    def test_transfer_zero_rubles_bug(self, open_transfer_menu):
        driver = open_transfer_menu

        card_input = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, "//input[@placeholder='0000 0000 0000 0000']"))
        )
        card_input.send_keys("1111222233334444")

        time.sleep(1)

        amount_input = driver.find_element(By.XPATH, "//input[@placeholder='1000']")
        amount_input.clear()
        amount_input.send_keys("0")

        transfer_btn = driver.find_element(By.XPATH, "//span[text()='Перевести']/ancestor::button")
        transfer_btn.click()

        alert = WebDriverWait(driver, 3).until(EC.alert_is_present())
        alert_text = alert.text
        alert.accept()

        assert "принят" not in alert_text, f"БАГ: Перевод 0 рублей не должен проходить, но получено: {alert_text}"

    def test_empty_amount_bug(self, open_transfer_menu):
        driver = open_transfer_menu

        card_input = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, "//input[@placeholder='0000 0000 0000 0000']"))
        )
        card_input.send_keys("1111222233334444")

        time.sleep(1)

        amount_input = driver.find_element(By.XPATH, "//input[@placeholder='1000']")
        amount_input.clear()

        transfer_btn = driver.find_element(By.XPATH, "//span[text()='Перевести']/ancestor::button")
        transfer_btn.click()

        alert = WebDriverWait(driver, 3).until(EC.alert_is_present())
        alert_text = alert.text
        alert.accept()

        assert "принят" not in alert_text, f"БАГ: Перевод с пустой суммой не должен проходить, но получено: {alert_text}"

    def test_negative_amount_bug(self, open_transfer_menu):
        driver = open_transfer_menu

        card_input = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, "//input[@placeholder='0000 0000 0000 0000']"))
        )
        card_input.send_keys("1111222233334444")

        time.sleep(1)

        amount_input = driver.find_element(By.XPATH, "//input[@placeholder='1000']")
        amount_input.clear()
        amount_input.send_keys("-100")

        transfer_btn = driver.find_element(By.XPATH, "//span[text()='Перевести']/ancestor::button")
        transfer_btn.click()

        alert = WebDriverWait(driver, 3).until(EC.alert_is_present())
        alert_text = alert.text
        alert.accept()

        assert "принят" not in alert_text, f"БАГ: Перевод отрицательной суммы не должен проходить, но получено: {alert_text}"

    def test_commission_rounding_bug(self, open_transfer_menu):
        driver = open_transfer_menu

        card_input = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, "//input[@placeholder='0000 0000 0000 0000']"))
        )
        card_input.send_keys("1111222233334444")

        time.sleep(1)

        amount_input = driver.find_element(By.XPATH, "//input[@placeholder='1000']")
        amount_input.clear()
        amount_input.send_keys("99")

        commission_span = WebDriverWait(driver, 3).until(
            EC.presence_of_element_located((By.ID, "comission"))
        )
        commission_text = commission_span.text
        assert commission_text == "9", f"БАГ: Комиссия должна быть 9, но отображается {commission_text}"

    def test_commission_9091_bug(self, open_transfer_menu):
        driver = open_transfer_menu

        card_input = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, "//input[@placeholder='0000 0000 0000 0000']"))
        )
        card_input.send_keys("1234542315432151")

        time.sleep(1)

        amount_input = driver.find_element(By.XPATH, "//input[@placeholder='1000']")
        amount_input.clear()
        amount_input.send_keys("9091")

        commission_span = WebDriverWait(driver, 3).until(
            EC.presence_of_element_located((By.ID, "comission"))
        )
        commission_text = commission_span.text
        assert commission_text == "909", f"БАГ: Комиссия для 9091 должна быть 909, но отображается {commission_text}"

    def test_positive_transfer(self, open_transfer_menu):
        driver = open_transfer_menu

        card_input = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, "//input[@placeholder='0000 0000 0000 0000']"))
        )
        card_input.send_keys("1111222233334444")

        time.sleep(1)

        amount_input = driver.find_element(By.XPATH, "//input[@placeholder='1000']")
        amount_input.clear()
        amount_input.send_keys("1000")

        commission_span = driver.find_element(By.ID, "comission")
        assert commission_span.text == "100", "Комиссия должна быть 100"

        transfer_btn = driver.find_element(By.XPATH, "//span[text()='Перевести']/ancestor::button")
        assert transfer_btn.is_enabled(), "Кнопка должна быть активна"