from bs4 import BeautifulSoup
import requests
import protectedInfo
import athlete
# import mechanicalsoup
# import sys


USERNAME = 'spkane31'
PASSWORD = '08211996'

# Borrowing ideas, code, and organization from loisaidasam on Github
# stravalib-scraper


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


def main():
    s = requests.session()

    #Login to R2W
    s.post('http://www.running2win.com/index.asp', data={
        'txtUsername': USERNAME,
        'txtPassword': PASSWORD,
        'chkRememberMe': 0,
        'btnLogin': 'Login'
    })
    r = s.get('http://running2win.com/community/view-member-running-log.asp')
    # return r
    r2wScrape(r)    
    # print(r.status_code) # A status code of 200 indicates the page was downloaded correctly

def r2wScrape(r):

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

if __name__ == '__main__':
    main()