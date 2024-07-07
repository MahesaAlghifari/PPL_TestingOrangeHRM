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
        time.sleep(5)
        
    def test_add_user_failure_all_are_not_filled_in(self):
        driver = self.driver
        wait = WebDriverWait(driver, 10)

        admin_menu = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".oxd-main-menu-item")))
        admin_menu.click()

        add_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".oxd-icon.bi-plus")))
        add_button.click()

        save_button = wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div/div[1]/div[2]/div[2]/div/div/form/div[3]/button[2]")))
        save_button.click()

        time.sleep(3)

    def test_add_user_failure_unselect_userRole_status(self):
        driver = self.driver
        wait = WebDriverWait(driver, 10)

        admin_menu = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".oxd-main-menu-item")))
        admin_menu.click()

        add_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".oxd-icon.bi-plus")))
        add_button.click()

        employee_name_field = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Type for hints...']")))
        employee_name_field.send_keys("joker john selvam")

        username_field = wait.until(EC.presence_of_element_located((By.XPATH, "//label[text()='Username']/following::input[1]")))
        username_field.send_keys("john.smith")

        password_field = wait.until(EC.presence_of_element_located((By.XPATH, "//label[text()='Password']/following::input[1]")))
        password_field.send_keys("password123")

        confirm_password_field = wait.until(EC.presence_of_element_located((By.XPATH, "//label[text()='Confirm Password']/following::input[1]")))
        confirm_password_field.send_keys("password123")

        # role_button = wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div/div[1]/div[2]/div[2]/div/div/form/div[1]/div/div[1]/div/div[2]")))
        # role_button.click()

        # status_button = wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div/div[1]/div[2]/div[2]/div/div/form/div[1]/div/div[3]/div/div[2]/div/div/div[1]")))
        # status_button.click()

        save_button = wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div/div[1]/div[2]/div[2]/div/div/form/div[3]/button[2]")))
        save_button.click()

        time.sleep(3)

    def test_add_user_success_all_filled_in(self):
        driver = self.driver
        wait = WebDriverWait(driver, 10)

        admin_menu = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".oxd-main-menu-item")))
        admin_menu.click()

        add_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".oxd-icon.bi-plus")))
        add_button.click()

        employee_name_field = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Type for hints...']")))
        employee_name_field.send_keys("joker john selvam")

        username_field = wait.until(EC.presence_of_element_located((By.XPATH, "//label[text()='Username']/following::input[1]")))
        username_field.send_keys("john.smith")

        password_field = wait.until(EC.presence_of_element_located((By.XPATH, "//label[text()='Password']/following::input[1]")))
        password_field.send_keys("password123")

        confirm_password_field = wait.until(EC.presence_of_element_located((By.XPATH, "//label[text()='Confirm Password']/following::input[1]")))
        confirm_password_field.send_keys("password123")

        role_button = wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div/div[1]/div[2]/div[2]/div/div/form/div[1]/div/div[1]/div/div[2]")))
        role_button.click()

        status_button = wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div/div[1]/div[2]/div[2]/div/div/form/div[1]/div/div[3]/div/div[2]/div/div/div[1]")))
        status_button.click()

        save_button = wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div/div[1]/div[2]/div[2]/div/div/form/div[3]/button[2]")))
        save_button.click()

        time.sleep(3)

    @classmethod
    def teardown_class(cls):
        cls.driver.quit()

if __name__ == "__main__":
    pytest.main()
