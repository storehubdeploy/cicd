import datetime
import json
import sys
import time

import requests
from chinese_calendar import is_workday
from selenium import webdriver
from selenium.webdriver import DesiredCapabilities, Keys
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait
import ci_constants as CONSTANTS

class Automation(object):
    def __init__(self, url, auto_run, terminate, auto_status, driver_path, login_cookie, jenkins_url):
        print(">>> Default values ...")
        self.url = url
        self.auto_run = auto_run
        self.terminate = terminate
        self.auto_status = auto_status
        self.driver_path = driver_path
        self.login_cookie = login_cookie
        self.jenkins_url = jenkins_url

        self.today = datetime.datetime.now().strftime("%Y-%m-%d")

        # 创建driver
        self.driver = Automation.firefoxDriver(self)

        # 设置超时时间
        self.wait = WebDriverWait(self.driver, 40)


    def getApolloConfig(self):
        url = "http://apollo-pro.shub.us"
        appid = "beep-pipeline"
        cluster = "default"
        namespace = "application"

        try:
            r = requests.get("{0}/configfiles/json/{1}/{2}/{3}".format(url, appid, cluster, namespace))
            if r.status_code == 200:
                for k, v in r.json().items():
                    if k == "PHASE_RELEASE_GROUP":
                        return v
                    else:
                        print("\n>>> Can not get workplace 'PHASE_RELEASE_GROUP'. ")
        except:
            # Guaranteed to run successfully, resolve apollo outages
            print(">>> Failed to get appllo configuration, using default configuration.")
            return "t_5917367818355022"


    def firefoxDriver(self):
        options = webdriver.FirefoxOptions()
        # options.add_argument("-headless")  # Windowless mode
        options.set_preference('browser.link.open_newwindow', '3')
        options.set_preference('permissions.default.image', 2)  # no pictures mode

        profile = webdriver.FirefoxProfile(self.login_cookie)
        profile.set_preference("dom.webdriver.enabled", False)
        profile.set_preference('useAutomationExtension', False)
        profile.update_preferences()
        desired = DesiredCapabilities.FIREFOX

        # Open website
        driver = webdriver.Firefox(executable_path=self.driver_path, options=options, firefox_profile=profile, desired_capabilities=desired)

        print("\n{} \n>>> Creating firefox driver success.".format(self.today))
        return driver


    # 获取release当前状态
    def getPhaseStatus(self):
        print(">>> Get phase stage status...")
        self.driver.get(self.url)

        try:
            self.wait.until(ec.presence_of_element_located(("css selector", ".page-header > div:nth-child(1) > div:nth-child(1)")))
        except:
            self.wait.until(ec.presence_of_element_located(("xpath", "//span[contains(@class, 'VfPpkd') and text()='Next']")))

            self.driver.find_element("xpath", "//span[contains(@class, 'VfPpkd') and text()='Next']").click()
            time.sleep(2)
            self.driver.find_element("css selector", '#password > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > input:nth-child(1)').send_keys(CONSTANTS.GOOGLE_PWD, Keys.ENTER)

            print("\n==> Login has expired, this will not affect the normal release, but please update in time！！")

        self.wait.until(ec.presence_of_element_located(("css selector", ".page-header > div:nth-child(1) > div:nth-child(1)")))

        stage_note = self.driver.find_element("css selector", "simple-html.text-line:nth-child(2) > span:nth-child(1)").text
        release_name = self.driver.find_element("css selector", ".page-header > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > simple-html:nth-child(1) > span:nth-child(1)").text
        time.sleep(3)
        if stage_note == "Available on Google Play":
            current_stage = "100%"
        else:
            current_stage = self.driver.find_element("xpath", "//console-scorecard[@debug-id='rollout-percentage-scorecard']/div[2]/div[contains(@class,'row _ngcontent')]/span").text.replace(" ", "")

        return release_name, current_stage[:-1]


    # 修改phase stage
    def changePhase(self, new_stage):
        print(">>> Change phase...")
        self.driver.find_element("xpath", "//material-button[@debug-id='update-rollout-button']").click()
        stage = self.driver.find_element("xpath", "//material-input[@debug-id='rollout-percentage-input']/label/input")

        stage.clear()
        stage.send_keys(new_stage)

        time.sleep(3)
        #self.driver.find_element("xpath", "//material-button[@debug-id='cancel-button']").click()  # change！！！
        self.driver.find_element("xpath", "//material-button[@debug-id='confirm-button']").click() # Commit Change

        time.sleep(2)
        if new_stage == 100:
            return True
        else:
            return False


    # 修改jenkins状态
    def jenkinsLogin(self):
        print(">>> Change jenkins...")
        self.driver.get(self.jenkins_url)

        # jenkins login
        self.wait.until(ec.presence_of_element_located(("css selector", '#j_username')))
        self.driver.find_element("css selector", '#j_username').send_keys(CONSTANTS.JENKINS_USER)
        time.sleep(1)
        self.driver.find_element("css selector", 'div.formRow:nth-child(2) > input:nth-child(1)').send_keys(CONSTANTS.JENKINS_PASSWORD)
        self.driver.find_element("css selector", '.submit-button').click()


    def changeJenkins(self, stage_over):
        self.jenkinsLogin()

        self.wait.until(ec.presence_of_element_located(("css selector", '#cb32')))
        self.driver.find_element("css selector", '#cb32').send_keys(Keys.SPACE)
        time.sleep(2)

        if self.auto_run == "true":
            # autorun time
            self.driver.find_element("css selector", 'div.config_general:nth-child(11) > div:nth-child(4) > div:nth-child(4) > div:nth-child(1) > div:nth-child(2) > textarea:nth-child(1)').send_keys("10 9 * * *")

            # change default url
            selector1 = self.driver.find_element("css selector", 'div.repeated-chunk:nth-child(2) > div:nth-child(1) > div:nth-child(4) > div:nth-child(2) > input:nth-child(1)')
            selector1.clear()
            selector1.send_keys(self.url)

            time.sleep(1)
            # change jenkins job status
            selector2 = self.driver.find_element("css selector", 'div.hetero-list-container:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(4) > div:nth-child(2) > textarea:nth-child(1)')
            selector2.clear()
            selector2.send_keys("Running")

            print(">>> Jenkins autoRun Started...")
        elif self.terminate == "true" or stage_over:
            # change jenkins job status
            selector1 = self.driver.find_element("css selector", 'div.hetero-list-container:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(4) > div:nth-child(2) > textarea:nth-child(1)')
            selector1.clear()
            selector1.send_keys("Stopped")

            print(">>> Jenkins autoRun Stopped...")

        # save
        time.sleep(1)
        self.driver.find_element("xpath", "//button[text()='Save' and @type='button']").click()
        self.wait.until_not(ec.presence_of_element_located(("xpath", "//button[text()='Save' and @type='button']")))


    # 工作日判定
    def dateJudgement(self):
        year = datetime.datetime.now().strftime("%Y")
        mouth = datetime.datetime.now().strftime("%m")
        day = datetime.datetime.now().strftime("%d")

        t_mouth = (datetime.datetime.now() + datetime.timedelta(days=1)).strftime("%m")
        t_day = (datetime.datetime.now() + datetime.timedelta(days=1)).strftime("%d")

        date_now = datetime.date(int(year),int(mouth),int(day))
        tomorrow = datetime.date(int(year),int(t_mouth),int(t_day))

        today_work = is_workday(date_now)
        tomorrow_work = is_workday(tomorrow)

        return today_work, tomorrow_work


    def text(self, action, release_name, current_stage, phase_url):
        text = '''Date: {}\nAction: {}\nRelease: {}\nCurrent Stage: {}%\nURL: {}'''.format(self.today, action, release_name, current_stage, phase_url)
        print(text)

        return text


    def send_message(self, recipient, text):
        if 't_' in recipient:
            thread_type = "thread_key"
        else:
            thread_type = "id"

        data = {
            "recipient": {thread_type: recipient},
            "message": {
                "text": text,
            },
        }

        post_data = json.dumps(data)
        url = CONSTANTS.WORKPLACE_URL
        headers = {'Content-Type': 'application/json'}
        payload = {'access_token': CONSTANTS.WORKPLACE_TOKEN}

        try:
            r = requests.post(url, headers=headers, params=payload, data=post_data)
            r.raise_for_status()
            print("\n>>> Message sent success! ")
        except requests.RequestException as e:
            print('recipient:' + recipient)
            print('text:' + text)
            print(str(e))
            return e
        else:
            return r.json()

