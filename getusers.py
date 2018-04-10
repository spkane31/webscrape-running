# File for mining users for analysis
# Part of webscrape-running project for CS2021
# Developed by Jake Carlson and Sean Kane

from bs4 import BeautifulSoup
import requests
import time
start_time = time.time()

USERNAME = 'cs2021'
PASSWORD = 'cs2021isfun'

MEMBER_PROFILE = 'http://www.running2win.com/community/view-member-profile.asp?vu=Spkane31'
MEMBER_RACES = 'http://www.running2win.com/community/AllUserRacesNew.asp?k=0&vu=Spkane31'

writeToCSV = []

def main():
    s = requests.session()

    #Login to R2W
    s.post('http://www.running2win.com/index.asp', data={
        'txtUsername': USERNAME,
        'txtPassword': PASSWORD,
        'chkRememberMe': 0,
        'btnLogin': 'Login'
    })

    r = s.get('http://www.running2win.com/community/dailyruns.asp')
    soup = BeautifulSoup(r.content, 'html.parser')
    details = soup.find_all("td", {'align': 'left', 'valign': None}) #aligh_="left")
    users = [d.get_text() for d in details]

    for u in users:
        if (' ' in u) == True or 'Member' in u:
            users.remove(u)
            print('REMOVED')
        elif u in writeToCSV:
            users.remove(u)
            print('REMOVED')
            pass
        else:
            writeToCSV.append(u)

    print(len(users))
    storeAccount(writeToCSV)

    print('Number of Users:', len(writeToCSV))
    print("---- %s seconds ----" % (time.time() - start_time))
        
def storeAccount(usernames):
    timeSearch = time.time()
    download_dir = 'r2wUsers.csv' #r2wUsers%s.csv' % str(int(timeSearch))
    csv = open(download_dir, "w")

    columnTitleRow = "username\n"
    csv.write(columnTitleRow)
    for u in usernames:
        csv.write(u + "\n")

        

if __name__ == '__main__':
    main()