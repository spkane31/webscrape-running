# webscrape-running
Webscrape Running2win.com

Developed by Jake Carlson and Sean Kane

carlsojb@mail.uc.edu

kanesp@mail.uc.edu

This project is currently being worked on...

## Python Files

### analysis.py
* Data analysis with statistics and matplotlib python libraries
* Creates plots to show data for final report


### athlete.py
* class file for each scraped athlete

* Hold information like:
    * age
    * gender
    * total
    * miles run
    * personal bests
* Checks to see if personal bests are reasonable
* ie:
    * 1:41 in the 800
    * 3:50 in the mile
    * 13:30 in the 5000
    * :59:00 in the half
    * 2:05:00 in the full marathon
* Checks to see if mileage is realistic:
    * Running very low (> 3 miles/day) and very fast
    * Running very high mileage overa  long period of time ( < 120 miles/wk over years
    * Very young ( > 18) or old ( > 65) and running very high mileage
* Removes data deemed "unrealistic" or "outlier"

### getusers.py


### r2w.py
* Logs in to Running2win.com
* Gathers user info 
    * age
    * gender
    * total
    * miles run
    * personal bests


### plot.py
* Plots user data

## CSV Files

### r2wData.csv
* Data stored here in comma seperated list after each iteration of r2w.py. This file is overwritten each time the script is written.

### r2wDataKeep.csv
* Final data for analysis. We had issues with our script timing out, and therefore we manually migrated data to this file from r2wData.csv, and rerun r2w.py with new usernames

### r2wUsers.csv
* Each line is a recently active user who logged a run, this file is updated by getusers.py
