import time
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

@pytest.fixture(scope="class")
def setup(request):
    chrome_service = ChromeService(executable_path=ChromeDriverManager().install())
    driver = webdriver.Chrome(service=chrome_service)
    driver.get("https://opensource-demo.orangehrmlive.com/")
    request.cls.driver = driver
    yield
    driver.quit()

def pytest_configure(config):
    config._metadata['Module Name'] = 'Login'
    config._metadata['Project Name'] = 'OrangeHRM'

@pytest.mark.usefixtures("setup")
class TestLogin:

    def test_login_failure_incorrect_username_password(self):
        driver = self.driver
        wait = WebDriverWait(driver, 10)

        username_field = wait.until(EC.presence_of_element_located((By.NAME, "username")))
        username_field.send_keys("mahesa")

        password_field = driver.find_element(By.NAME, "password")
        password_field.send_keys("mahesa123")

        login_button = driver.find_element(By.CSS_SELECTOR, ".oxd-button")
        login_button.click()
        time.sleep(5)

        error_message = driver.find_element(By.CSS_SELECTOR, ".oxd-alert-content-text")
        assert "Invalid credentials" in error_message.text

    def test_login_failure_incorrect_password(self):
        driver = self.driver
        wait = WebDriverWait(driver, 10)

        username_field = wait.until(EC.presence_of_element_located((By.NAME, "username")))
        username_field.send_keys("admin")

        password_field = driver.find_element(By.NAME, "password")
        password_field.send_keys("mahesa123")

        login_button = driver.find_element(By.CSS_SELECTOR, ".oxd-button")
        login_button.click()
        time.sleep(5)

        error_message = driver.find_element(By.CSS_SELECTOR, ".oxd-alert-content-text")
        assert "Invalid credentials" in error_message.text

    def test_login_failure_incorrect_username(self):
        driver = self.driver
        wait = WebDriverWait(driver, 10)

        username_field = wait.until(EC.presence_of_element_located((By.NAME, "username")))
        username_field.send_keys("mahesa")

        password_field = driver.find_element(By.NAME, "password")
        password_field.send_keys("admin123")

        login_button = driver.find_element(By.CSS_SELECTOR, ".oxd-button")
        login_button.click()
        time.sleep(5)

        error_message = driver.find_element(By.CSS_SELECTOR, ".oxd-alert-content-text")
        assert "Invalid credentials" in error_message.text

    def test_login_success_correct_username_password(self):
        driver = self.driver
        wait = WebDriverWait(driver, 10)

        username_field = wait.until(EC.presence_of_element_located((By.NAME, "username")))
        username_field.send_keys("admin")

        password_field = driver.find_element(By.NAME, "password")
        password_field.send_keys("admin123")

        login_button = driver.find_element(By.CSS_SELECTOR, ".oxd-button")
        login_button.click()
        time.sleep(5)

        dashboard_header = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".oxd-topbar-header-breadcrumb-module")))
        assert "Dashboard" in dashboard_header.text

if __name__ == "__main__":
    pytest.main()
