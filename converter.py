#!/usr/local/bin/python
import os
import sys
import re
import csv
import json
from datetime import datetime, timezone


def datemaker(year, month, day, hour, minute, second=0, microsecond=0):
    """ Because everybody loves messing with datetime. """ 
    return datetime(year, month, day, hour, minute, second, microsecond, tzinfo=timezone.utc).isoformat()


tickets = {
"versions":[
    {"name": "0.09a"}, {"name": "1.0a"}, {"name": "1.0b"}, {"name": "4.0 A Staging"}, 
        {"name": "production 2.0a"}, {"name": "stage 2.0a"}, {"name": "stage 3.0a"}, 
        {"name": "stage 3.5a"}],

"meta": {
        "default_assignee": "ironman", 
        "default_kind": "bug", 
        "default_milestone": "", 
        "default_version": ""
    },
"components": [{"name": "Functional"}, {"name": "Suggestion"}, {"name": "Text"}, 
                {"name": "Usability"},{"name": "User input data"},{"name": "Visual"}],
"issues": [],
"comments": []
}


def umapper(oldname):

    """Old system exported user full name strings; new system needs bitbucket ids."""

    if oldname == "Tony Stark":
        newname = "ironman"
    elif oldname == "Bruce Wayne":
        newname = "batman"
    elif oldname == "Natasha Romanova":
        newname = "blackwidow"
    else: 
        newname = None

    return newname


def vmapper(oldversion):

    """Old system had a funky accidental version."""

    if oldversion == "ou are using v1.0b.":
        newversion = "1.0b"
    else:
        newversion = oldversion

    return newversion


def pmapper(oldpriority):

    """The priorities aren't 1:1."""

    if oldpriority == "Medium":
        newpriority = "minor"
    elif oldpriority == "Low":
        newpriority = "trivial"
    elif oldpriority == "High":
        newpriority = "major"
    elif oldpriority == "Critical":
        newpriority = "critical"
    else:
        newpriority = "trivial"

    return newpriority


def smapper(oldstatus):

    """Naturally the statuses aren't 1:1, either."""

    if oldstatus == "Resolved":
        newstatus = "resolved"
    elif oldstatus == "Closed":
        newstatus = "closed"
    elif oldstatus in ["In progress", "Confirmed", "Acknowledged"]:
        newstatus = "open"
    elif oldstatus == "New":
        newstatus = "new"
    elif oldstatus == "Feedback":
        newstatus = "on hold"
    else:
        newstatus = None

    return newstatus


def cmapper(oldtype):

    """Old Type goes to new Component since the old system didn't export components :'(."""

    if oldtype == "Functional":
        newtype = "Functional"
    elif oldtype == "Suggestion":
        newtype = "Suggestion"
    elif oldtype == "Text":
        newtype = "Text"
    elif oldtype == "Usability":
        newtype = "Usability"
    elif oldtype == "User input data":
        newtype = "User input data"
    elif oldtype == "Visual":
        newtype = "Visual"
    else:
        newtype = None

    return newtype

def stringint(instring='0'):

    """CSVs are a terrible thing."""

    return int(instring.strip("'"))


# DO THE THING

# files setup
commentsfile = "comments.csv"
issuefile = "issues.csv"

# process the comments
with open("comments.csv") as j:
    for q, stuff in enumerate(j):
        k = stuff.split("|")
        dm = datemaker(stringint(k[5]), stringint(k[6]), stringint(k[7]), stringint(k[8]), stringint(k[9]), stringint(k[10]))
        tickets["comments"].append({"content": str(k[1]), "created_on": dm, "user": str(k[2]), "issue": int(k[0]), "id": None})


# process the issues
with open(issuefile) as f:
    for i,line in enumerate(f):
        if re.match(r"^\d*\|", line):
            q = line.split("|")
            updateddt = datetime.strptime(str(q[17]).strip(), "%d/%m/%Y %H:%M:%S").isoformat()
            createddt = datetime.strptime(str(q[17]).strip(), "%d/%m/%Y %H:%M:%S").isoformat()
            
            tickets["issues"].append({"status": smapper(str(q[3])), 
                "priority": pmapper(str(q[4])), 
                "kind": "bug",
                "title": str(q[1]), 
                "reporter": umapper(str(q[8])), 
                "component": cmapper(str(q[6])), 
                "content": str(q[10]), 
                "assignee": umapper(str(q[9])), 
                "created_on": createddt, 
                "version": vmapper(str(q[2])),
                "updated_on": updateddt,
                "id": int(q[0])
                }) 

print(json.dumps(tickets, indent=4, sort_keys=True, default=str))
