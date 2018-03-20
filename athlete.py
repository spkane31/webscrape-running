import numpy as np
mileage = []
fiveK = []

def toSeconds(lst):
    
    hour, minutes, sec = 0, 0, 0
    times = []
    for r in lst:
        r = r.split(":")
        if len(r) == 3:
            hour, minutes, sec = float(r[0]), float(r[1]), float(r[2])
        if len(r) == 2 and r[0] != '':
            minutes, sec = float(r[0]), float(r[1])
        if len(r) == 1:
            sec = float(r[0])
        if r[0] == '' and r[1] != '':
            sec = float(r[1])
        

        times.append(hour * 3600 + min * 60 + sec)
    return(times)
       

class athlete():

    def __init__(self, name, gender, totalMiles, PRs = [] * 6,  age = 0):
        self.name = name
        self.age = age
        self.gender = gender
        self.miles = totalMiles
        self.PRs = PRs

    def __rep__(self):
        return "athlete()"
    
    def __str__(self):
        return "Name: %s \t Gender: %s \t Total Miles: %s \t PRs: %s \t Age: %s" %(self.name, self.gender, self.miles, self.PRs, self.age)
    
    def convertToSeconds(self, str):
        s = (str.split(":"))
        num = [float(i) for i in s]
        time = num[-1]
        for i in range(len(num)-1):
            time += 60 * num[i]
        return (time)    

    # def addToData(self):
    #     mileage.append(self.miles)
    #     print(mileage)
    #     fiveK.append(self.PRs[3])
    #     print(fiveK)



def addToData(a):
        mileage.append(a.miles)
        fiveK.append(a.PRs[3])


spkane31 = athlete('spkane31', 'Male', 16000, toSeconds(['54.0', '1:59.2', '4:31', '15:52', '1:12:50', '2:32:26']), 21)
evan = athlete('evansergent', 'Male', 159.18 + 2992.52 + 3273.65 + 703.78, toSeconds(['', '2:15', '4:37.75', '16:35', '', '3:00:43']), 21)
print(spkane31)
print(evan)

runners = []
runners.append(spkane31)
runners.append(evan)
# print(runners)
[addToData(r) for r in runners]
# print(mileage)
# print(fiveK)
# print(np.mean(mileage), np.std(mileage))
# print(np.mean(fiveK), np.std(fiveK))


pbs = [':54', '1:59.2', '4:31', '15:52', '1:12:50', '2:32:26']



# print(toSeconds(pbs))