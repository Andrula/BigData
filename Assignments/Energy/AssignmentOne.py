import aiohttp
import asyncio
import requests
from time import sleep
import csv
import os.path
import datetime

sleepDelay = int()


async def getData():

    async with aiohttp.ClientSession() as session:
        async with session.get('https://api.energidataservice.dk/dataset/ElectricityProdex5MinRealtime?limit=2') as response:
            result = await response.json()
            records = result.get('records', [])
            return records                    

oldDict = []
def storeData(filename, dictList):
    """
    Store a list of dicts as CSV file
    filename: Name of file to store data in
    """
    global oldDict
    global sleepDelay

    # Creates a variable that extracts the UTC and DK timestamps from the new data
    newTimestamps = [(record['Minutes5UTC'], record['Minutes5DK']) for record in dictList]

    # Creates a variable that extracts the UTC and DK timestamps from the old data
    oldTimestamps = [(record['Minutes5UTC'], record['Minutes5DK']) for record in oldDict]

    while set (newTimestamps) == set(oldTimestamps):
       sleep(5)
       sleepDelay -= 5

    else:
        fileExist = os.path.exists(filename)

        with open(filename, 'a+', newline='') as f:
            w = csv.DictWriter(f, dictList[0].keys())

            # Checks if file already exists and if it doesn't, create the header.
            if not fileExist:
                w.writeheader()
            
            # Writes to the fil
            w.writerows(dictList)
            print("Writing data!")

        sleep(1)
        oldDict = dictList

def checkData(filename, dictList):
    global oldDict
    global sleepDelay
    print("1")
    fileExist = os.path.exists(filename)

    if fileExist:
        print("2")
        # Creates a variable that extracts the UTC and DK timestamps from the new data
        nyTimestamps = [(record['Minutes5UTC'], record['Minutes5DK']) for record in dictList]

        # Creates a variable that extracts the UTC and DK timestamps from the old data
        gamTimestamps = [(record['Minutes5UTC'], record['Minutes5DK']) for record in oldDict]

        if set(nyTimestamps) == set(gamTimestamps):
            print("Data is the same")

        


async def timeout():
    global sleepDelay
    for i in range(1, sleepDelay +1):
        print(i)
        await asyncio.sleep(1)

async def main():
    global sleepDelay
    data = await getData()
    checkData("Data/EnergyDataPer5Min.csv", data)
    try:
        while True:
            data = await getData()
            sleepDelay = 280
            storeData("Data/EnergyDataPer5Min.csv", data)
            await timeout()  # Sleep for 5 minutes before fetching data again
    except Exception as ex:
        print(f"An exception has occoured!: {ex}")

if __name__ == "__main__":
    asyncio.run(main())
