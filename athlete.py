# CS2021 Final Project Spring Semester 2018

# Code written by Sean P. Kane
# Contact information kanesp@mail.uc.edu
# Code written in collaboration with Jake Carlson
# Jake put your e-mail here

import numpy as np
       
# -----------------------------------------------------------------------------------------------------------------------------------
# Class for an athlete after information is scraped from their pages
class athlete():

    def __init__(self, name, gender, totalMiles, PRs = [] * 6,  age = 0):
        self.name = name
        self.age = age
        self.gender = gender
        self.miles = totalMiles
        self.prs = PRs

    '''
        TRY to implement this class as an iterable class to allow for use in for loops
    '''

    # def __next__(self):

    # def __iter__(self):

    def __rep__(self):
        return "athlete()"
    
    def __str__(self):
        return "Name: %s \t Gender: %s \t Total Miles: %s \t PRs: %s \t Age: %s" %(self.name, self.gender, self.miles, self.prs, self.age)
    
    def convertToSeconds(self, str):
        s = (str.split(":"))
        num = [float(i) for i in s]
        time = num[-1]
        for i in range(len(num)-1):
            time += 60 * num[i]
        return (time)    




# -------------------------------------------------------------------------------------
# Athlete class test cases
spkane31 = athlete('spkane31', 'Male', 16000, (['54.0', '1:59.2', '4:31', '15:52', '1:12:50', '2:32:26']), 21)
evan = athlete('evansergent', 'Male', 159.18 + 2992.52 + 3273.65 + 703.78, (['', '2:15', '4:37.75', '16:35', '', '3:00:43']), 21)

runners = []
runners.append(spkane31)
runners.append(evan)

# [addToData(r) for r in runners]

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

for p in pbs:
    print(strToSeconds(p))
