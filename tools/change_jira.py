# This script shows how to use the client in anonymous mode
# against jira.atlassian.com.
import sys
from jira import JIRA
import re

# By default, the client will connect to a Jira instance started from the Atlassian Plugin SDK
# (see https://developer.atlassian.com/display/DOCS/Installing+the+Atlassian+Plugin+SDK for details).
# Override this with the options parameter.
jira = JIRA('https://storehub.atlassian.net', basic_auth=(name, password)

# Get all projects viewable by anonymous users.
projects = jira.projects()
print(projects)

# Sort available project keys, then return the second, third, and fourth keys.
keys = sorted([project.key for project in projects])[2:5]
print(keys)
# Get an issue.
get_issue = sys.argv[1]
comments = sys.argv[2]
label1 = sys.argv[3]
print(get_issue)
if get_issue.startswith("release"):
    print('No ticket')
else:
    issue = jira.issue(get_issue)
    transitions = jira.transitions(issue)
    t = [(t['id'], t['name']) for t in transitions]
    print(t)
    jira.add_comment(issue, comments)
    issue.update(fields={"labels": [label1]})    
#trans = sys.argv[2]
#print(trans)
#user_id = sys.argv[3]
#print(user_id)
#jira.transition_issue(issue, trans, assignee={'id': user_id})
#print(issue.fields.status)


# Find all comments made by Atlassians on this issue.
#atl_comments = [
#    comment
#    for comment in issue.fields.comment.comments
#    if re.search(r"", comment.author.emailAddress)
#]
#print(atl_comments)
# Add a comment to the issue.

# Change the issue's summary and description.
#issue.update(
#    summary="I'm different!", description="Changed the summary to be different."
#)

# Change the issue without sending updates
#issue.update(notify=False, description="Quiet summary update.")

# You can update the entire labels field like this
#label2 = sys.argv[6]

# Or modify the List of existing labels. The new label is unicode with no
# spaces
#issue.fields.labels.append(u"new_text")
#issue.update(fields={"labels": issue.fields.labels})

# Send the issue away for good.
#issue.delete()

# Linking a remote jira issue (needs applinks to be configured to work)
#issue = jira.issue("JRA-1330")
#issue2 = jira.issue("XX-23")  # could also be another instance
#jira.add_remote_link(issue, issue2)
