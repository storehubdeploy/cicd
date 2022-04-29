#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
import datetime
import json
import os
import sys
import time

import requests
from chinese_calendar import is_workday
from dotenv import dotenv_values
from selenium import webdriver
from selenium.webdriver import DesiredCapabilities, Keys
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait


class Automation(object):
    def __init__(self):
        self.url = sys.argv[1]
        self.increases = [1, 2, 5, 10, 20, 50, 100]
        self.today = datetime.datetime.now().strftime("%Y-%m-%d")

        self.JENKISN_USER, self.JENKISN_PWD, self.WORKPLACE_URL, self.WORKPLACE_TOKEN = self.info()
        self.recipient = self.getApolloConfig()

        self.driver = Automation.firefoxDriver(self)
        self.wait = WebDriverWait(self.driver, 150)


    def info(self):
        path = os.path.join(os.path.dirname(__file__), 'ci.env')
        config = dotenv_values(path)

        JENKISN_USER = config['JENKISN_USER']
        JENKISN_PWD = config['JENKISN_PWD']

        WORKPLACE_URL = config['WORKPLACE_URL']
        WORKPLACE_TOKEN = config['WORKPLACE_TOKEN']

        return JENKISN_USER, JENKISN_PWD, WORKPLACE_URL, WORKPLACE_TOKEN


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
        options.add_argument("-headless") # Windowless mode
        options.set_preference('browser.link.open_newwindow', '3')
        options.set_preference('permissions.default.image', 2)  # no pictures mode

        profile = webdriver.FirefoxProfile(r"/Users/shbuild/Library/Application Support/Firefox/Profiles/fe1nds70.default-release")
        profile.set_preference("dom.webdriver.enabled", False)
        profile.set_preference('useAutomationExtension', False)
        profile.update_preferences()
        desired = DesiredCapabilities.FIREFOX

        # Open website
        driver = webdriver.Firefox(executable_path=driver_path, options=options, firefox_profile=profile, desired_capabilities=desired)

        print("\n{} \n>>> Creating firefox driver success.".format(self.today))
        return driver


    def firebaseAuto(self):
        print("\n>>> Opening firebase website. ")
        self.driver.get(self.url)

        # waiting for loading complete
        self.wait.until(ec.presence_of_element_located(('css selector', 'button.mat-menu-trigger:nth-child(1)')))

        self.driver.find_element('css selector', 'button.mat-menu-trigger:nth-child(1)').click()
        self.driver.find_element('css selector', '.increase-distribution-button').click()

        # get last number and set present number
        prenu = self.driver.find_element('css selector', 'input.ng-pristine').get_attribute('value')

        if int(prenu) == 50 and tomorrow_work == False:
            nownu = int(prenu)
            print("Today({}) is last workday, not updating to 100.".format(self.today))
            text = '{}: Today is last workday, not updating to 100.'
            self.send_message(text)
        else:
            index = self.increases.index(int(prenu))
            nownu = self.increases[index+1]

            time.sleep(2)
            self.driver.find_element('css selector', 'input.ng-pristine').clear()
            self.driver.find_element('css selector', 'input.ng-pristine').send_keys(nownu)

            time.sleep(2)
            self.driver.find_element('css selector', '.send-button').click()

            # waiting for operating before
            self.wait.until_not(ec.presence_of_element_located(('css selector', '.send-button')))

            print('\n>>>"Increase distribution" have been updated.  \n>>> And now, Increase distribution = {}%. '.format(nownu))
            text = '''
            {}: "Increase distribution" have been updated.\nIncrease distribution = {}%.
            '''.format(self.today, nownu)

            self.send_message(text)

        if int(nownu) == 100:
            Automation.jenkinsAuto(self)
            print("\n>>> Auto-run mode stopped, because of Increase distribution = 100%.")
            text = "{}: Auto-run mode stopped, because of Increase distribution = 100%.".format(self.today)
            self.send_message(text)
        else:
            self.driver.quit()


    def jenkinsAuto(self):
        print("\n>>> Opening jenkins website. ")
        self.driver.get('https://jenkins.shub.us/job/mobile/job/Android/job/RN-POS_Phase_Release_Automation/configure')

        # start opration
        self.wait.until(ec.presence_of_element_located(("css selector", '#j_username')))
        self.driver.find_element("css selector", '#j_username').send_keys(self.JENKISN_USER)
        self.driver.find_element("css selector", 'div.formRow:nth-child(2) > input:nth-child(1)').send_keys(self.JENKISN_PWD)
        self.driver.find_element("css selector", '.submit-button').click()

        # auto stop
        self.wait.until(ec.presence_of_element_located(("css selector", '#cb32')))
        self.driver.find_element("css selector", '#cb32').send_keys(Keys.SPACE)
        time.sleep(2)

        # set default value
        if auto_run == "true":
            self.driver.find_element("css selector", 'div.config_general:nth-child(11) > div:nth-child(4) > div:nth-child(4) > div:nth-child(1) > div:nth-child(2) > textarea:nth-child(1)').send_keys("0 9 * * *")

            selector1 = self.driver.find_element("css selector", 'div.hetero-list-container:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(4) > div:nth-child(2) > input:nth-child(1)')
            selector1.clear()
            selector1.send_keys(self.url)

            text = '''
            {}: Auto-run mode started.\nIt will run automatically according to the rule of [1%,2%,5%,10%,20%,50%,100%].\nURL: {}
            '''.format(self.today, self.url)
            self.send_message(text)

            print("\n>>> Auto-run mode started. It will run automatically according to the rule of [1%,2%,5%,10%,20%,50%,100%]. ")
        elif terminate == "true":
            text = "{}: Auto-run mode stopped, because of manual termination.".format(self.today)
            self.send_message(text)

            print("\n>>> Auto-run mode stopped, because of manual termination. ")

        # save
        self.driver.find_element("xpath", "//button[text()='Save' and @type='button']").click()
        self.wait.until_not(ec.presence_of_element_located(("xpath", "//button[text()='Save' and @type='button']")))

        self.driver.quit()


    def send_message(self, text):
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
        url = self.WORKPLACE_URL
        headers = {'Content-Type': 'application/json'}
        payload = {'access_token': self.WORKPLACE_TOKEN}

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

    auto_run = sys.argv[2]
    terminate = sys.argv[3]

    today_work, tomorrow_work = auto.dateJudgement()

    if auto_run == "true" and terminate == "false":
        auto.jenkinsAuto()
        print("\n>>> Automation is starting!!! ")
    elif terminate == "true" or (terminate == "true" and auto_run == "true"):
        auto.jenkinsAuto()
        print("\n>>> Automation was stopped!!! ")
    elif auto_run == "false" and terminate == "false":
        if today_work:
            auto.firebaseAuto()
        else:
            print("\nToday({}) is holiday or last workday, not running automation.".format(datetime.datetime.now().strftime("%Y-%m-%d")))
    else:
        print("error")



