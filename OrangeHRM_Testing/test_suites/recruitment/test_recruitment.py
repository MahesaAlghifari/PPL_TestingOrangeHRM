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

class RecruitmentPage:
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

    def navigate_to_recruitment(self):
        recruitment_menu = self.wait.until(EC.presence_of_element_located((By.ID, "menu_recruitment")))
        recruitment_menu.click()

    def add_job_vacancy(self, job_title, job_description):
        add_vacancy_button = self.wait.until(EC.presence_of_element_located((By.ID, "btnAddJobVacancy")))
        add_vacancy_button.click()
        title_field = self.wait.until(EC.presence_of_element_located((By.ID, "job_title")))
        title_field.send_keys(job_title)
        description_field = self.driver.find_element(By.ID, "job_description")
        description_field.send_keys(job_description)
        save_button = self.driver.find_element(By.ID, "btnSaveJobVacancy")
        save_button.click()

    def verify_job_vacancy_added(self, job_title):
        self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".oxd-alert-content-text")))
        search_box = self.wait.until(EC.presence_of_element_located((By.ID, "searchJobVacancy")))
        search_box.clear()
        search_box.send_keys(job_title)
        search_button = self.driver.find_element(By.ID, "searchBtn")
        search_button.click()
        results = self.wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".resultsTable tbody tr")))
        return any(job_title in result.text for result in results)

@pytest.mark.usefixtures("setup")
class TestRecruitment:

    def test_add_job_vacancy(self):
        recruitment_page = RecruitmentPage(self.driver)
        recruitment_page.login_as_admin()
        recruitment_page.navigate_to_recruitment()
        recruitment_page.add_job_vacancy("Software Engineer", "Responsible for developing and maintaining software applications.")
        assert recruitment_page.verify_job_vacancy_added("Software Engineer")

if __name__ == "__main__":
    pytest.main()
