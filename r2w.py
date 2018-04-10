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

    users = ['Spkane31', 'Thunder_Strohm', 'Tstoverink', 'vmclach', 'Jesspascoe', 'parrell26', 'runsofwrath', 'nolandozier', 'aiabilly', 'spolzin']

    for u in users:

        account = athlete.athlete(u)

        r = s.get('http://www.running2win.com/community/view-member-running-log.asp?vu=%s' % account.username)
        account.miles = r2wScrapeUserInfo(r)

        r = s.get('http://www.running2win.com/community/AllUserRacesNew.asp?k=0&vu=%s' % account.username)
        account.prs = personalBests(account.username, r)

        print(account)

    print("---- %s seconds ----" % (time.time() - start_time))

   
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
# Scrape for user gender
def scrapeGenderUser(user):
    r = s.get('http://www.running2win.com/community/view-member-profile.asp?vu=%s' % user)
    soup = BeautifulSoup(r.content, 'html.parser')
    details = soup.find(text=" Male ")

    gender = "Male"

    if not details:
        gender = "Female"
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
    return round(totalMiles, 2)

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
            eight = strToSeconds(userRaces[i+1].split()[0])
        if '1500 Meters' in u:
            fifteen = strToSeconds(userRaces[i+1].split()[0])
        if '1600 Meters' in u:
            sixteen = strToSeconds(userRaces[i+1].split()[0])
        if '1 Mile' in u and 's' not in u:
            mile = strToSeconds(userRaces[i+1].split()[0])
        if '5 Kilometers' in u and '2' not in u and '1' not in u:
            five = strToSeconds(userRaces[i+1].split()[0])
        if '13.1 Miles' in u:
            half = strToSeconds(userRaces[i+1].split()[0])
        if '26.2 Miles' in u:
            full = strToSeconds(userRaces[i+1].split()[0])
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

    result = round(min(select), 2)
    if result == 99999:
        result = 0

    return result


# -----------------------------------------------------------------------------------------------------------------------------------
# Main method
if __name__ == '__main__':
    main()
