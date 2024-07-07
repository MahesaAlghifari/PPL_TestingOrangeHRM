import time
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

class TestAdmin:

    @classmethod
    def setup_class(cls):
        chrome_service = ChromeService(executable_path=ChromeDriverManager().install())
        cls.driver = webdriver.Chrome(service=chrome_service)
        cls.driver.get("https://opensource-demo.orangehrmlive.com/")

        wait = WebDriverWait(cls.driver, 10)
        username_field = wait.until(EC.presence_of_element_located((By.NAME, "username")))
        username_field.send_keys("admin")

        password_field = wait.until(EC.presence_of_element_located((By.NAME, "password")))
        password_field.send_keys("admin123")

        login_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".oxd-button")))
        login_button.click()
        
        admin_menu = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".oxd-main-menu-item")))
        admin_menu.click()
        
        time.sleep(5)
        

    @classmethod
    def teardown_class(cls):
        cls.driver.quit()

if __name__ == "__main__":
    pytest.main()
