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
class TestDashboard:

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

    def test_dashboard_elements(self):
        driver = self.driver
        wait = WebDriverWait(driver, 10)

        self.login_as_admin()

        # Verify the presence of dashboard widgets
        widget1 = wait.until(EC.presence_of_element_located((By.ID, "widget1_id")))
        widget2 = wait.until(EC.presence_of_element_located((By.ID, "widget2_id")))
        widget3 = wait.until(EC.presence_of_element_located((By.ID, "widget3_id")))

        assert widget1.is_displayed()
        assert widget2.is_displayed()
        assert widget3.is_displayed()

    def test_dashboard_statistics(self):
        driver = self.driver
        wait = WebDriverWait(driver, 10)

        self.login_as_admin()

        # Verify the display of key statistics
        statistics_section = wait.until(EC.presence_of_element_located((By.ID, "statistics_section_id")))

        total_employees = wait.until(EC.presence_of_element_located((By.ID, "total_employees_id")))
        total_jobs = wait.until(EC.presence_of_element_located((By.ID, "total_jobs_id")))
        pending_requests = wait.until(EC.presence_of_element_located((By.ID, "pending_requests_id")))

        assert total_employees.is_displayed()
        assert total_jobs.is_displayed()
        assert pending_requests.is_displayed()

    def test_dashboard_charts(self):
        driver = self.driver
        wait = WebDriverWait(driver, 10)

        self.login_as_admin()

        # Verify the display of charts
        chart1 = wait.until(EC.presence_of_element_located((By.ID, "chart1_id")))
        chart2 = wait.until(EC.presence_of_element_located((By.ID, "chart2_id")))

        assert chart1.is_displayed()
        assert chart2.is_displayed()

    def test_interact_with_widgets(self):
        driver = self.driver
        wait = WebDriverWait(driver, 10)

        self.login_as_admin()

        # Click on a widget to interact with it
        widget1 = wait.until(EC.presence_of_element_located((By.ID, "widget1_id")))
        widget1.click()

        # Verify widget interaction
        interaction_result = wait.until(EC.presence_of_element_located((By.ID, "interaction_result_id")))
        assert interaction_result.is_displayed()

if __name__ == "__main__":
    pytest.main()
