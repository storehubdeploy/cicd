#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
  Author  : mingdez
  Dtae    : 201809
"""

import os, sys

class Model(object):    # save xml
    def __init__(self,env,sub,app,git_url,pom_dir=None,mvn_cmd=None,branch='release'):  
        self.env  = env
        self.sub  = sub
        self.app  = app
        self.git_url = git_url
        self.pom_dir = pom_dir  # for 
        self.mvn_cmd = mvn_cmd  # for
        self.branch  = branch   # default : release
        self.description = '{0} {1} {2}'.format(env,sub,app)
        
    def static(self):
        result = '''<?xml version='1.1' encoding='UTF-8'?>
<project>
  <actions/>
  <description>{0}</description>
  <keepDependencies>false</keepDependencies>
  <properties/>
  <scm class="hudson.plugins.git.GitSCM" plugin="git@3.9.1">
    <configVersion>2</configVersion>
    <userRemoteConfigs>
      <hudson.plugins.git.UserRemoteConfig>
        <url>{1}</url>
        <credentialsId>2741cf03-7fb3-4d5b-ac1d-3ef6d023b4c6</credentialsId>
      </hudson.plugins.git.UserRemoteConfig>
    </userRemoteConfigs>
    <branches>
      <hudson.plugins.git.BranchSpec>
        <name>*/{5}</name>
      </hudson.plugins.git.BranchSpec>
    </branches>
    <doGenerateSubmoduleConfigurations>false</doGenerateSubmoduleConfigurations>
    <submoduleCfg class="list"/>
    <extensions/>
  </scm>
  <canRoam>true</canRoam>
  <disabled>false</disabled>
  <blockBuildWhenDownstreamBuilding>false</blockBuildWhenDownstreamBuilding>
  <blockBuildWhenUpstreamBuilding>false</blockBuildWhenUpstreamBuilding>
  <triggers/>
  <concurrentBuild>false</concurrentBuild>
  <builders>
    <hudson.tasks.Shell>
      <command>#!/bin/sh
/data/xj_scripts/for_static/static_deploy.py --env {2} --sub {3} --app {4}</command>
    </hudson.tasks.Shell>
  </builders>
  <publishers/>
  <buildWrappers>
    <hudson.plugins.ansicolor.AnsiColorBuildWrapper plugin="ansicolor@0.5.2">
      <colorMapName>xterm</colorMapName>
    </hudson.plugins.ansicolor.AnsiColorBuildWrapper>
  </buildWrappers>
</project>'''.format(self.description,self.git_url,self.env,self.sub,self.app,self.branch)
        return result
        
    def java(self):
        result = '''<?xml version='1.1' encoding='UTF-8'?>
<maven2-moduleset plugin="maven-plugin@3.1.2">
  <actions/>
  <description>{0}</description>
  <keepDependencies>false</keepDependencies>
  <properties/>
  <scm class="hudson.plugins.git.GitSCM" plugin="git@3.9.1">
    <configVersion>2</configVersion>
    <userRemoteConfigs>
      <hudson.plugins.git.UserRemoteConfig>
        <url>{1}</url>
        <credentialsId>2741cf03-7fb3-4d5b-ac1d-3ef6d023b4c6</credentialsId>
      </hudson.plugins.git.UserRemoteConfig>
    </userRemoteConfigs>
    <branches>
      <hudson.plugins.git.BranchSpec>
        <name>*/{7}</name>
      </hudson.plugins.git.BranchSpec>
    </branches>
    <doGenerateSubmoduleConfigurations>false</doGenerateSubmoduleConfigurations>
    <submoduleCfg class="list"/>
    <extensions/>
  </scm>
  <canRoam>true</canRoam>
  <disabled>false</disabled>
  <blockBuildWhenDownstreamBuilding>false</blockBuildWhenDownstreamBuilding>
  <blockBuildWhenUpstreamBuilding>false</blockBuildWhenUpstreamBuilding>
  <triggers/>
  <concurrentBuild>false</concurrentBuild>
  <rootModule>
    <groupId>com.fonova.kechuan.transdata</groupId>
    <artifactId>pulldata-kechuan</artifactId>
  </rootModule>
  <rootPOM>{5}</rootPOM>
  <goals>{6}</goals>
  <aggregatorStyleBuild>true</aggregatorStyleBuild>
  <incrementalBuild>false</incrementalBuild>
  <ignoreUpstremChanges>true</ignoreUpstremChanges>
  <ignoreUnsuccessfulUpstreams>false</ignoreUnsuccessfulUpstreams>
  <archivingDisabled>false</archivingDisabled>
  <siteArchivingDisabled>false</siteArchivingDisabled>
  <fingerprintingDisabled>false</fingerprintingDisabled>
  <resolveDependencies>false</resolveDependencies>
  <processPlugins>false</processPlugins>
  <mavenValidationLevel>-1</mavenValidationLevel>
  <runHeadless>false</runHeadless>
  <disableTriggerDownstreamProjects>false</disableTriggerDownstreamProjects>
  <blockTriggerWhenBuilding>true</blockTriggerWhenBuilding>
  <settings class="jenkins.mvn.FilePathSettingsProvider">
    <path>/usr/local/maven/conf/settings.xml</path>
  </settings>
  <globalSettings class="jenkins.mvn.FilePathGlobalSettingsProvider">
    <path>/usr/local/maven/conf/settings.xml</path>
  </globalSettings>
  <reporters/>
  <publishers/>
  <buildWrappers>
    <hudson.plugins.ansicolor.AnsiColorBuildWrapper plugin="ansicolor@0.5.2">
      <colorMapName>xterm</colorMapName>
    </hudson.plugins.ansicolor.AnsiColorBuildWrapper>
  </buildWrappers>
  <prebuilders/>
  <postbuilders>
    <hudson.tasks.Shell>
      <command>#!/bin/sh
/data/xj_scripts/for_java/java_deploy.py --env {2} --sub {3} --app {4}</command>
    </hudson.tasks.Shell>
  </postbuilders>
  <runPostStepsIfResult>
    <name>SUCCESS</name>
    <ordinal>0</ordinal>
    <color>BLUE</color>
    <completeBuild>true</completeBuild>
  </runPostStepsIfResult>
</maven2-moduleset>'''.format(self.description,self.git_url,self.env,self.sub,self.app,self.pom_dir,self.mvn_cmd,self.branch)
        return result
        
    def tomcat(self): 
        result = '''<?xml version='1.1' encoding='UTF-8'?>
<maven2-moduleset plugin="maven-plugin@3.1.2">
  <actions/>
  <description>{0}</description>
  <keepDependencies>false</keepDependencies>
  <properties/>
  <scm class="hudson.plugins.git.GitSCM" plugin="git@3.9.1">
    <configVersion>2</configVersion>
    <userRemoteConfigs>
      <hudson.plugins.git.UserRemoteConfig>
        <url>{1}</url>
        <credentialsId>2741cf03-7fb3-4d5b-ac1d-3ef6d023b4c6</credentialsId>
      </hudson.plugins.git.UserRemoteConfig>
    </userRemoteConfigs>
    <branches>
      <hudson.plugins.git.BranchSpec>
        <name>*/{7}</name>
      </hudson.plugins.git.BranchSpec>
    </branches>
    <doGenerateSubmoduleConfigurations>false</doGenerateSubmoduleConfigurations>
    <submoduleCfg class="list"/>
    <extensions/>
  </scm>
  <canRoam>true</canRoam>
  <disabled>false</disabled>
  <blockBuildWhenDownstreamBuilding>false</blockBuildWhenDownstreamBuilding>
  <blockBuildWhenUpstreamBuilding>false</blockBuildWhenUpstreamBuilding>
  <triggers/>
  <concurrentBuild>false</concurrentBuild>
  <rootModule>
    <groupId>com.fosun-wuyuan</groupId>
    <artifactId>wuyuan-restapi</artifactId>
  </rootModule>
  <rootPOM>{5}</rootPOM>
  <goals>{6}</goals>
  <aggregatorStyleBuild>true</aggregatorStyleBuild>
  <incrementalBuild>false</incrementalBuild>
  <ignoreUpstremChanges>true</ignoreUpstremChanges>
  <ignoreUnsuccessfulUpstreams>false</ignoreUnsuccessfulUpstreams>
  <archivingDisabled>false</archivingDisabled>
  <siteArchivingDisabled>false</siteArchivingDisabled>
  <fingerprintingDisabled>false</fingerprintingDisabled>
  <resolveDependencies>false</resolveDependencies>
  <processPlugins>false</processPlugins>
  <mavenValidationLevel>-1</mavenValidationLevel>
  <runHeadless>false</runHeadless>
  <disableTriggerDownstreamProjects>false</disableTriggerDownstreamProjects>
  <blockTriggerWhenBuilding>true</blockTriggerWhenBuilding>
  <settings class="jenkins.mvn.DefaultSettingsProvider"/>
  <globalSettings class="jenkins.mvn.DefaultGlobalSettingsProvider"/>
  <reporters/>
  <publishers/>
  <buildWrappers>
    <hudson.plugins.ansicolor.AnsiColorBuildWrapper plugin="ansicolor@0.5.2">
      <colorMapName>xterm</colorMapName>
    </hudson.plugins.ansicolor.AnsiColorBuildWrapper>
  </buildWrappers>
  <prebuilders/>
  <postbuilders>
    <hudson.tasks.Shell>
      <command>#!/bin/sh
/data/xj_scripts/for_tomcat/tomcat_deploy.py --env {2} --sub {3} --app {4}</command>
    </hudson.tasks.Shell>
  </postbuilders>
  <runPostStepsIfResult>
    <name>SUCCESS</name>
    <ordinal>0</ordinal>
    <color>BLUE</color>
    <completeBuild>true</completeBuild>
  </runPostStepsIfResult>
</maven2-moduleset>'''.format(self.description,self.git_url,self.env,self.sub,self.app,self.pom_dir,self.mvn_cmd,self.branch)
        return result