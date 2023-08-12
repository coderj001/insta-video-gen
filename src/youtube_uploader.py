import os
import time

from selenium import webdriver
from selenium.webdriver.common.by import By

from src.settings import settings
from src.utils import download_chromedriver


class YouTubeUploader:
    def __init__(self):
        self.username = settings.your_youtube_username
        self.password = settings.your_youtube_password
        self.check_chromedriver()
        options = webdriver.ChromeOptions()
        self.driver = webdriver.Chrome(options=options)

    def check_chromedriver(self):
        if not os.path.exists(os.path.join(settings.base_dir, 'chromedriver')):
            print("ChromeDriver not found. Downloading now...")
            # Assuming this is the function you wrote to download ChromeDriver
            download_chromedriver()

    def login(self):
        self.driver.get('https://www.youtube.com')
        self.driver.find_element(By.LINK_TEXT, 'Sign in').click()
        time.sleep(2)
        self.driver.find_element(
            By.ID, 'identifierId').send_keys(self.username)
        self.driver.find_element(By.ID, 'identifierNext').click()
        time.sleep(5)
        self.driver.find_element(By.NAME, 'password').send_keys(self.password)
        self.driver.find_element(By.ID, 'passwordNext').click()
        time.sleep(5)

    def upload_video(self, video_path, title, description, tags):
        self.driver.find_element(
            By.CSS_SELECTOR,
            'button[aria-label="Create"]'
        ).click()
        time.sleep(2)
        self.driver.find_element(By.LINK_TEXT, 'Upload video').click()
        time.sleep(2)
        self.driver.find_element(
            By.CSS_SELECTOR, 'input[type="file"]').send_keys(video_path)
        time.sleep(5)
        self.driver.find_element(By.NAME, 'title').send_keys(title)
        self.driver.find_element(By.NAME, 'description').send_keys(description)
        self.driver.find_element(By.NAME, 'tags').send_keys(','.join(tags))
        time.sleep(2)
        self.driver.find_element(
            By.CSS_SELECTOR, 'button[aria-label="Publish"]').click()
        time.sleep(5)

    def close(self):
        self.driver.quit()
