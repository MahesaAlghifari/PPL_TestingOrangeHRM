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
class TestMyInfo:

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

    def test_update_personal_details(self):
        driver = self.driver
        wait = WebDriverWait(driver, 10)

        self.login_as_admin()

        # Navigate to My Info
        my_info_menu = wait.until(EC.presence_of_element_located((By.ID, "menu_pim_viewMyDetails")))
        my_info_menu.click()

        # Click on 'Edit'
        edit_button = wait.until(EC.presence_of_element_located((By.ID, "btnSave")))
        edit_button.click()

        # Update personal details
        middle_name = driver.find_element(By.NAME, "middleName")
        middle_name.clear()
        middle_name.send_keys("A")

        save_button = driver.find_element(By.ID, "btnSave")
        save_button.click()

        # Optional fixed delay
        time.sleep(2)

        # Verify personal details are updated
        success_message = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".oxd-alert-content-text")))
        assert "Successfully Saved" in success_message.text

    def test_change_profile_picture(self):
        driver = self.driver
        wait = WebDriverWait(driver, 10)

        self.login_as_admin()

        # Navigate to My Info
        my_info_menu = wait.until(EC.presence_of_element_located((By.ID, "menu_pim_viewMyDetails")))
        my_info_menu.click()

        # Click on 'Edit' to change profile picture
        edit_button = wait.until(EC.presence_of_element_located((By.ID, "btnSave")))
        edit_button.click()

        # Click on 'Change Picture'
        change_picture_button = wait.until(EC.presence_of_element_located((By.ID, "uploadPic")))
        change_picture_button.click()

        # Upload a new profile picture
        upload_input = driver.find_element(By.NAME, "photofile")
        upload_input.send_keys("/path/to/new/profile-picture.jpg")  # Adjust path as needed

        save_button = driver.find_element(By.ID, "btnSave")
        save_button.click()

        # Optional fixed delay
        time.sleep(2)

        # Verify profile picture is updated
        profile_picture = wait.until(EC.presence_of_element_located((By.ID, "profile-pic")))
        assert profile_picture.is_displayed()

    def test_view_personal_information(self):
        driver = self.driver
        wait = WebDriverWait(driver, 10)

        self.login_as_admin()

        # Navigate to My Info
        my_info_menu = wait.until(EC.presence_of_element_located((By.ID, "menu_pim_viewMyDetails")))
        my_info_menu.click()

        # Verify personal information is visible
        personal_info_section = wait.until(EC.presence_of_element_located((By.ID, "personal_details")))
        assert personal_info_section.is_displayed()

if __name__ == "__main__":
    pytest.main()
