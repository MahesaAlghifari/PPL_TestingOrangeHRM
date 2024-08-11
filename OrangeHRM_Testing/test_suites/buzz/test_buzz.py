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
class TestBuzz:

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

    def test_create_new_post(self):
        driver = self.driver
        wait = WebDriverWait(driver, 10)

        self.login_as_admin()

        # Navigate to Buzz
        buzz_menu = wait.until(EC.presence_of_element_located((By.ID, "menu_buzz_viewBuzz")))
        buzz_menu.click()

        # Click on 'Add Post'
        add_post_button = wait.until(EC.presence_of_element_located((By.ID, "btnAddPost")))
        add_post_button.click()

        # Enter post content
        post_content = wait.until(EC.presence_of_element_located((By.ID, "postContent")))
        post_content.send_keys("This is a test post!")

        # Click 'Save' button
        save_button = driver.find_element(By.ID, "btnSavePost")
        save_button.click()

        # Optional fixed delay
        time.sleep(2)

        # Verify post is created
        post_message = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".post-content-text")))
        assert "This is a test post!" in post_message.text

    def test_like_post(self):
        driver = self.driver
        wait = WebDriverWait(driver, 10)

        self.login_as_admin()

        # Navigate to Buzz
        buzz_menu = wait.until(EC.presence_of_element_located((By.ID, "menu_buzz_viewBuzz")))
        buzz_menu.click()

        # Like the first post
        like_button = wait.until(EC.presence_of_element_located((By.XPATH, "//table[@id='buzz_table']//button[@class='like-btn']")))
        like_button.click()

        # Optional fixed delay
        time.sleep(2)

        # Verify post is liked
        like_count = wait.until(EC.presence_of_element_located((By.XPATH, "//table[@id='buzz_table']//button[@class='like-btn']/span")))
        assert int(like_count.text) > 0

    def test_view_post_details(self):
        driver = self.driver
        wait = WebDriverWait(driver, 10)

        self.login_as_admin()

        # Navigate to Buzz
        buzz_menu = wait.until(EC.presence_of_element_located((By.ID, "menu_buzz_viewBuzz")))
        buzz_menu.click()

        # Click on the first post to view details
        first_post = wait.until(EC.presence_of_element_located((By.XPATH, "//table[@id='buzz_table']//tr[1]//a")))
        first_post.click()

        # Verify post details are visible
        post_details = wait.until(EC.presence_of_element_located((By.ID, "postDetails")))
        assert post_details.is_displayed()

if __name__ == "__main__":
    pytest.main()
