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

USERNAME = 'spkane31'
PASSWORD = 'jakeisnofun'

BASE_URL = 'http://running2win.com/'

MEMBER_PROFILE = 'http://www.running2win.com/community/view-member-profile.asp?vu=Spkane31'
MEMBER_RACES = 'http://www.running2win.com/community/AllUserRacesNew.asp?k=0&vu=Spkane31'

class r2wScraper(object):
    BASE_URL = 'http://running2win.com/'

    URL_PROFILE = "%s/community/view-member-profile.asp?vu=Spkane31"  % BASE_URL #Change to be personal to each user
    URL_RACES = "%s/community/AllUserRacesNew.asp?k=0&vu=Spkane31"  % BASE_URL #Change to be personal to each user

    def __init__(self, username, password):
        self.username = USERNAME
        self.password = PASSWORD
        self.session = requests.Session

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

    # Below link will scrape the users Running Log and return all runs displayed in format ['mileage', 'distance', 'pace']
    r = s.get('http://www.running2win.com/community/view-member-running-log.asp')

    # Below is the link to the my Running2Win User Information page
    r = s.get('http://www.running2win.com/community/view-member-profile.asp?vu=Spkane31')

    userAge, userLifetime = scrapeAgeUser(r)

    print('User Age:', userAge)
    print('User Lifetime:', userLifetime)

    # r2wScrapeUserInfo(r)    
    # print(r.status_code) # A status code of 200 indicates the page was downloaded correctly (used for debugging purposes, probably can delete)

# -----------------------------------------------------------------------------------------------------------------------------------
# Scrape for age and days user
def scrapeAgeUser(r):

    age, lifetime = 0, 0

    soup = BeautifulSoup(r.content, 'html.parser')

    details = soup.find_all('td')

    userDetails = [d.get_text() for d in details]
    nextAge = False
    nextUserLifetime = False
    for u in userDetails:
        if nextAge:
            try:
                age = int(u)
            except:
                age = 0
        if nextUserLifetime:
            try:
                print(int(u), 'lifetime')
                lifetime = int(u)
            except:
                lifetime = 0

        nextAge = False
        nextUserLifetime = False

        if 'Current Age' in u:
            nextAge = True
        if 'Number of days' in u:
            nextUserLifetime = True

    return age, lifetime

    # nextAge = False
    # nextLifetime = False
    # for u in userDetails:

    #     if nextAge:
    #         print('User Age', u)
    #         userAge = int(u)
    #     if nextLifetime:
    #         print('User Lifetime', u)
    #         userLifetime = int(u)

    #     nextAge = False
    #     nextLifetime = False

    #     if 'days' in u:
    #         nextLifetime = True
    #         print(u)
    #     if 'Current Age' in u:
    #         nextAge = True
    #         print(u)

        


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
    print(totalMiles)
    return(totalMiles)

  

# -----------------------------------------------------------------------------------------------------------------------------------
# Scrape users running log page for all runs, distance, and paces
def r2wScrapeRunningLog(r):

    soup = BeautifulSoup(r.content, 'html.parser')

    details = soup.find_all('strong') 

    runs = [d.get_text() for d in details ]

    Data = []
    for r in runs:
        newRow = []
        if 'Miles' in r: # Parses for all details involving a run
            row = r.split()
            newRow.append(row[0])
            newRow.append(row[3])
            pace = row[4]
            pace = pace[1:]
            newRow.append(pace)
        if newRow != []:
            Data.append(newRow)
    print(Data)


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

# -----------------------------------------------------------------------------------------------------------------------------------
# Main method
if __name__ == '__main__':
    main()