# Data Analysis of Running2win.com users
# Sean Kane & Jake Carlson

import csv
import time
import matplotlib
import matplotlib.pyplot as plt
import statistics
start_time = time.time()

def floatToString(seconds):
    hours = seconds // 3600
    minutes = seconds // 60 % 60
    seconds = seconds % 60

    string = '%02d:%02d:%05.2f' %(hours, minutes, seconds)
    return string

DOWNLOAD_DIR = 'r2wDataKeep.csv'

with open(DOWNLOAD_DIR, 'r') as in_file:
    data = list(csv.reader(in_file))

usernames = []
gender = []
totalMiles = []
eightHundred = []
mile = []
fiveThousand = []
halfMarathon = []
marathon = []
age = []
accountLifetime = []

for d in data:
    usernames.append(d[0])
    gender.append(d[1])
    totalMiles.append(float(d[2]))
    eightHundred.append(float(d[3]))
    mile.append(float(d[4]))
    fiveThousand.append(float(d[5]))
    halfMarathon.append(float(d[6]))
    marathon.append(float(d[7]))
    age.append(int(d[8]))
    accountLifetime.append(int(d[9]))

# -----------------------------------------------------------------------------------------------
# Basic Statistics

male = [1 for g in gender if g == 'Male']
maleProportion = len(male)/len(gender)
femaleProportion = 1 - maleProportion
print(round(100 * maleProportion, 5), '% Male\t', round(100 * femaleProportion, 5), '% Female')

filteredAge = [a for a in age if a != 0]
ageMean = statistics.mean(filteredAge)
ageSD = statistics.stdev(filteredAge)
print('Average age: %.2f \tAge Standard Deviation: %0.2f' % (ageMean, ageSD))

filteredEight = [e for e in eightHundred if e != 0]
filteredMile = [m for m in mile if m != 0]
filteredFiveK = [f for f in fiveThousand if f != 0]
filteredHalf = [h for h in halfMarathon if h != 0]
filteredMarathon = [m for m in marathon if m != 0]

stats = []
stats.append([statistics.mean(filteredEight), statistics.stdev(filteredEight)])
stats.append([statistics.mean(filteredMile), statistics.stdev(filteredMile)])
stats.append([statistics.mean(filteredFiveK), statistics.stdev(filteredFiveK)])
stats.append([statistics.mean(filteredHalf), statistics.stdev(filteredHalf)])
stats.append([statistics.mean(filteredMarathon), statistics.stdev(filteredMarathon)])
statsString = []
for s in stats:
    statsString += [[ floatToString(s[0]), floatToString(s[1]) ]]

print('Average 800: %s \t800 Standard Deviation: %s \tCount:' %(statsString[0][0], statsString[0][1]), len(filteredEight))
print('Average Mile: %s \tMile Standard Deviation: %s \tCount:' %(statsString[1][0], statsString[1][1]), len(filteredMile))
print('Average 5k: %s \t5k Standard Deviation: %s \tCount:' %(statsString[2][0], statsString[2][1]), len(filteredFiveK))
print('Average Half: %s \tHalf Standard Deviation: %s \tCount:' %(statsString[3][0], statsString[3][1]), len(filteredHalf))
print('Average Marathon: %s \tMarathon Standard Deviation: %s \tCount:' %(statsString[4][0], statsString[4][1]), len(filteredMarathon))

# -----------------------------------------------------------------------------------------------
# Plots age vs. mile time
# Filters out all zero answers
x = []
y = []

for i in range(len(age)):
    if age[i] == 0 or mile[i] == 0:
        pass
    else:
        x.append(age[i])
        y.append(mile[i])

# plt.scatter(x, y)
# plt.show()

print("---- %s seconds ----" % round(time.time() - start_time, 4))