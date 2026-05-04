import os
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@pytest.fixture
def driver():
    """Запуск браузера и открытие страницы банка"""
    balance = os.getenv("BALANCE", "30000")
    reserved = os.getenv("RESERVED", "20001")

    url = f"http://localhost:8000/?balance={balance}&reserved={reserved}"

    options = Options()
    options.add_argument("--headless")  # Фоновый режим (без открытия окна)
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=options)
    driver.get(url)
    yield driver
    driver.quit()

@pytest.fixture
def open_transfer_menu(driver):
    """Открывает меню перевода по рублёвому счёту"""
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

    ruble_card = wait.until(EC.element_to_be_clickable((By.XPATH, "//h2[text()='Рубли']/..")))
    ruble_card.click()

    return driver