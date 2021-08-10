#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
  Author  : mingdez
  Dtae    : 201809
"""
import os, sys, json
import jenkins
from optparse import OptionParser

class Model(object):    # save xml
    def __init__(self,app,git_url):
        self.app  = app
        self.git_url = git_url

    def step_01(self):
        result = '''<?xml version='1.1' encoding='UTF-8'?>
<project>
  <actions/>
  <description>master &gt;&gt;&gt; release</description>
  <keepDependencies>false</keepDependencies>
  <properties>
    <com.sonyericsson.rebuild.RebuildSettings plugin="rebuild@1.29">
      <autoRebuild>false</autoRebuild>
      <rebuildDisabled>false</rebuildDisabled>
    </com.sonyericsson.rebuild.RebuildSettings>
  </properties>
  <scm class="hudson.plugins.git.GitSCM" plugin="git@3.9.3">
    <configVersion>2</configVersion>
    <userRemoteConfigs>
      <hudson.plugins.git.UserRemoteConfig>
        <url>{1}</url>
        <credentialsId>45ffa5c8-48bf-4c18-b40f-334bc25d0c56</credentialsId>
      </hudson.plugins.git.UserRemoteConfig>
    </userRemoteConfigs>
    <branches>
      <hudson.plugins.git.BranchSpec>
        <name>origin/master</name>
      </hudson.plugins.git.BranchSpec>
    </branches>
    <doGenerateSubmoduleConfigurations>false</doGenerateSubmoduleConfigurations>
    <submoduleCfg class="list"/>
    <extensions>
      <hudson.plugins.git.extensions.impl.PreBuildMerge>
        <options>
          <mergeRemote>origin</mergeRemote>
          <mergeTarget>release</mergeTarget>
          <mergeStrategy>default</mergeStrategy>
          <fastForwardMode>FF</fastForwardMode>
        </options>
      </hudson.plugins.git.extensions.impl.PreBuildMerge>
    </extensions>
  </scm>
  <canRoam>true</canRoam>
  <disabled>false</disabled>
  <blockBuildWhenDownstreamBuilding>false</blockBuildWhenDownstreamBuilding>
  <blockBuildWhenUpstreamBuilding>false</blockBuildWhenUpstreamBuilding>
  <triggers>
    <com.cloudbees.jenkins.GitHubPushTrigger plugin="github@1.29.4">
      <spec></spec>
    </com.cloudbees.jenkins.GitHubPushTrigger>
  </triggers>
  <concurrentBuild>false</concurrentBuild>
  <builders>
    <hudson.tasks.Shell>
      <command>#!/bin/bash

/data/ops/ci/for_merge/01.py
</command>
    </hudson.tasks.Shell>
  </builders>
  <publishers>
    <hudson.plugins.git.GitPublisher plugin="git@3.9.3">
      <configVersion>2</configVersion>
      <pushMerge>true</pushMerge>
      <pushOnlyIfSuccess>true</pushOnlyIfSuccess>
      <forcePush>false</forcePush>
    </hudson.plugins.git.GitPublisher>
    <hudson.plugins.parameterizedtrigger.BuildTrigger plugin="parameterized-trigger@2.35.2">
      <configs>
        <hudson.plugins.parameterizedtrigger.BuildTriggerConfig>
          <configs>
            <hudson.plugins.parameterizedtrigger.CurrentBuildParameters/>
            <hudson.plugins.parameterizedtrigger.PredefinedBuildParameters>
              <properties>fail_name=$JOB_NAME
fail_number=$BUILD_NUMBER
branch=release</properties>
              <textParamValueOnNewLine>false</textParamValueOnNewLine>
            </hudson.plugins.parameterizedtrigger.PredefinedBuildParameters>
          </configs>
          <projects>merge-{0}-03</projects>
          <condition>UNSTABLE_OR_WORSE</condition>
          <triggerWithNoParameters>false</triggerWithNoParameters>
          <triggerFromChildProjects>false</triggerFromChildProjects>
        </hudson.plugins.parameterizedtrigger.BuildTriggerConfig>
      </configs>
    </hudson.plugins.parameterizedtrigger.BuildTrigger>
    <hudson.plugins.ws__cleanup.WsCleanup plugin="ws-cleanup@0.37">
      <patterns class="empty-list"/>
      <deleteDirs>false</deleteDirs>
      <skipWhenFailed>false</skipWhenFailed>
      <cleanWhenSuccess>true</cleanWhenSuccess>
      <cleanWhenUnstable>true</cleanWhenUnstable>
      <cleanWhenFailure>true</cleanWhenFailure>
      <cleanWhenNotBuilt>true</cleanWhenNotBuilt>
      <cleanWhenAborted>true</cleanWhenAborted>
      <notFailBuild>false</notFailBuild>
      <cleanupMatrixParent>false</cleanupMatrixParent>
      <externalDelete></externalDelete>
      <disableDeferredWipeout>false</disableDeferredWipeout>
    </hudson.plugins.ws__cleanup.WsCleanup>
  </publishers>
  <buildWrappers>
    <hudson.plugins.ansicolor.AnsiColorBuildWrapper plugin="ansicolor@0.5.3">
      <colorMapName>xterm</colorMapName>
    </hudson.plugins.ansicolor.AnsiColorBuildWrapper>
  </buildWrappers>
</project>'''.format(self.app,self.git_url)
        return result

    def step_02(self):
        result = '''<?xml version='1.1' encoding='UTF-8'?>
<project>
  <actions/>
  <description>release &gt;&gt;&gt; development</description>
  <keepDependencies>false</keepDependencies>
  <properties>
    <com.sonyericsson.rebuild.RebuildSettings plugin="rebuild@1.29">
      <autoRebuild>false</autoRebuild>
      <rebuildDisabled>false</rebuildDisabled>
    </com.sonyericsson.rebuild.RebuildSettings>
  </properties>
  <scm class="hudson.plugins.git.GitSCM" plugin="git@3.9.3">
    <configVersion>2</configVersion>
    <userRemoteConfigs>
      <hudson.plugins.git.UserRemoteConfig>
        <url>{1}</url>
        <credentialsId>45ffa5c8-48bf-4c18-b40f-334bc25d0c56</credentialsId>
      </hudson.plugins.git.UserRemoteConfig>
    </userRemoteConfigs>
    <branches>
      <hudson.plugins.git.BranchSpec>
        <name>origin/release</name>
      </hudson.plugins.git.BranchSpec>
    </branches>
    <doGenerateSubmoduleConfigurations>false</doGenerateSubmoduleConfigurations>
    <submoduleCfg class="list"/>
    <extensions>
      <hudson.plugins.git.extensions.impl.PreBuildMerge>
        <options>
          <mergeRemote>origin</mergeRemote>
          <mergeTarget>development</mergeTarget>
          <mergeStrategy>default</mergeStrategy>
          <fastForwardMode>FF</fastForwardMode>
        </options>
      </hudson.plugins.git.extensions.impl.PreBuildMerge>
    </extensions>
  </scm>
  <canRoam>true</canRoam>
  <disabled>false</disabled>
  <blockBuildWhenDownstreamBuilding>false</blockBuildWhenDownstreamBuilding>
  <blockBuildWhenUpstreamBuilding>false</blockBuildWhenUpstreamBuilding>
  <triggers>
    <com.cloudbees.jenkins.GitHubPushTrigger plugin="github@1.29.4">
      <spec></spec>
    </com.cloudbees.jenkins.GitHubPushTrigger>
  </triggers>
  <concurrentBuild>false</concurrentBuild>
  <builders>
    <hudson.tasks.Shell>
      <command>#!/bin/bash

/data/ops/ci/for_merge/01.py
</command>
    </hudson.tasks.Shell>
  </builders>
  <publishers>
    <hudson.plugins.git.GitPublisher plugin="git@3.9.3">
      <configVersion>2</configVersion>
      <pushMerge>true</pushMerge>
      <pushOnlyIfSuccess>true</pushOnlyIfSuccess>
      <forcePush>false</forcePush>
    </hudson.plugins.git.GitPublisher>
    <hudson.plugins.parameterizedtrigger.BuildTrigger plugin="parameterized-trigger@2.35.2">
      <configs>
        <hudson.plugins.parameterizedtrigger.BuildTriggerConfig>
          <configs>
            <hudson.plugins.parameterizedtrigger.CurrentBuildParameters/>
            <hudson.plugins.parameterizedtrigger.PredefinedBuildParameters>
              <properties>fail_name=$JOB_NAME
fail_number=$BUILD_NUMBER
branch=development</properties>
              <textParamValueOnNewLine>false</textParamValueOnNewLine>
            </hudson.plugins.parameterizedtrigger.PredefinedBuildParameters>
          </configs>
          <projects>merge-{0}-03</projects>
          <condition>UNSTABLE_OR_WORSE</condition>
          <triggerWithNoParameters>false</triggerWithNoParameters>
          <triggerFromChildProjects>false</triggerFromChildProjects>
        </hudson.plugins.parameterizedtrigger.BuildTriggerConfig>
      </configs>
    </hudson.plugins.parameterizedtrigger.BuildTrigger>
    <hudson.plugins.ws__cleanup.WsCleanup plugin="ws-cleanup@0.37">
      <patterns class="empty-list"/>
      <deleteDirs>false</deleteDirs>
      <skipWhenFailed>false</skipWhenFailed>
      <cleanWhenSuccess>true</cleanWhenSuccess>
      <cleanWhenUnstable>true</cleanWhenUnstable>
      <cleanWhenFailure>true</cleanWhenFailure>
      <cleanWhenNotBuilt>true</cleanWhenNotBuilt>
      <cleanWhenAborted>true</cleanWhenAborted>
      <notFailBuild>false</notFailBuild>
      <cleanupMatrixParent>false</cleanupMatrixParent>
      <externalDelete></externalDelete>
      <disableDeferredWipeout>false</disableDeferredWipeout>
    </hudson.plugins.ws__cleanup.WsCleanup>
  </publishers>
  <buildWrappers>
    <hudson.plugins.ansicolor.AnsiColorBuildWrapper plugin="ansicolor@0.5.3">
      <colorMapName>xterm</colorMapName>
    </hudson.plugins.ansicolor.AnsiColorBuildWrapper>
  </buildWrappers>
</project>'''.format(self.app,self.git_url)
        return result

    def step_03(self):
        result = '''<?xml version='1.1' encoding='UTF-8'?>
<project>
  <actions/>
  <description>raise PR when failed</description>
  <keepDependencies>false</keepDependencies>
  <properties>
    <com.sonyericsson.rebuild.RebuildSettings plugin="rebuild@1.29">
      <autoRebuild>false</autoRebuild>
      <rebuildDisabled>false</rebuildDisabled>
    </com.sonyericsson.rebuild.RebuildSettings>
    <hudson.model.ParametersDefinitionProperty>
      <parameterDefinitions>
        <hudson.model.StringParameterDefinition>
          <name>fail_name</name>
          <description></description>
          <defaultValue></defaultValue>
          <trim>false</trim>
        </hudson.model.StringParameterDefinition>
        <hudson.model.StringParameterDefinition>
          <name>fail_number</name>
          <description></description>
          <defaultValue></defaultValue>
          <trim>false</trim>
        </hudson.model.StringParameterDefinition>
        <hudson.model.StringParameterDefinition>
          <name>branch</name>
          <description></description>
          <defaultValue></defaultValue>
          <trim>false</trim>
        </hudson.model.StringParameterDefinition>    
      </parameterDefinitions>
    </hudson.model.ParametersDefinitionProperty>
  </properties>
  <scm class="hudson.plugins.git.GitSCM" plugin="git@3.9.3">
    <configVersion>2</configVersion>
    <userRemoteConfigs>
      <hudson.plugins.git.UserRemoteConfig>
        <url>{0}</url>
        <credentialsId>45ffa5c8-48bf-4c18-b40f-334bc25d0c56</credentialsId>
      </hudson.plugins.git.UserRemoteConfig>
    </userRemoteConfigs>
    <branches>
      <hudson.plugins.git.BranchSpec>
        <name>origin/development</name>
      </hudson.plugins.git.BranchSpec>
    </branches>
    <doGenerateSubmoduleConfigurations>false</doGenerateSubmoduleConfigurations>
    <submoduleCfg class="list"/>
    <extensions>
      <hudson.plugins.git.extensions.impl.LocalBranch>
        <localBranch>development</localBranch>
      </hudson.plugins.git.extensions.impl.LocalBranch>
    </extensions>
  </scm>
  <canRoam>true</canRoam>
  <disabled>false</disabled>
  <blockBuildWhenDownstreamBuilding>false</blockBuildWhenDownstreamBuilding>
  <blockBuildWhenUpstreamBuilding>false</blockBuildWhenUpstreamBuilding>
  <triggers/>
  <concurrentBuild>false</concurrentBuild>
  <builders>
    <hudson.tasks.Shell>
      <command>#!/bin/bash

/data/ops/ci/for_merge/02.sh</command>
    </hudson.tasks.Shell>
  </builders>
  <publishers>
    <hudson.plugins.ws__cleanup.WsCleanup plugin="ws-cleanup@0.37">
      <patterns class="empty-list"/>
      <deleteDirs>false</deleteDirs>
      <skipWhenFailed>false</skipWhenFailed>
      <cleanWhenSuccess>true</cleanWhenSuccess>
      <cleanWhenUnstable>true</cleanWhenUnstable>
      <cleanWhenFailure>true</cleanWhenFailure>
      <cleanWhenNotBuilt>true</cleanWhenNotBuilt>
      <cleanWhenAborted>true</cleanWhenAborted>
      <notFailBuild>false</notFailBuild>
      <cleanupMatrixParent>false</cleanupMatrixParent>
      <externalDelete></externalDelete>
      <disableDeferredWipeout>false</disableDeferredWipeout>
    </hudson.plugins.ws__cleanup.WsCleanup>
  </publishers>
  <buildWrappers>
    <hudson.plugins.ws__cleanup.PreBuildCleanup plugin="ws-cleanup@0.37">
      <deleteDirs>false</deleteDirs>
      <cleanupParameter></cleanupParameter>
      <externalDelete></externalDelete>
      <disableDeferredWipeout>false</disableDeferredWipeout>
    </hudson.plugins.ws__cleanup.PreBuildCleanup>
    <hudson.plugins.ansicolor.AnsiColorBuildWrapper plugin="ansicolor@0.5.3">
      <colorMapName>xterm</colorMapName>
    </hudson.plugins.ansicolor.AnsiColorBuildWrapper>
  </buildWrappers>
</project>'''.format(self.git_url)
        return result

if __name__ == "__main__":
    parser = OptionParser()
    parser.add_option("-a","--app"      , dest="app"      , default=None)
    parser.add_option("-u","--git_url"  , dest="git_url"  , default=None)
    (options, args) = parser.parse_args()

    app      = options.app
    git_url  = options.git_url

    # jenkins
    json_rc   = {}
    user_id   = 'jenkins_pub'
    api_token = 'admin@#098'
    url       = 'https://jenkins.shub.us'
    server=jenkins.Jenkins( url, username=user_id, password=api_token)

    # Step-01
    old_job = 'merge-template-01'
    new_job = 'merge-{}-01'.format(app)
    model   = Model(app,git_url)
    result  = model.step_01()

    server.copy_job(old_job, new_job)                   # copy from old to new
    server.reconfig_job(new_job,result)                 # Reconfig
    server.disable_job(new_job)                         # disable new
    server.enable_job(new_job)                          # enable new

    # Step-02
    old_job = 'merge-template-02'
    new_job = 'merge-{}-02'.format(app)
    model   = Model(app,git_url)
    result  = model.step_02()

    server.copy_job(old_job, new_job)                   # copy from old to new
    server.reconfig_job(new_job,result)                 # Reconfig
    server.disable_job(new_job)                         # disable new
    server.enable_job(new_job)                          # enable new

    # Step-02
    old_job = 'merge-template-03'
    new_job = 'merge-{}-03'.format(app)
    model   = Model(app,git_url)
    result  = model.step_03()

    server.copy_job(old_job, new_job)                   # copy from old to new
    server.reconfig_job(new_job,result)                 # Reconfig
    server.disable_job(new_job)                         # disable new
    server.enable_job(new_job)                          # enable new

    json_rc['app'    ] = 'auto-merge-{}'.format(app)
    json_rc['result' ] = 'SUCCESS'
    print(json.dumps(json_rc))
  
