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
        self.increases = [1, 2, 5, 10, 20, 50, 100]
        self.recipient = self.getApolloConfig()

        self.driver = Automation.firefoxDriver(self)
        self.wait = WebDriverWait(self.driver, 150)


    def getApolloConfig(self):
        url = "http://apollo-pro.shub.us"
        appid = "rnpos-pipeline"
        cluster = "default"
        namespace = "application"

        r = requests.get("{0}/configfiles/json/{1}/{2}/{3}".format(url, appid, cluster, namespace))
        if r.status_code == 200:
            for k, v in r.json().items():
                if k == "PHASE_RELEASE_GROUP":
                    return v
                else:
                    print("\n>>> Can not get workplace 'PHASE_RELEASE_GROUP'. ")


    def firefoxDriver(self):
        driver_path = "/Users/shbuild/jenkins/workspace/mobile/Android/RN-POS_Phase_Release_Automation/geckodriver"

        # init
        options = webdriver.FirefoxOptions()
        # options.add_argument("-headless")  # Windowless mode
        options.set_preference('browser.link.open_newwindow', '3')
        options.set_preference('permissions.default.image', 2)  # no pictures mode

        profile = webdriver.FirefoxProfile(r"/Users/shbuild/Library/Application Support/Firefox/Profiles/fe1nds70.default-release")
        profile.set_preference("dom.webdriver.enabled", False)
        profile.set_preference('useAutomationExtension', False)
        profile.update_preferences()
        desired = DesiredCapabilities.FIREFOX

        # Open website
        driver = webdriver.Firefox(executable_path=driver_path, options=options, firefox_profile=profile, desired_capabilities=desired)

        print("\n{} \n>>> Creating firefox driver success.".format(today))
        return driver


    def getFirebaseValues(self):
        self.driver.get(url)

        self.wait.until(ec.presence_of_element_located(('css selector', 'button.mat-menu-trigger:nth-child(1)')))

        release_name = self.driver.find_element("css selector", '.fire-feature-bar-title').text
        distribution = self.driver.find_element('css selector', 'div.summary-chip:nth-child(5) > div:nth-child(2)').text

        self.driver.quit()

        return release_name, distribution


    def firebaseAuto(self):
        print("\n>>> Opening firebase website. ")
        self.driver.get(url)

        # waiting for loading complete
        self.wait.until(ec.presence_of_element_located(('css selector', 'button.mat-menu-trigger:nth-child(1)')))

        self.driver.find_element('css selector', 'button.mat-menu-trigger:nth-child(1)').click()
        self.driver.find_element('css selector', '.increase-distribution-button').click()

        # get last number and set present number
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

        self.driver.quit()

        return nownu


    def jenkinsAuto(self):
        print("\n>>> Opening jenkins website. ")
        self.driver.get('https://jenkins.shub.us/job/mobile/job/Android/job/RN-POS_Phase_Release_Automation/configure')

        # start opration
        self.wait.until(ec.presence_of_element_located(("css selector", '#j_username')))
        self.driver.find_element("css selector", '#j_username').send_keys(CONSTANTS.JENKINS_USER)
        self.driver.find_element("css selector", 'div.formRow:nth-child(2) > input:nth-child(1)').send_keys(CONSTANTS.JENKINS_PASSWORD)
        self.driver.find_element("css selector", '.submit-button').click()

        # auto stop
        self.wait.until(ec.presence_of_element_located(("css selector", '#cb32')))
        self.driver.find_element("css selector", '#cb32').send_keys(Keys.SPACE)
        time.sleep(2)

        # set default value
        if auto_run == "true" and terminate == "false":
            self.driver.find_element("css selector", 'div.config_general:nth-child(11) > div:nth-child(4) > div:nth-child(4) > div:nth-child(1) > div:nth-child(2) > textarea:nth-child(1)').send_keys("0 9 * * *")

            selector1 = self.driver.find_element("css selector", 'div.repeated-chunk:nth-child(2) > div:nth-child(1) > div:nth-child(4) > div:nth-child(2) > input:nth-child(1)')
            selector1.clear()
            selector1.send_keys(url)

            time.sleep(1)
            selector2 = self.driver.find_element("css selector", 'div.hetero-list-container:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(4) > div:nth-child(2) > textarea:nth-child(1)')
            selector2.clear()
            selector2.send_keys("Running")
        elif terminate == "true":
            time.sleep(1)
            selector1 = self.driver.find_element("css selector", 'div.hetero-list-container:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(4) > div:nth-child(2) > textarea:nth-child(1)')
            selector1.clear()
            selector1.send_keys("Stopped")

        # save
        self.driver.find_element("xpath", "//button[text()='Save' and @type='button']").click()
        self.wait.until_not(ec.presence_of_element_located(("xpath", "//button[text()='Save' and @type='button']")))

        self.driver.quit()


    def text(self, today, action, release_name, distribution, url):
        text = '''
        Date：{}
        Action: {}
        Release: {}
        Current Stage: {}
        Url: {}
        '''.format(today, action, release_name, distribution, url)

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

        return today_work,tomorrow_work


if __name__ == '__main__':
    auto = Automation()

    url = sys.argv[1]
    auto_run = sys.argv[2]
    terminate = sys.argv[3]
    auto_status = sys.argv[4]

    today = datetime.datetime.now().strftime("%Y-%m-%d")
    today_work, tomorrow_work = auto.dateJudgement()
    release_name, distribution = auto.getFirebaseValues()

    if auto_run == "true" and terminate == "false" and auto_status == "Stopped":
        auto.jenkinsAuto()  # main

        action = "Auto-run mode started."
        text = auto.text(today, action, release_name, distribution, url)

        print(text)
        auto.send_message(text)

    elif terminate == "true" and auto_status == "Running":
        auto.jenkinsAuto()  # main

        action = "Auto-run mode stopped, because of manual termination."
        text = auto.text(today, action, release_name, distribution, url)

        print(text)
        auto.send_message(text)
        
    elif auto_run == "false" and terminate == "false":
        if today_work:
            if int(distribution) == 50 and tomorrow_work == False:
                action = "Today is last workday, not updating to 100%."
                text = auto.text(today, action, release_name, distribution, url)

                print(text)
                auto.send_message(text)
            elif int(distribution) == 100:
                auto.jenkinsAuto()

                action = "Increase distribution had already been update to 100%. Stopped auto-run."
                text = auto.text(today, action, release_name, distribution, url)

                print(text)
                auto.send_message(text)
            else:
                nownu = auto.firebaseAuto()

                if int(nownu) == 100:
                    auto.jenkinsAuto()

                    action = 'Auto-run mode stopped, because of "Increase distribution" = 100%.'
                    text = auto.text(today, action, release_name, distribution, url)

                    print(text)
                    auto.send_message(text)
                else:
                    action = 'Increase phase stage.'
                    text = auto.text(today, action, release_name, distribution, url)

                    print(text)
                    auto.send_message(text)
        else:
            print("\nToday({}) is holiday or last workday, not running automation.".format(today))
    else:
        print("Illegal operation, please check the status of the Jenkins job.\nJenkins auto_run status : ", auto_status)
        text = "Illegal operation, please check the status of the Jenkins job.\nJenkins auto_run status : {}".format(auto_status)
        auto.send_message(text)



