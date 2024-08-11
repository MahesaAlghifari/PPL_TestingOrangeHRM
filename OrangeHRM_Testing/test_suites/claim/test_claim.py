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
class TestClaim:

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

    def test_create_new_claim(self):
        driver = self.driver
        wait = WebDriverWait(driver, 10)

        self.login_as_admin()

        # Navigate to the Claims page
        claim_menu = wait.until(EC.presence_of_element_located((By.ID, "menu_claim")))
        claim_menu.click()

        # Click on 'Add Claim'
        add_claim_button = wait.until(EC.presence_of_element_located((By.ID, "btnAddClaim")))
        add_claim_button.click()

        # Fill out the claim form
        claim_type = wait.until(EC.presence_of_element_located((By.ID, "claim_type")))
        claim_type.send_keys("Travel")

        claim_amount = driver.find_element(By.ID, "claim_amount")
        claim_amount.send_keys("100")

        save_button = driver.find_element(By.ID, "btnSaveClaim")
        save_button.click()

        # Verify claim is added
        claim_success_message = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".oxd-alert-content-text")))
        assert "Claim added successfully" in claim_success_message.text

    def test_approve_claim(self):
        driver = self.driver
        wait = WebDriverWait(driver, 10)

        self.login_as_admin()

        # Navigate to the Claims page
        claim_menu = wait.until(EC.presence_of_element_located((By.ID, "menu_claim")))
        claim_menu.click()

        # Approve the first claim in the list
        first_claim_checkbox = wait.until(EC.presence_of_element_located((By.XPATH, "//table[@id='claims_table']//input[@type='checkbox']")))
        first_claim_checkbox.click()

        approve_button = driver.find_element(By.ID, "btnApproveClaim")
        approve_button.click()

        # Verify claim is approved
        approve_success_message = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".oxd-alert-content-text")))
        assert "Claim approved successfully" in approve_success_message.text

    def test_view_claim_history(self):
        driver = self.driver
        wait = WebDriverWait(driver, 10)

        self.login_as_admin()

        # Navigate to the Claims page
        claim_menu = wait.until(EC.presence_of_element_located((By.ID, "menu_claim")))
        claim_menu.click()

        # View claim history
        history_button = wait.until(EC.presence_of_element_located((By.ID, "btnViewHistory")))
        history_button.click()

        # Verify history page is loaded
        history_table = wait.until(EC.presence_of_element_located((By.ID, "history_table")))
        assert history_table.is_displayed()

if __name__ == "__main__":
    pytest.main()
