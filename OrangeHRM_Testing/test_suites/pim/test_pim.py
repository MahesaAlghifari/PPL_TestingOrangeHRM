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

@pytest.mark.usefixtures("setup")
class TestPIM:

    def login_as_admin(self):
        driver = self.driver
        wait = WebDriverWait(driver, 10)

        # Login as admin
        username_field = wait.until(EC.presence_of_element_located((By.NAME, "username")))
        username_field.send_keys("admin")

        password_field = driver.find_element(By.NAME, "password")
        password_field.send_keys("admin123")

        login_button = driver.find_element(By.CSS_SELECTOR, ".oxd-button")
        login_button.click()

        # Wait until dashboard is loaded
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".oxd-topbar-header-breadcrumb-module")))

        # Optional fixed delay
        time.sleep(2)

    def test_add_employee(self):
        driver = self.driver
        wait = WebDriverWait(driver, 10)

        self.login_as_admin()

        # Navigate to the PIM module
        pim_menu = wait.until(EC.presence_of_element_located((By.ID, "menu_pim_viewPimModule")))
        pim_menu.click()

        # Click on 'Add Employee'
        add_employee_button = wait.until(EC.presence_of_element_located((By.ID, "menu_pim_addEmployee")))
        add_employee_button.click()

        # Fill out the employee form
        first_name = wait.until(EC.presence_of_element_located((By.NAME, "firstName")))
        first_name.send_keys("John")

        last_name = driver.find_element(By.NAME, "lastName")
        last_name.send_keys("Doe")

        employee_id = driver.find_element(By.NAME, "employeeId")
        employee_id.send_keys("12345")

        save_button = driver.find_element(By.ID, "btnSave")
        save_button.click()

        # Optional fixed delay
        time.sleep(2)

        # Verify employee is added
        success_message = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".oxd-alert-content-text")))
        assert "Successfully Saved" in success_message.text

    def test_edit_employee(self):
        driver = self.driver
        wait = WebDriverWait(driver, 10)

        self.login_as_admin()

        # Navigate to the PIM module
        pim_menu = wait.until(EC.presence_of_element_located((By.ID, "menu_pim_viewPimModule")))
        pim_menu.click()

        # Search for an employee
        employee_name = wait.until(EC.presence_of_element_located((By.ID, "empsearch_employee_name_empName")))
        employee_name.send_keys("John Doe")

        search_button = driver.find_element(By.ID, "searchBtn")
        search_button.click()

        # Click on the employee record
        employee_record = wait.until(EC.presence_of_element_located((By.XPATH, "//a[contains(text(),'John Doe')]")))
        employee_record.click()

        # Click on 'Edit'
        edit_button = wait.until(EC.presence_of_element_located((By.ID, "btnSave")))
        edit_button.click()

        # Modify employee details
        middle_name = driver.find_element(By.NAME, "middleName")
        middle_name.send_keys("A")

        save_button = driver.find_element(By.ID, "btnSave")
        save_button.click()

        # Optional fixed delay
        time.sleep(2)

        # Verify employee details are updated
        success_message = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".oxd-alert-content-text")))
        assert "Successfully Saved" in success_message.text

    def test_view_employee(self):
        driver = self.driver
        wait = WebDriverWait(driver, 10)

        self.login_as_admin()

        # Navigate to the PIM module
        pim_menu = wait.until(EC.presence_of_element_located((By.ID, "menu_pim_viewPimModule")))
        pim_menu.click()

        # Search for an employee
        employee_name = wait.until(EC.presence_of_element_located((By.ID, "empsearch_employee_name_empName")))
        employee_name.send_keys("John Doe")

        search_button = driver.find_element(By.ID, "searchBtn")
        search_button.click()

        # Click on the employee record
        employee_record = wait.until(EC.presence_of_element_located((By.XPATH, "//a[contains(text(),'John Doe')]")))
        employee_record.click()

        # Optional fixed delay
        time.sleep(2)

        # Verify employee details are visible
        employee_details = wait.until(EC.presence_of_element_located((By.ID, "profile-pic")))
        assert employee_details.is_displayed()

if __name__ == "__main__":
    pytest.main()
