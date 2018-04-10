# CS2021 Final Project Spring Semester 2018

# Code written by Sean P. Kane
# Contact information kanesp@mail.uc.edu
# Code written in collaboration with Jake Carlson
# Jake put your e-mail here

import numpy as np
import r2w

# -----------------------------------------------------------------------------------------------------------------------------------
# Class for an athlete after information is scraped from their pages
class athlete():

    def __init__(self, username): #, gender, totalMiles, PRs = [] * 6,  age = 0):
        self.username = username
        self.URL_PROFILE = "http://running2win.com/community/view-member-profile.asp?vu=%s"  % self.username #Change to be personal to each user
        self.URL_RACES = "http://running2win.com/community/AllUserRacesNew.asp?k=0&vu=%s"  % self.username #Change to be personal to each user
        self.URL_PRS = "http://running2win.com/community/AllUserRacesNew.asp?k=0&vu=%s" % self.username
        self.age = r2w.scrapeAgeUser(username)
        self.gender = r2w.scrapeGenderUser(username)
        self.accountAge = r2w.userLifetime(username)
        self.miles = 0
        self.prs = []


    def __rep__(self):
        return "athlete()"
    
    def __str__(self):
        return "Name: %s \t Gender: %s \t Total Miles: %s \t PRs: %s \t Age: %s \t Account Lifetime: %s" %(self.username, self.gender, self.miles, self.prs, self.age, self.accountAge)
    
    def convertToSeconds(self, str):
        s = (str.split(":"))
        num = [float(i) for i in s]
        time = num[-1]
        for i in range(len(num)-1):
            time += 60 * num[i]
        return (time)    

# -----------------------------------------------------------------------------
# Functions to convert a list of strings of pbs to a list of floating point numbers
pbs = [':54', '1:59.2', '4:31', '15:52', '1:12:50', '2:32:26']

def strToSeconds(str):
    time = 0
    s = str.split(":")

    num = []
    for i in s:
        if i == '':
            num.append(0)
            
        else:
            num += [float(i)]

    for i in num:
        time *= 60
        time = time + 1

    return time

# for p in pbs:
#     print(strToSeconds(p))
