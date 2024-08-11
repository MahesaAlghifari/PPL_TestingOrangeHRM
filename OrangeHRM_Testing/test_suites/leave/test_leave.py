import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
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

class LeavePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def login_as_admin(self):
        username_field = self.wait.until(EC.presence_of_element_located((By.NAME, "username")))
        username_field.send_keys("admin")
        password_field = self.driver.find_element(By.NAME, "password")
        password_field.send_keys("admin123")
        login_button = self.driver.find_element(By.CSS_SELECTOR, ".oxd-button")
        login_button.click()
        self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".oxd-topbar-header-breadcrumb-module")))

    def navigate_to_leave(self):
        leave_menu = self.wait.until(EC.presence_of_element_located((By.ID, "menu_leave")))
        leave_menu.click()

    def apply_leave(self, leave_type, leave_from, leave_to, leave_comment):
        apply_leave_button = self.wait.until(EC.presence_of_element_located((By.ID, "btnApplyLeave")))
        apply_leave_button.click()
        leave_type_dropdown = self.wait.until(EC.presence_of_element_located((By.ID, "leave_type")))
        leave_type_dropdown.send_keys(leave_type)
        from_date_field = self.driver.find_element(By.ID, "leave_from")
        from_date_field.send_keys(leave_from)
        to_date_field = self.driver.find_element(By.ID, "leave_to")
        to_date_field.send_keys(leave_to)
        comment_field = self.driver.find_element(By.ID, "leave_comment")
        comment_field.send_keys(leave_comment)
        save_button = self.driver.find_element(By.ID, "btnSaveLeave")
        save_button.click()

    def verify_leave_application(self, leave_type, leave_from):
        self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".oxd-alert-content-text")))
        search_box = self.wait.until(EC.presence_of_element_located((By.ID, "searchLeave")))
        search_box.clear()
        search_box.send_keys(leave_type)
        search_button = self.driver.find_element(By.ID, "searchBtn")
        search_button.click()
        results = self.wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".resultsTable tbody tr")))
        return any(leave_type in result.text and leave_from in result.text for result in results)

@pytest.mark.usefixtures("setup")
class TestLeave:

    def test_apply_leave(self):
        leave_page = LeavePage(self.driver)
        leave_page.login_as_admin()
        leave_page.navigate_to_leave()
        leave_page.apply_leave("Sick Leave", "2024-08-15", "2024-08-17", "Sick leave due to illness.")
        assert leave_page.verify_leave_application("Sick Leave", "2024-08-15")

if __name__ == "__main__":
    pytest.main()
