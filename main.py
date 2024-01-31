from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
import os
from selenium.webdriver.support.ui import Select


class ProjectChanger:

    def __init__(self):
        self.service = ChromeService(executable_path=ChromeDriverManager().install())
        self.project_changer_driver = webdriver.Chrome(service=self.service)
        self.project_changer_driver.implicitly_wait(15)
        self.login_to_trieste()

    def login_to_trieste(self):
        print("Logging in to Trieste...")
        self.project_changer_driver.get("http://trieste.io")
        trieste_username = self.project_changer_driver.find_element(By.ID, "user_email")
        trieste_password = self.project_changer_driver.find_element(By.ID, "user_password")
        login_submit_button = self.project_changer_driver.find_element(By.NAME, "commit")

        trieste_username.send_keys(os.environ.get("TRIESTE_USERNAME"))
        trieste_password.send_keys(os.environ.get("TRIESTE_PASSWORD"))
        login_submit_button.click()

    def change_project(self, lead_url, new_project):
        self.project_changer_driver.get(lead_url)
        move_link = self.project_changer_driver.find_element(By.LINK_TEXT, "Move")
        move_link.click()

        # select project from drop down list, click "move"
        project_dropdown_list = Select(self.project_changer_driver.find_element(By.ID, "site_link[site_id]"))
        project_dropdown_list.select_by_visible_text(new_project)
        move_button = self.project_changer_driver.find_element(By.NAME, "commit")
        move_button.click()
        print(f"{lead_url} project changed to {new_project}")



new_project = "prilla.com - active"

lead_url_list = []

user_input_lead_url = input("Paste keywords here (1 keyword(s) per line): ")
# allow user to input urls, 1 line per url

while user_input_lead_url != '':
    lead_url_list.append(user_input_lead_url)
    user_input_lead_url = input()

project_changer = ProjectChanger()

for url in lead_url_list:
    project_changer.change_project(lead_url=url, new_project=new_project)

input("Continue?")
