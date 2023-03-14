#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
import sys
import time

from phaseFuncs import Automation


if __name__ == '__main__':
    phase_url = sys.argv[1]
    auto_run = sys.argv[2]
    terminate = sys.argv[3]
    auto_status = sys.argv[4]

    # ENV
    driver_path = "/Users/shbuild/jenkins/workspace/mobile/Android/RN-POS_Phase_Release_Automation/geckodriver"
    login_cookie = "/Users/shbuild/Library/Application Support/Firefox/Profiles/f9rkhimy.default-release"
    jenkins_url = "https://jenkins.shub.us/job/mobile/job/Android/job/Beep_Phase_Release_Automation/configure"
    increases = [1, 2, 5, 10, 20, 50, 100]
    stage_over = False

    auto = Automation(phase_url, auto_run, terminate, auto_status, driver_path, login_cookie, jenkins_url)

    recipient = auto.getApolloConfig()
    #today_work, tomorrow_work = auto.dateJudgement()

    release_name, current_stage = auto.getPhaseStatus()
    print("Release Name={}\nCurrent Stage={}%".format(release_name, current_stage))

    try:
        index = increases.index(int(current_stage))
        new_stage = increases[index+1]
    except:
        new_stage = int(current_stage)
    print("Next Stage={}%\n".format(new_stage))

    if current_stage == "100":
        action = "Phase stage has been already upgraded to 100%. Please check url."
        text = auto.text(action, release_name, current_stage, phase_url)
    elif int(current_stage) not in increases:
        action = "Current stage({}) is not in [1%, 2%, 5%, 10%, 20%, 50%, 100%]. Not change. Please check.".format(current_stage)
        text = auto.text(action, release_name, current_stage, phase_url)
    else:
        if auto_status == "Stopped" and terminate == "false":
            if auto_run == "true":
                auto.changeJenkins(stage_over)

                action = "Auto-run mode started."
                text = auto.text(action, release_name, current_stage, phase_url)
            elif auto_run == "false":
                stage_over = auto.changePhase(new_stage)
                action = "Increase phase stage by manual update."

                if stage_over:
                    action = "Phase stage was manually upgraded to 100% today."
                text = auto.text(action, release_name, new_stage, phase_url)

        elif auto_status == "Running" and auto_run == "false":
            if terminate == "true":
                auto.changeJenkins(stage_over)

                action = "Auto-run mode stopped, because of manual termination."
                text = auto.text(action, release_name, current_stage, phase_url)
            elif terminate == "false":
                stage_over = auto.changePhase(new_stage)
                action = "Increase phase stage."

                if stage_over:
                    auto.changeJenkins(stage_over)
                    action = "Phase stage was upgraded to 100% today. Stoppend jenkins autoRun."
                text = auto.text(action, release_name, new_stage, phase_url)
        else:
            print(">>> Your operation is not legal and the current Jenkins job status is :{}. Unable to complete the (terminate={},auto_run={}) operation.".format(auto_status, terminate, auto_run))

            action = "Your operation is not legal and the current Jenkins job status is :{}. Unable to complete the (terminate={},auto_run={}) operation.".format(auto_status, terminate, auto_run)
            text = auto.text(action, release_name, current_stage, phase_url)

    auto.driver.quit()
    auto.send_message(recipient, text)



