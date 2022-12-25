from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, NoSuchWindowException

from webdriver_manager.chrome import ChromeDriverManager

from fake_useragent import UserAgent

import time
import re
import csv
from datetime import datetime


class ChromeDriver():    
    def __init__(self):
        user_agent = UserAgent(verify_ssl=False).random
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument(f'user-agent={user_agent}')
        chrome_options.add_experimental_option("detach", True)
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        self.driver.maximize_window()
        print("🔥 Start Instagram Comments Crawler")

    def get(self, url):
        try:
            print(f"🛫 Moving to 👉 {url}")
            self.driver.get(url)
        except:
            print("❌ Failed to get url. Check if url is correct")

    def close(self):
        self.driver.close()
    
    def move_to_login_page(self):
        login_url = "https://www.instagram.com/accounts/login/"
        self.get(login_url)
        self.driver.implicitly_wait(10)
        print("✅ Successfully moved to login page")
    
    def login_to_instagram(self, username, password):
        types = {'username': username, 'password': password}
        for type in types:
            input_css_selector = f'input[name="{type}"]'
            inputBox = self.driver.find_element(By.CSS_SELECTOR, input_css_selector)
            inputBox.send_keys(types[type])
            time.sleep(2)

        login_btn_css_selector = "button[type='submit']"
        login_btn = self.driver.find_element(By.CSS_SELECTOR, login_btn_css_selector)
        login_btn.click()
        time.sleep(3)
        
        try:
            error_css_selector = "#slfErrorAlert"
            self.driver.find_element(By.CSS_SELECTOR, error_css_selector)
        except NoSuchElementException:
            print("✅ Successfully Logged in to Instagram")
        else:
            print("❌ Failed to login. Please Relaunch Script File")
            self.driver.close()
            raise Exception("Failed to Login")

    def load_all_comments(self):
        more_comment_load_btn_css_selector = "ul.XQXOT > li button.wpO6b"
        count = 1
        
        print("✔️ Start Loading All Comments")
        try:
            while True:
                more_comment_load_btn = self.driver.find_element(By.CSS_SELECTOR, more_comment_load_btn_css_selector)
                if more_comment_load_btn:
                    more_comment_load_btn.click()
                    self.driver.implicitly_wait(5)
                    print(f'⏳ Click Count : {count}')
                    count += 1
        except:
            print("✅ Complete Loading All Comments")

    def load_all_replies(self):
        view_replies_css_selector = "span.EizgU"
        count = 1
        idx = 0

        print("✔️ Start Loading All Replies")

        try:
            view_replies_btns = self.driver.find_elements(By.CSS_SELECTOR, view_replies_css_selector)
            isRemained = True
            while isRemained:
                if "View" in view_replies_btns[idx].text:
                    view_replies_btns[idx].click()
                    print(f'⏳ Click Count : {count}')
                    count += 1
                    continue
                idx += 1
                if len(view_replies_btns) == idx:
                    isRemained = False
        except:
            print("❌ Something is failed.")
        else:
            print("✅ Complete Loading All Replies")

    def collect_comments(self):
        self.comments = {}
        
        comment_container_css_selector = "ul.Mr508 div.C4VMK"
        comment_writer_css_selector = comment_container_css_selector + " a.sqdOP"
        comment_content_css_selector = comment_container_css_selector + " > span"
        
        comment_containers = self.driver.find_elements(By.CSS_SELECTOR, comment_container_css_selector)

        print("✔️ Start Collecting All Comments")

        try:
            for comment in comment_containers:
                comment_writer = comment.find_element(By.CSS_SELECTOR, comment_writer_css_selector).text
                comment_content = comment.find_element(By.CSS_SELECTOR, comment_content_css_selector).text
                self.comments[comment_writer] = comment_content
        except:
            print("❌ Failed to Find Browser Element. Please Keep Browser Open.")
            raise NoSuchWindowException
        else:
            print("✅ Complete Collecting All Comments")

        try:
            self.filename = self.save_to_csv(self.comments)
        except:
            print("❌ Failed to Save All comments into CSV file")
            raise Exception('Failed to Saving CSV file')
        else:
            print(f"✅ Successfully All Comments Saved to {self.filename}")


    def filter_comments(self):
        self.__answer_list = []
        student_id_regex = re.compile('(^6020\d+)')
        answer_regex = re.compile('8\D')

        print("🤔 Checking All Answers and Student ID")
        for writer, content in self.comments.items():
            isEligibleStudentId = student_id_regex.search(content)
            isCorrectAnswer = answer_regex.search(content)
            if isEligibleStudentId and isCorrectAnswer:
                std_id = isEligibleStudentId.group()
                self.__answer_list.append({"std_id": std_id, "writer": writer, "content": content})
        
        print("✅ Complete Checking All Comments")

    def get_answer_list(self):
        return self.__answer_list

    def save_to_csv(self, dict):
        now = datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
        filename = f'comments_{now}.csv'

        f = open(filename, 'w', newline='')
        wr = csv.writer(f)
        for idx, (writer, content) in enumerate(dict.items()):
            wr.writerow([idx + 1, writer, content.replace('\n', ' ')])
        f.close()

        return filename