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

class DirectoryPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def search_employee(self, name):
        search_box = self.wait.until(EC.presence_of_element_located((By.ID, "searchDirectory_emp_name_empName")))
        search_box.clear()
        search_box.send_keys(name)
        search_button = self.driver.find_element(By.ID, "searchBtn")
        search_button.click()

    def get_search_results(self):
        results = self.wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".resultsTable tbody tr")))
        return [result.text for result in results]

    def view_employee_details(self, employee_name):
        self.search_employee(employee_name)
        employee_link = self.wait.until(EC.presence_of_element_located((By.LINK_TEXT, employee_name)))
        employee_link.click()
        return self.wait.until(EC.presence_of_element_located((By.ID, "employeeDetails"))).is_displayed()

    def filter_employees_by_department(self, department):
        department_filter = self.wait.until(EC.presence_of_element_located((By.ID, "searchDirectory_job_title")))
        department_filter.select_by_visible_text(department)
        search_button = self.driver.find_element(By.ID, "searchBtn")
        search_button.click()

    def get_filtered_results(self):
        results = self.wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".resultsTable tbody tr")))
        return [result.text for result in results]

@pytest.mark.usefixtures("setup")
class TestDirectory:

    def test_search_employee(self):
        directory_page = DirectoryPage(self.driver)
        directory_page.search_employee("John Doe")
        results = directory_page.get_search_results()
        assert "John Doe" in results

    def test_view_employee_details(self):
        directory_page = DirectoryPage(self.driver)
        assert directory_page.view_employee_details("John Doe")

    def test_filter_employees_by_department(self):
        directory_page = DirectoryPage(self.driver)
        directory_page.filter_employees_by_department("IT")
        results = directory_page.get_filtered_results()
        assert any("IT" in result for result in results)

if __name__ == "__main__":
    pytest.main()
