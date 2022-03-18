#!/usr/bin/env python3.6
import sys
import re


filename = sys.argv[1]
with open(filename, 'r') as fh:
    lines = fh.readlines()
    branch_list = []
    for i in lines:
        #merge_branch = re.findall("storehubnet/[a-z]+-([\d.]+)", i)
        merge_branch = re.findall("storehubnet/[A-Z]+-\d+", i)
        if merge_branch:
            mer_branch = merge_branch[0].split("/")[1]
            branch_list.append((mer_branch))
        other_branch = re.findall("[A-Za-z]+-[\d.]+", i)
        branch_list.extend(other_branch)
    print("Merged branchs since latest tag:", set(branch_list))
