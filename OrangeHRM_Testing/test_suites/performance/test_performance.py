import time
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

class TestPerformance:

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

    def test_add_kpi_success(self):
        driver = self.driver
        wait = WebDriverWait(driver, 10)

        # Navigate to Performance > KPIs
        performance_menu = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[text()='Performance']")))
        performance_menu.click()

        configure_menu = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[text()='Configure']")))
        configure_menu.click()

        kpi_menu = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[text()='KPIs']")))
        kpi_menu.click()

        # Add a new KPI
        add_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".oxd-button--secondary")))
        add_button.click()

        job_title_dropdown = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".oxd-select-text-input")))
        job_title_dropdown.click()

        select_job_title = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[text()='Chief Executive Officer']")))
        select_job_title.click()

        kpi_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input.oxd-input")))
        kpi_input.send_keys("Increase Market Share")

        min_rating_input = driver.find_elements(By.CSS_SELECTOR, "input.oxd-input")[1]
        min_rating_input.send_keys("3")

        max_rating_input = driver.find_elements(By.CSS_SELECTOR, "input.oxd-input")[2]
        max_rating_input.send_keys("5")

        make_active_checkbox = driver.find_element(By.XPATH, "//label[text()='Make Default']/following-sibling::span")
        make_active_checkbox.click()

        save_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".oxd-button--secondary")))
        save_button.click()

        time.sleep(3)

    def test_verify_kpi_added(self):
        driver = self.driver
        wait = WebDriverWait(driver, 10)

        # Verify that the KPI was added successfully
        kpi_list = wait.until(EC.presence_of_element_located((By.XPATH, "//div[@class='oxd-table-card']/div[1]/div[2]")))

        assert "Increase Market Share" in kpi_list.text

    @classmethod
    def teardown_class(cls):
        cls.driver.quit()

if __name__ == "__main__":
    pytest.main()
