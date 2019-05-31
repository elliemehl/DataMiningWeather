# Gabrielle Mehltretter 20065730 April 5th 2019
# This program sorts and searches data from the Toronto Pearson Airport.
# Calculates mean temperature, max temperature, amounts of rain and snow
# giving dates as well.

# This given function creates a list of dictionaries from the file.
# Each dictionary has the data for a certain month of a certain year.

def readData(filename):
    fileIn = open(filename, 'r')
    allData = []
    line = fileIn.readline()
    while line != "":
        line = fileIn.readline().strip()
        if line != "":
            values = line.split(',')
            monthData = {}
            monthData['year'] = int(values[0])
            monthData['month'] = int(values[1])
            monthData['yearmonth'] = int(values[0]) * 100 + int(values[1])
            monthData['meanT'] = float(values[2])
            monthData['maxT'] = float(values[3])
            monthData['minT'] = float(values[4])
            monthData['rain'] = float(values[5])
            monthData['snow'] = float(values[6])
            allData.append(monthData)
    fileIn.close()
    return allData

# This function prints the beginning and end portions of the
# supplied list of dictionaries.

def showSome(allData):
    for i in range(10):
        print(allData[i])
    print("<snip>")
    for i in range(-10, 0):
        print(allData[i])

# This function ensures that given integers fall within
# proper parameters.

def getInt(prompt, lowLimit=None, highLimit=None):
    numberOK = False
    while not numberOK:
        try:
            userNum = int(input(prompt))
            if lowLimit != None and userNum < lowLimit:
                print("The number must be higher than", lowLimit)
                print("Please try again.")
            elif highLimit != None and userNum > highLimit:
                print("The number must be lower than", highLimit)
                print("Please try again.")
            else:
                numberOK = True
        except ValueError:
            print("Your entry is not a valid integer, please try again.")
    return userNum

# This insertion sort function sorts the file in increasing order
# by "yearmonth". Starting with the first index decides if
# the value should be before or after the zero index. Continues
# through every index, switching where needed.

def insertionSort(allData, key):
    for i in range(1, len(allData)):
        temp = allData[i]
        j = i - 1
        while j >= 0 and temp[key] < allData[j][key]:
            allData[j + 1] = allData[j]
            j -= 1
        allData[j + 1] = temp
        
# This function uses a binary search to find the amount of rain
# from a certain date. Binary search finds the midpoint in the data
# it then cuts the data in half and searches the half with the
# point it is looking for. It continues to cut the data in half
# until it finds the data it is looking for. The function assumes the
# data has been sorted in increasing order by date. The function will
# raise a ValueError exception if the year and month target do not
# exist in the data.

def findRain(allData, target):
    low = 0
    high = len(allData) - 1
    found = False
    while low <= high and not found:
        mid = (low + high) // 2
        if target == allData[mid]["yearmonth"]:
            found = True
        else:
            if target < allData[mid]["yearmonth"]:
                high = mid - 1
            else:
                low = mid + 1
    return allData[mid]["rain"]

    raise ValueError("Target rainfall not found!")

# This function finds the max value in the data for a certain key.

def findMax(allData, key):
    val = 0
    for i in range(1, len(allData)):
        if allData[i][key] > allData[val][key]:
            val = i
    return allData[val]

# This function finds the min value in the data for a certain key.

def findMin(allData, key):
    val = 0
    for i in range(1, len(allData)):
        if allData[i][key] < allData[val][key]:
            val = i
    return allData[val]

# This function returns a list of dictionaries that say the total amount
# of snow for every year in the data.

def getAnnualSnow(allData):
    snowData = []
    i = 0
    while i < len(allData):
        snowSum = 0
        currentYear = allData[i]["year"]
        while i < len(allData) and allData[i]["year"] == currentYear:
            snowSum = snowSum + allData[i]["snow"]
            i = i + 1

        yearOfSnow = {}
        yearOfSnow["year"] = allData[i-1]["year"]
        yearOfSnow["totalsnow"] = snowSum

        snowData.append(yearOfSnow)
    return snowData

# This function calculates the mean temperatures for a year in the data.

def saveAnnualMeanTemp(allData, filename):
    file = open(filename, "w+")
    i = 0
    while i < len(allData):
        tempSum = 0
        currentYear = allData[i]["year"]
        while i < len(allData) and allData[i]["year"] == currentYear:
            tempSum = tempSum + allData[i]["meanT"]
            i = i + 1
        tempSum = tempSum / 12
    file.write(str(tempSum) + "\n")
    file.close()

# The main function was given. It first opens the file and then prints both the
# unsorted and sorted list of dictionaries made from the file. It then prompts
# for a certian month and year and prints the rainfall for that month. It will
# raise a ValueError exception if there is no data for that month. It then will
# print the max and min for temperature as well as the max snowfall and rainfall.
# Also prints the highest, lowest and median snowfall. Finally it will print the
# highest, lowest and median mean temperature for the data.

def main():
    db = readData("TorontoWeatherData.csv")
    unsortedDb = readData("TorontoWeatherData.csv")
    print("Before sorting, as read from file:")
    showSome(db)
    insertionSort(db, 'yearmonth')
    print("\nAfter sorting by date:")
    showSome(db)

    searchYear = getInt("Enter year for rainfall search: ", 1938, 2018)
    searchMonth = getInt("Enter month for rainfall search: ", 1, 12)
    searchYearMonth = 100 * searchYear + searchMonth
    try:
        rainfall = findRain(db, searchYearMonth)
        print(f"Rainfall was {rainfall} mm.")
    except ValueError as message:
        print(message)

    maxR = findMax(db, 'maxT')
    print(f"\nHighest temperature {maxR['maxT']} deg C, in month {maxR['month']}, {maxR['year']}.")
    minR = findMin(db, 'minT')
    print(f"Lowest temperature {minR['minT']} deg C, in month {minR['month']}, {minR['year']}.")
    maxR = findMax(db, 'rain')
    print(f"Highest rainfall {maxR['rain']} mm, in month {maxR['month']}, {maxR['year']}.")
    maxR = findMax(db, 'snow')
    print(f"Highest snowfall {maxR['snow']} cm, in month {maxR['month']}, {maxR['year']}.")

    annualSnow = getAnnualSnow(db)
    insertionSort(annualSnow, 'totalsnow')
    minR = annualSnow[0]
    print(f"\nLowest annual snowfall {minR['totalsnow']} cm, in {minR['year']}.")
    medR = annualSnow[len(annualSnow) // 2]
    print(f"Median annual snowfall {medR['totalsnow']} cm.")    
    maxR = annualSnow[len(annualSnow) - 1]
    print(f"Highest annual snowfall {maxR['totalsnow']} cm, in {maxR['year']}.")
    
    insertionSort(db, 'meanT')
    minR = db[0]
    print(f"\nLowest mean temperature {minR['meanT']} deg C, in month {minR['month']}, {minR['year']}.")
    medR = db[len(db) // 2]
    print(f"Median mean temperature {medR['meanT']} deg C.")
    maxR = db[-1]
    print(f"Highest mean temperature {maxR['meanT']} deg C, in month {maxR['month']}, {maxR['year']}.")

    saveAnnualMeanTemp(db, "YearMeans.txt")
    
main()
