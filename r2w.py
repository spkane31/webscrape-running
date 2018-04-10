# Code written by Sean P. Kane
# Contact information kanesp@mail.uc.edu
# Code written in collaboration with Jake Carlson
# Jake put your e-mail here

# Borrowing ideas, code, and organization from loisaidasam on Github
# stravalib-scraper

from bs4 import BeautifulSoup
import requests
import protectedInfo
import athlete
import time
start_time = time.time()

USERNAME = 'cs2021'
PASSWORD = 'cs2021isfun'

BASE_URL = 'http://running2win.com/'

MEMBER_PROFILE = 'http://www.running2win.com/community/view-member-profile.asp?vu=Spkane31'
MEMBER_RACES = 'http://www.running2win.com/community/AllUserRacesNew.asp?k=0&vu=Spkane31'

s = requests.session()

class r2wScraper(object):
    # BASE_URL = 'http://running2win.com/'

    def __init__ (self, username):
        self.username = username
        self.URL_PROFILE = "http://running2win.com/community/view-member-profile.asp?vu=%s"  % self.username #Change to be personal to each user
        self.URL_RACES = "http://running2win.com/community/AllUserRacesNew.asp?k=0&vu=%s"  % self.username #Change to be personal to each user
        self.URL_PRS = "http://running2win.com/community/AllUserRacesNew.asp?k=0&vu=%s" % self.username
        self.age = scrapeAgeUser(username)
        self.accountAge = userLifetime(username)
        # self.loggedMiles = r2wScrapeUserInfo(username)
        # self.milesRun = 

    


# -----------------------------------------------------------------------------------------------------------------------------------
# Main method to login to R2w
def main():
    s = requests.session()

    #Login to R2W
    s.post('http://www.running2win.com/index.asp', data={
        'txtUsername': USERNAME,
        'txtPassword': PASSWORD,
        'chkRememberMe': 0,
        'btnLogin': 'Login'
    })

    # Link to my Running2Win User Information page

    users = ['hoffmanmax96']

    for u in users:

        account = r2wScraper(u)

        r = s.get('http://www.running2win.com/community/view-member-running-log.asp?vu=%s' % account.username)

        print('Account:', account.username)
        print("Miles Logged:", r2wScrapeUserInfo(r))
        print('Age:',account.age)
        print('Account Age:', account.accountAge)

        r = s.get('http://www.running2win.com/community/AllUserRacesNew.asp?k=0&vu=%s' % account.username)
        pbs = personalBests(account.username, r)
        print('PBs:', pbs)

    print("---- %s seconds ----" % (time.time() - start_time))

    # print(r.status_code) # A status code of 200 indicates the page was downloaded correctly (used for debugging purposes, probably can delete)

# -----------------------------------------------------------------------------------------------------------------------------------
# Scrape for length of time user has been a member
def userLifetime(user):

    r = s.get('http://www.running2win.com/community/view-member-profile.asp?vu=%s' % user)
    lifetime = 0

    soup = BeautifulSoup(r.content, 'html.parser')
    details = soup.find_all('tr')
    lifetimeTag = str(details[21])

    lifetimeStr = []

    for l in lifetimeTag:
        if l in '0123456789,':
            lifetimeStr.append(l)
    lifetimeStr = lifetimeStr[3:]

    for l in lifetimeStr:
        if l != ',':
            lifetime = lifetime * 10 + int(l)
            # print(lifetime)
    return lifetime

# -----------------------------------------------------------------------------------------------------------------------------------
# Scrape for user age
def scrapeAgeUser(user):

    r = s.get('http://www.running2win.com/community/view-member-profile.asp?vu=%s' % user)

    age = 0

    soup = BeautifulSoup(r.content, 'html.parser')

    details = soup.find_all('td')

    userDetails = [d.get_text() for d in details]
    nextAge = False
    for u in userDetails:
        if nextAge:
            try:
                age = int(u)
            except:
                age = 0

        nextAge = False

        if 'Current Age' in u:
            nextAge = True

    return age

# -----------------------------------------------------------------------------------------------------------------------------------
# Scrape for user age
def scrapeGenderUser(user):

    r = s.get('http://www.running2win.com/community/view-member-profile.asp?vu=%s' % user)

    gender = "Male"

    soup = BeautifulSoup(r.content, 'html.parser')

    details = soup.find(text=" Male ")


    i = 0

    if not details:
        gender = "Female"
    # for u in details:
    #     if 'Female' in u:
    #           gender = "Female"
    #
    #
    #     i += 1

return gender

# -----------------------------------------------------------------------------------------------------------------------------------
# Scrape Home Page for Lifetime (Logged) Mileage
def r2wScrapeUserInfo(r):

    soup = BeautifulSoup(r.content, 'html.parser')

    details = soup.find_all('select')

    mileage = [d.get_text() for d in details]

    data = mileage[1]

    data = data.split('\n')

    validNumbers = '0123456789.'

    totalMiles = 0
    for d in data[1:len(data)-1]:
        d = d.split(' - ')
        milesColumn = d[2]
        milesFloat = []
        
        for m in milesColumn:
            if m in validNumbers:
                milesFloat.append(m)

        totalMiles += (list_to_dec(milesFloat))
    return(totalMiles)

def personalBests(user, r):

    eight, fifteen, sixteen, mile, five, half, full = 0, 0, 0, 0, 0, 0, 0

    # r = s.get('http://www.running2win.com/community/AllUserRacesNew.asp?k=0&vu=%s' % user)
    soup = BeautifulSoup(r.content, 'html.parser')
    raceDistances = soup.find_all("div", class_="row")#, class_="col-md-12 race col-md-3")
   
    userRaces = [r.get_text() for r in raceDistances]

    i = 0
    # print(userRaces[i])
    # print(type(userRaces))
    for u in userRaces:
        if '800 Meters' in u:
            e = userRaces[i+1].split()
            eight = strToSeconds(e[0])
        if '1500 Meters' in u:
            e = userRaces[i+1].split()
            fifteen = strToSeconds(e[0])
        if '1600 Meters' in u:
            s = userRaces[i+1].split()
            sixteen = strToSeconds(s[0])
        if '1 Mile' in u and 's' not in u:
            e = userRaces[i+1].split()
            mile = strToSeconds(e[0])
        if '5 Kilometers' in u and '2' not in u and '1' not in u:
            e = userRaces[i+1].split()
            five = strToSeconds(e[0])
        if '13.1 Miles' in u:
            s = userRaces[i+1].split()
            half = strToSeconds(s[0])
        if '26.2 Miles' in u:
            e = userRaces[i+1].split()
            full = strToSeconds(e[0])
            break

        i += 1    

    mile = selectMilePR(fifteen, sixteen, mile)
    return [eight, mile, five, half, full]

    
# ---------------------------------------------------------------
# This function would take a list, ['1', '2', '3', '.', '4'] and return 123.4 in a float
def list_to_dec(lst):
    result = 0

    # Loop counts how many numbers are to the right of the decimal point
    for i in range(0, len(lst)):
        if lst[i] == '.':
            decimals = len(lst) - i
            break

    # Loop creates an integer that has all the numbers added to the end
    for l in lst:
        if l != '.':
            result += int(l)
            result = result * 10

    return result/(10 ** (decimals)) 

# ---------------------------------------------------------------
# Takes a string of a personal bests and converts it into seconds
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
        time = time + i

    return time

# ---------------------------------------------------------------
# Compares a runners 1500, 1600 and full mile PR's, converts to full mile and takes the lowest
def selectMilePR(fifteen, sixteen, mile):
    if fifteen == 0:
        fifteen = 99999
    if sixteen == 0:
        sixteen = 99999
    if mile == 0:
        mile = 99999

    fifteenToMile = 1.08 * fifteen
    sixteenToMile = 1.0058 * sixteen

    select = [fifteenToMile, sixteenToMile, mile]

    return round(min(select), 2)


# -----------------------------------------------------------------------------------------------------------------------------------
# Main method
if __name__ == '__main__':
    main()