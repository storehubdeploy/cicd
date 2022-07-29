#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

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
    def __init__(self):
        self.url = sys.argv[1]
        self.today = datetime.datetime.now().strftime("%Y-%m-%d")
        self.increases = [1, 2, 5, 10, 20, 50, 100]
        self.recipient = self.getApolloConfig()

        self.driver = Automation.firefoxDriver(self)
        self.wait = WebDriverWait(self.driver, 60)


    def getApolloConfig(self):
        url = "http://apollo-pro.shub.us"
        appid = "rnpos-pipeline"
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
            return "t_5021833814548561"


    def firefoxDriver(self):
        driver_path = "/Users/shbuild/jenkins/workspace/mobile/Android/RN-POS_Phase_Release_Automation/geckodriver"

        # init
        options = webdriver.FirefoxOptions()
        # options.add_argument("-headless")  # Windowless mode
        options.set_preference('browser.link.open_newwindow', '3')
        options.set_preference('permissions.default.image', 2)  # no pictures mode

        profile = webdriver.FirefoxProfile(r"/Users/shbuild/Library/Application Support/Firefox/Profiles/f9rkhimy.default-release")
        profile.set_preference("dom.webdriver.enabled", False)
        profile.set_preference('useAutomationExtension', False)
        profile.update_preferences()
        desired = DesiredCapabilities.FIREFOX

        # Open website
        driver = webdriver.Firefox(executable_path=driver_path, options=options, firefox_profile=profile, desired_capabilities=desired)

        print("\n{} \n>>> Creating firefox driver success.".format(self.today))
        return driver


    def getFirebaseValues(self):
        print("\n>>> Opening firebase website. ")
        self.driver.get(self.url)

        try:
            # self.wait.until(ec.presence_of_element_located(('css selector', 'div.summary-chip:nth-child(5) > div:nth-child(2)')))
            time.sleep(8)
            release_name = self.driver.find_element("css selector", '.fire-feature-bar-title')

            self.wait.until(ec.presence_of_element_located(('css selector', 'div.summary-chip:nth-child(5) > div:nth-child(2)')))
            distributions = self.driver.find_element("css selector", 'div.summary-chip:nth-child(5) > div:nth-child(2)').text
        except:
            self.wait.until(ec.presence_of_element_located(('css selector', '.VfPpkd-RLmnJb')))
            self.driver.find_element("css selector", '.VfPpkd-LgbsSe').click()
            time.sleep(2)
            self.driver.find_element("css selector", '#password > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > input:nth-child(1)').send_keys(CONSTANTS.GOOGLE_PWD, Keys.ENTER)
            self.wait.until(ec.presence_of_element_located(('css selector', 'div.summary-chip:nth-child(5) > div:nth-child(2)')))

            release_name = self.driver.find_element("css selector", '.fire-feature-bar-title').text
            distributions = self.driver.find_element("css selector", 'div.summary-chip:nth-child(5) > div:nth-child(2)').text

            print("==> Login has expired, this will not affect the normal release, but please update in time！！")

        # get distribution value
        str_index = distributions.find("%")
        distribution = distributions[0:str_index].strip()

        # print(release_name, distribution)

        return release_name, distribution


    def firebaseAuto(self):
        time.sleep(1)
        self.driver.find_element('css selector', 'button.mat-menu-trigger:nth-child(1)').click()
        self.driver.find_element('css selector', '.increase-distribution-button').click()

        prenu = self.driver.find_element('css selector', 'input.ng-pristine').get_attribute('value')

        index = self.increases.index(int(prenu))
        nownu = self.increases[index+1]

        time.sleep(2)
        self.driver.find_element('css selector', 'input.ng-pristine').clear()
        self.driver.find_element('css selector', 'input.ng-pristine').send_keys(nownu)

        time.sleep(2)
        self.driver.find_element('css selector', '.send-button').click()

        # waiting for operating before
        self.wait.until_not(ec.presence_of_element_located(('css selector', '.send-button')))

        return nownu


    def jenkinsAuto(self):
        print("\n>>> Opening jenkins website. ")
        self.driver.get('https://jenkins.shub.us/job/mobile/job/Android/job/RN-POS_Phase_Release_Automation/configure')

        # start opration
        self.wait.until(ec.presence_of_element_located(("css selector", '#j_username')))
        self.driver.find_element("css selector", '#j_username').send_keys(CONSTANTS.JENKINS_USER)
        self.driver.find_element("css selector", 'div.formRow:nth-child(2) > input:nth-child(1)').send_keys(CONSTANTS.JENKINS_PASSWORD)
        self.driver.find_element("css selector", '.submit-button').click()

        # auto-run stop/start
        self.wait.until(ec.presence_of_element_located(("css selector", '#cb32')))
        self.driver.find_element("css selector", '#cb32').send_keys(Keys.SPACE)
        time.sleep(2)

        # set default value
        if auto_run == "true" and terminate == "false":
            # enter run time
            self.driver.find_element("css selector", 'div.config_general:nth-child(11) > div:nth-child(4) > div:nth-child(4) > div:nth-child(1) > div:nth-child(2) > textarea:nth-child(1)').send_keys("0 9 * * *")

            # change default url
            selector1 = self.driver.find_element("css selector", 'div.repeated-chunk:nth-child(2) > div:nth-child(1) > div:nth-child(4) > div:nth-child(2) > input:nth-child(1)')
            selector1.clear()
            selector1.send_keys(self.url)

            time.sleep(1)
            # change jenkins job status
            selector2 = self.driver.find_element("css selector", 'div.hetero-list-container:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(4) > div:nth-child(2) > textarea:nth-child(1)')
            selector2.clear()
            selector2.send_keys("Running")
        elif terminate == "true" or nownu == 100:
            # change jenkins job status
            selector1 = self.driver.find_element("css selector", 'div.hetero-list-container:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(4) > div:nth-child(2) > textarea:nth-child(1)')
            selector1.clear()
            selector1.send_keys("Stopped")

        # save
        time.sleep(1)
        self.driver.find_element("xpath", "//button[text()='Save' and @type='button']").click()
        self.wait.until_not(ec.presence_of_element_located(("xpath", "//button[text()='Save' and @type='button']")))


    def text(self, action, release_name, distribution, url):
        text = '''Date: {}\nAction: {}\nRelease: {}\nCurrent Stage: {}%\nURL: {}'''.format(self.today, action, release_name, distribution, url)

        return text


    def send_message(self,text):
        if 't_' in self.recipient:
            thread_type = "thread_key"
        else:
            thread_type = "id"

        data = {
            "recipient": {thread_type: self.recipient},
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
            print('recipient:' + self.recipient)
            print('text:' + text)
            print(str(e))
            return e
        else:
            return r.json()


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


if __name__ == '__main__':
    auto = Automation()

    auto_run = sys.argv[2]
    terminate = sys.argv[3]
    auto_status = sys.argv[4]

    today_work, tomorrow_work = auto.dateJudgement()
    release_name, distribution = auto.getFirebaseValues()

    if auto_run == "true" and terminate == "false" and auto_status == "Stopped":
        if int(distribution) == 100:
            action = '"Increase distribution" had already updated to 100%. Auto-run start faild.'
            text = auto.text(action, release_name, distribution, auto.url)

            print(text)
            auto.send_message(text)
        elif int(distribution) not in [1, 2, 5, 10, 20, 50]:
            action = '"Increase distribution"({}) is not in [1%, 2%, 5%, 10%, 20%, 50%]. Auto-run start faild.'.format(distribution)
            text = auto.text(action, release_name, distribution, auto.url)

            print(text)
            auto.send_message(text)
        else:
            auto.jenkinsAuto()  # main
            auto.driver.quit()

            action = "Auto-run mode started."
            text = auto.text(action, release_name, distribution, auto.url)

            print(text)
            auto.send_message(text)

    elif terminate == "true" and auto_status == "Running":
        auto.jenkinsAuto()  # main
        auto.driver.quit()

        action = "Auto-run mode stopped, because of manual termination."
        text = auto.text(action, release_name, distribution, auto.url)

        print(text)
        auto.send_message(text)

    elif auto_run == "false" and terminate == "false":
        if today_work and auto_status == "Running": # auto or manual run once
            if int(distribution) == 50 and tomorrow_work == False:
                auto.driver.quit()
                action = "Today is last workday, not updating to 100%."
                text = auto.text(action, release_name, distribution, auto.url)

                print(text)
                auto.send_message(text)
            else:
                nownu = auto.firebaseAuto()

                if int(nownu) == 100:
                    auto.jenkinsAuto()
                    auto.driver.quit()

                    action = 'Auto-run mode stopped. "Increase distribution" update to 100% today.'
                    text = auto.text(action, release_name, 100, auto.url)

                    print(text)
                    auto.send_message(text)
                else:
                    auto.driver.quit()
                    action = 'Increase phase stage.'
                    text = auto.text(action, release_name, nownu, auto.url)

                    print(text)
                    auto.send_message(text)
        elif auto_status == "Stopped": # manual run once
            if int(distribution) == 100:
                auto.driver.quit()

                action = '"Increase distribution" had already updated to 100%. Manual execution failed.'
                text = auto.text(action, release_name, distribution, auto.url)

                print(text)
                auto.send_message(text)
            else:
                nownu = auto.firebaseAuto()

                auto.driver.quit()
                action = 'Increase phase stage by manual update.'
                text = auto.text(action, release_name, nownu, auto.url)

                print(text)
                auto.send_message(text)
        else:
            auto.driver.quit()
            print("\nToday({}) is holiday or last workday, not running automation. \nCurrent Stage: {}%".format(auto.today, distribution))
    else:
        auto.driver.quit()
        print("Illegal operation, please check the status of the Jenkins job.\nJenkins auto_run status : ", auto_status)
        text = "Action: Illegal operation, please check the status of the Jenkins job.\nJenkins job status: {} \nCurrent Stage: {}%".format(auto_status, distribution)
        auto.send_message(text)



